from os import environ

AUTH_USER_MODEL = "questions.User"
AUTHENTICATION_BACKENDS = [
    "lung_cancer_screening.questions.auth.NHSLoginOIDCBackend",
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "/oidc/authenticate/"
LOGIN_REDIRECT_URL_FAILURE = "/agree-to-share-information"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# OIDC Client Configuration for NHS Login
# See: https://mozilla-django-oidc.readthedocs.io/
OIDC_RP_CLIENT_ID = environ.get("OIDC_RP_CLIENT_ID")
# Private key JWT authentication (no client secret)
# Set a dummy value to satisfy mozilla-django-oidc's requirement
# It w't be used since we override get_token() to use private key JWT
OIDC_RP_CLIENT_SECRET = "not-used-private-key-jwt"
OIDC_RP_CLIENT_PRIVATE_KEY = environ.get("OIDC_RP_CLIENT_PRIVATE_KEY")
OIDC_OP_FQDN = environ.get("OIDC_OP_FQDN")
OIDC_OP_AUTHORIZATION_ENDPOINT = f"{OIDC_OP_FQDN}/authorize"
OIDC_OP_TOKEN_ENDPOINT = f"{OIDC_OP_FQDN}/token"
OIDC_OP_USER_ENDPOINT = f"{OIDC_OP_FQDN}/userinfo"
OIDC_OP_JWKS_ENDPOINT = f"{OIDC_OP_FQDN}/.well-known/jwks.json"
# NHS Login requires RS512 for token endpoint authentication
# See: https://auth.sandpit.signin.nhs.uk/.well-known/openid-configuration
OIDC_RP_SIGN_ALGO = "RS512"
OIDC_RP_SCOPES = "openid profile profile_extended email"
OIDC_RP_REDIRECT_URI = f"{environ.get('BASE_URL')}/oidc/callback/"

NHS_LOGIN_SETTINGS_URL = environ.get("NHS_LOGIN_SETTINGS_URL")
