from .base import * # noqa

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
DEBUG = False