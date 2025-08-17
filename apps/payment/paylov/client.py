import base64
import urllib

import httpx
import requests

from rest_framework.exceptions import NotFound


from apps.payment.choices import TransactionStatus
from apps.payment.models import Transaction, UserCard, Provider
from apps.payment.paylov.constants import (
    API_ENDPOINTS,
    CHECKOUT_BASE_URL,
    STATUS_CODES,
    SUBSCRIPTION_BASE_URL,
    HTTPMethods,
)
from apps.payment.paylov.credentials import get_credentials
from apps.payment.paylov.errors import error_codes
from apps.payment.choices import ProviderChoices
from apps.users.models import User


class PaylovClient:
    """
    This class serves as a client for Paylov API.
    The client wraps API endpoints and provides methods
    to interact with the API.


    The Client consists of 2 parts:
    - Merchant API code
    - Subscribe API code
    """

    def __init__(self, params: dict | None = None) -> None:
        """
        Initialize the client with credentials and parameters.
        """
        credentials = get_credentials()
        self.MERCHANT_KEY = credentials["PAYLOV_API_KEY"]
        self.USERNAME = credentials["PAYLOV_USERNAME"]
        self.PASSWORD = credentials["PAYLOV_PASSWORD"]
        self.SUBSCRIPTION_KEY = credentials["PAYLOV_SUBSCRIPTION_KEY"]

        # Provider attrs
        self.merchant_headers = {"api-key": self.MERCHANT_KEY}
        self.subscription_headers = {"api-key": self.SUBSCRIPTION_KEY}
        self.params = params
        self.error = False
        self.code = STATUS_CODES["SUCCESS"]
        self.transaction = self.get_transaction()

    """
        Merchant API code
    """

    def send_request(
        self, to_endpoint: str, payload: dict | None = None, params: dict | None = None
    ) -> tuple[bool, dict]:
        endpoint, method = API_ENDPOINTS[to_endpoint]
        url = SUBSCRIPTION_BASE_URL + str(endpoint)
        headers = self.subscription_headers

        method_map = {
            "POST": requests.post,
            "GET": requests.get,
            "DELETE": requests.delete
        }

        try:
            response = method_map[method](url, json=payload, headers=headers, params=params)

            response.raise_for_status()
            response_data = response.json()

            return response.ok, response_data

        except requests.exceptions.HTTPError as e:
            try:
                response_data = e.response.json()
                return False, {
                    "error": {
                        "code": "api_error",
                        "message": str(e),
                        "details": response_data,
                    }
                }
            except ValueError:
                return False, {
                    "error": {
                        "code": "api_error",
                        "message": str(e),
                        "details": "Non-JSON response",
                    }
                }
        except requests.exceptions.RequestException as e:
            return False, {"error": {"code": "api_error", "message": str(e)}}
        except ValueError as e:
            return False, {"error": {"code": "invalid_response", "message": str(e)}}

    @classmethod
    def create_payment_link(cls, transaction: Transaction) -> str:
        credentials = get_credentials()
        merchant_key = credentials["PAYLOV_API_KEY"]
        return_url = urllib.parse.quote(
            credentials["PAYLOV_REDIRECT_URL"] + f"?transaction_id={transaction.id}",
            safe="",
        )

        if merchant_key is None:
            raise ValueError("Credentials not found")

        amount = int(transaction.amount)
        query = f"merchant_id={merchant_key}&amount={amount}&account.order_id={transaction.id}&return_url={return_url}"
        encode_params = base64.b64encode(query.encode("utf-8"))
        encode_params = str(encode_params, "utf-8")
        return f"{CHECKOUT_BASE_URL}{encode_params}"


    """
        Subscribe API code
    """

    def create_user_card(self, user, card_number: str, expire_month: str, expire_year: str) -> tuple[bool, dict]:
        expire_date_str = expire_year + expire_month

        payload = {
            "userId": str(user.id),
            "cardNumber": str(card_number),
            "expirenDate": str(expire_date_str),
        }

        success, response_data = self.send_request("CREATE_CARD", payload=payload)

        if success:
            otp_sent_phone = response_data["result"]["otpSentPhone"]
            card_id = response_data["result"]["cid"]

            paylov_provider = Provider.objects.filter(key="paylov").last()
            is_already_exists = UserCard.objects.filter(user=user, card_token=card_id).exists()

            if is_already_exists:
                return self.get_error_response("card_exists")

            user_card, _ = UserCard.objects.create(
                user=user,
                card_token=card_id,
                provider=paylov_provider,
                expire_month=expire_month,
                expire_year=expire_year,
                is_confirmed=False
            )

            return True, {"otp_sent_phone": otp_sent_phone, "card_id": card_id}

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)


    def confirm_user_card(self, user: User, card_id: int, otp: str, card_name: str | None) -> tuple[bool, dict]:
        try:
            card = UserCard.objects.get(user=user, id=card_id)
        except UserCard.DoesNotExist:
            return self.get_error_response("card_not_found")

        if card.is_confirmed:
            return self.get_error_response("card_already_confirmed")

        payload = {
            "cardId": card.card_token,
            "otp": otp,
            "cardName": card_name or "User",
        }

        success, response_data = self.send_request("CONFIRM_CARD", payload=payload)

        if success or not response_data.get("error", {}).get("code") == "card_is_already_activated":
            card_data = response_data.get("result", {}).get("card", {})

            if card_data:
                card.is_confirmed = True
                card.cardholder_name = card_data.get("owner", "")
                card.last_four_digits = card_data.get("number")[-4:]
                card.save(update_fields=["is_confirmed"])
                return True, {"card_token": card.card_token, "is_confirmed": True}

        error_code = response_data.get(
            "error", {"code": "unknown_error"}
        ).get(
            "details", {"code": "unknown_error"}
        ).get(
            "details", {"code": "unknown_error"}
        )["code"]

        return self.get_error_response(error_code)


        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)


    def get_user_cards(self, user_id: str) -> tuple[bool, dict]:
        query_params = {"userId": str(user_id)}
        success, response_data = self.api_request("GET_CARDS", params=query_params)

        if success:
            return success, response_data

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)


    def delete_user_card(self, user: User, card_id:str) -> tuple[bool, dict]:
        card = UserCard.objects.filter(id=int(card_id)).first()

        if not card:
            raise NotFound("User card not found", code="card_not_found")

        query_param = {"userCardId": card.card_id}
        success, response_data = self.api_request("DELETE_CARD", params=query_param)

        if success:
            card.soft_delete()
            response_data = {
                "detail": "User card deleted successfully",
                "code": 204
            }
            return success, response_data

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)


    """
         Utility methods
    """

    def get_transaction(self) -> Transaction | None:
        """
        Get the transaction from the database based on the provided params.
        """
        if not self.params or not self.params.get("account"):
            return None
        try:
            return Transaction.objects.get(id=self.params["account"]["order_id"])
        except Transaction.DoesNotExist:
            return None

    @staticmethod
    def send_error_response(error_code: str) -> tuple[bool, dict]:
        error_details = error_codes.get(
            str(error_code).upper(), ["unknown_error", "Unknown error"]
        )

        error_response = {"detail": error_details[1], "code": error_details[0]}
        return False, error_response

    @staticmethod
    def get_error_response(error_code: str) -> tuple[bool, dict]:
        error_details = error_codes.get(str(error_code).upper(), ["unknown_error", "Unknown error"])
        error_response = {
            "detail": error_details[1],
            "code": error_details[0]
        }
        return False, error_response

    def check_transaction(self) -> tuple[bool, str]:
        if not self.transaction:
            return True, STATUS_CODES["ORDER_NOT_FOUND"]

        self.is_transaction_already_completed()
        self.is_transaction_amount_correct(self.params["amount"])
        return self.error, self.code

    def perform_transaction(self) -> tuple[bool, str]:
        if not self.transaction:
            return True, STATUS_CODES["ORDER_ALREADY_PAID"]

        if self.transaction.status == TransactionStatus.FAILED:
            return True, STATUS_CODES["SERVER_ERROR"]

        self.is_transaction_already_completed()
        self.is_transaction_amount_correct(self.params["amount"])
        return self.error, self.code

    def is_transaction_already_completed(self):
        if self.transaction.status == TransactionStatus.COMPLETED:
            self.error = True
            self.code = STATUS_CODES["ORDER_ALREADY_PAID"]

    def is_transaction_amount_correct(self, amount: int):
        if int(self.transaction.amount) != int(amount):
            self.error = True
            self.code = STATUS_CODES["INVALID_AMOUNT"]