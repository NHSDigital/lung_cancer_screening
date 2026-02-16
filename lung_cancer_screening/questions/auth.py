"""
Custom OIDC authentication backend for NHS Login with private key JWT.
"""
import logging
import time
import requests
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger(__name__)


class NHSLoginOIDCBackend(OIDCAuthenticationBackend):
    """
    Custom OIDC authentication backend that uses private key JWT
    for client authentication instead of client secret.
    Uses NHS number as the username field.
    """

    def filter_users_by_claims(self, claims):
        """Find users by NHS number from OIDC claims."""
        user_class = get_user_model()

        nhs_number = claims.get('nhs_number')
        if not nhs_number:
            return user_class.objects.none()

        return user_class.objects.filter(nhs_number=nhs_number)

    def create_user(self, claims):
        user_class = get_user_model()

        nhs_number = claims.get('nhs_number')
        if not nhs_number:
            raise ValueError("Missing 'nhs_number' claim in OIDC token")

        email = claims.get('email')
        given_name = claims.get('given_name')
        family_name = claims.get('family_name')
        return user_class.objects.create_user(
            nhs_number=nhs_number,
            email=email,
            given_name=given_name,
            family_name=family_name,
        )

    def update_user(self, user, claims):
        changed = False
        email = claims.get('email')
        given_name = claims.get("given_name")
        family_name = claims.get("family_name")

        if email and user.email != email:
            user.email = email
            changed = True

        if given_name and user.given_name != given_name:
            user.given_name = given_name
            changed = True

        if family_name and user.family_name != family_name:
            user.family_name = family_name
            changed = True

        if changed:
            user.save()

        return user

    def _create_client_assertion(self):
        private_key_pem = settings.OIDC_RP_CLIENT_PRIVATE_KEY
        if not private_key_pem:
            return None

        try:
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode('utf-8'),
                password=None,
            )
        except Exception as e:
            raise ValueError(f"Failed to load private key: {e}") from e

        token_endpoint = settings.OIDC_OP_TOKEN_ENDPOINT
        client_id = settings.OIDC_RP_CLIENT_ID

        now = int(time.time())
        claims = {
            'iss': client_id,
            'sub': client_id,
            'aud': token_endpoint,
            'jti': f"{client_id}-{now}",  # noqa: E501
            'iat': now,
            'exp': now + 300,
        }

        headers = {'alg': settings.OIDC_RP_SIGN_ALGO}

        assertion = jwt.encode(
            claims,
            private_key,
            algorithm=settings.OIDC_RP_SIGN_ALGO,
            headers=headers
        )

        if isinstance(assertion, bytes):
            return assertion.decode('utf-8')
        return assertion

    def get_token(self, token_payload):
        token_endpoint = settings.OIDC_OP_TOKEN_ENDPOINT
        redirect_uri = token_payload.get('redirect_uri')
        authorization_code = token_payload.get('code')

        if not redirect_uri:
            redirect_uri = settings.OIDC_RP_REDIRECT_URI

        client_assertion = self._create_client_assertion()
        if not client_assertion:
            return super().get_token(token_payload)

        token_payload_updated = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_assertion': client_assertion,
            'client_assertion_type': (
                'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
            ),
        }

        response = requests.post(
            token_endpoint,
            data=token_payload_updated,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            verify=True,
            timeout=30,
        )

        if not response.ok:
            error_detail = response.text
            try:
                error_detail = response.json()
            except Exception:
                pass
            logger.error(
                "Token request failed: %s - %s",
                response.status_code,
                error_detail
            )
            raise ValueError(
                f"Token request failed: {response.status_code} - "
                f"{error_detail}"
            )

        return response.json()
