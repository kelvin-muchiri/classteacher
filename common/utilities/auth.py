import logging
import jwt

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.db.models import Q

from common.utilities import validate_phone_number

from django.conf import settings

from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header
)
from rest_framework.exceptions import (
    AuthenticationFailed,
)

LOGGER = logging.getLogger(__name__)
User = get_user_model()

class ClassteacherAuthenticationBackend:
    """
    Custom AuthenticationBackend for Cloud9xp.

    Default: ``django.contrib.auth.backends.ModelBackend``

    We want this to run first for purposes of authenticating users using
    either:
        1. Email address
        2. Phone Number (recommended default) or
        3. Board Number (For Doctors ONLY)

    If it fails, we fall back to 'django.contrib.auth.backends.ModelBackend'
    which uses the `phone_number` field, which has been set as the default
    `USERNAME_FIELD` in the custom `User` model (api.users.models.User).
    """

    def validate_username(self, username):
        # Check if username is a valid email address
        if username is None:
            raise ValidationError(
                "Provide a valid phone_number or email address.")
        if username.startswith("+") and username[1:].isalnum():  # Phone Number
            validate_phone_number(username)
        if "@" in username:  # Email address
            validate_email(username)

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def authenticate(self, username=None, password=None, **kwargs):
        self.validate_username(username)
        try:
            user = User.objects.get(
                Q(phone_number=username) | Q(email=username))
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        except Exception as e:
            LOGGER.error(
                'Unexpected error: ', exc_info=True, extra=e.args
            )
            return None
        else:
            if user.check_password(password) and \
                    self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


class JWTAuthentication(BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires authentication. 

        `authenticate` has two possible return values:

        1) `None` - We return `None` if we do not wish to authenticate. Usually
                    this means we know authentication will fail. An example of
                    this is when the request does not include a token in the
                    headers.

        2) `(user, token)` - We return a user/token combination when 
                             authentication is successful.

                            If neither case is met, that means there's an error 
                            and we do not return anything.
                            We simple raise the `AuthenticationFailed` 
                            exception and let Django REST Framework
                            handle the rest.
        """
        request.user = None

        # `auth_header` should be an array with two elements: 1) the name of
        # the authentication header (in this case, "Token") and 2) the JWT 
        # that we should authenticate against.
        auth_header = get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Invalid token header. No credentials provided. Do not attempt to
            # authenticate.
            return None

        elif len(auth_header) > 2:
            # Invalid token header. The Token string should not contain spaces. Do
            # not attempt to authenticate.
            return None

        # The JWT library we're using can't handle the `byte` type, which is
        # commonly used by standard libraries in Python 3. To get around this,
        # we simply have to decode `prefix` and `token`. This does not make for
        # clean code, but it is a good decision because we would get an error
        # if we didn't decode these values.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            # The auth header prefix is not what we expected. Do not attempt to
            # authenticate.
            return None

        # By now, we are sure there is a *chance* that authentication will
        # succeed. We delegate the actual credentials authentication to the
        # method below.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise AuthenticationFailed(msg)

        return (user, token)