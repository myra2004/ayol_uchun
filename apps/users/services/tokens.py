from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from core.constants import TOKEN_EXPIRY_SECONDS

signer = TimestampSigner(salt='password-reset')


def generate_number_confirm_token(user):
    return signer.sign(user.pk)

def verify_number_confirm_token(token):
    try:
        unsigned = signer.unsign(token, max_age=TOKEN_EXPIRY_SECONDS)
        return int(unsigned)
    except (BadSignature, SignatureExpired):
        return None


def generate_temporary_password():
    return signer.sign('temporary')