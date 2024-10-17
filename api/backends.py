import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        logger.debug(f"Attempting to authenticate email: {email}")
        try:
            user = UserModel.objects.get(email=email)
            logger.debug(f"User found for email: {email}")
            if user.check_password(password):
                logger.debug(f"Password correct for email: {email}")
                return user
            else:
                logger.warning(f"Incorrect password for email: {email}")
        except UserModel.DoesNotExist:
            logger.warning(f"No user found with email: {email}")
        return None