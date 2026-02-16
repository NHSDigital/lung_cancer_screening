from unittest.mock import Mock, patch
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.conf import settings
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from ...auth import NHSLoginOIDCBackend
from ...tests.factories.user_factory import UserFactory

User = get_user_model()

@override_settings(
        OIDC_RP_CLIENT_PRIVATE_KEY=None,  # Will be set per test
        OIDC_OP_TOKEN_ENDPOINT='https://auth.example.com/token',
        OIDC_RP_CLIENT_ID='test-client-id',
        OIDC_RP_REDIRECT_URI='https://app.example.com/callback',
        OIDC_RP_SIGN_ALGO='RS512',
    )
class TestNHSLoginOIDCBackend(TestCase):

    def setUp(self):
        self.backend = NHSLoginOIDCBackend()
        # Generate a test private key for JWT signing
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.test_private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        self.claims = {
            "sub": "nhs-login-sub-123",
            "nhs_number": "1234567890",
            "email": "test@example.com",
            "given_name": "Jane",
            "family_name": "Smith",
        }

    def test_filter_users_by_claims_for_existing_user(self):
        claims = { "sub": self.claims.get('sub') }
        user = User.objects.create_user(**self.claims)

        result = self.backend.filter_users_by_claims(claims)

        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), user)

    def test_filter_users_by_claims_for_non_existent_user(self):
        claims = {"sub": "other-sub-456"}
        result = self.backend.filter_users_by_claims(claims)

        self.assertEqual(result.count(), 0)

    def test_filter_users_by_claims_when_no_claim_is_provided(self):
        result = self.backend.filter_users_by_claims({})

        self.assertEqual(result.count(), 0)


    def test_create_user_creates_a_valid_user(self):
        user = self.backend.create_user(self.claims)

        self.assertEqual(user.sub, self.claims["sub"])
        self.assertEqual(user.nhs_number, self.claims["nhs_number"])
        self.assertEqual(user.email, self.claims["email"])
        self.assertEqual(user.given_name, self.claims["given_name"])
        self.assertEqual(user.family_name, self.claims["family_name"])


    def test_create_user_without_sub_raises_error(self):
        claims = {}

        with self.assertRaises(ValueError) as context:
            self.backend.create_user(claims)

        self.assertIn("Missing 'sub' claim", str(context.exception))


    def test_update_user_updates_the_user(self):
        user = UserFactory.create(sub='sub-123', nhs_number='1234567890')
        claims = {
            'sub': 'sub-123',
            'nhs_number': '1234567890',
            'email': 'test@example.com',
            'given_name': 'Jane',
            'family_name': 'Smith',
        }

        result = self.backend.update_user(user, claims)

        self.assertEqual(result, user)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.given_name, 'Jane')
        self.assertEqual(user.family_name, 'Smith')
        self.assertEqual(user.nhs_number, '1234567890')


    @patch('lung_cancer_screening.questions.auth.requests.post')
    def test_get_token_success(self, mock_post):
        settings.OIDC_RP_CLIENT_PRIVATE_KEY = self.test_private_key_pem

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {'access_token': 'token123'}
        mock_post.return_value = mock_response

        token_payload = {
            'redirect_uri': 'https://app.example.com/somewhereelse',
            'code': 'auth-code-123'
        }

        result = self.backend.get_token(token_payload)

        self.assertEqual(result, {'access_token': 'token123'})
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], 'https://auth.example.com/token')
        self.assertEqual(
            call_args[1]['headers']['Content-Type'],
            'application/x-www-form-urlencoded'
        )
        # Verify the request includes client_assertion
        data = call_args[1]['data']
        self.assertIn('client_assertion', data)
        self.assertEqual(
            data['client_assertion_type'],
            'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
        )
        self.assertEqual(data['grant_type'], 'authorization_code')
        self.assertEqual(data['code'], 'auth-code-123')
        # redirect_uri is always OIDC_RP_REDIRECT_URI so it matches the auth request
        self.assertEqual(data['redirect_uri'], 'https://app.example.com/callback')

    @patch('lung_cancer_screening.questions.auth.requests.post')
    def test_get_token_without_redirect_uri(self, mock_post):
        settings.OIDC_RP_CLIENT_PRIVATE_KEY = self.test_private_key_pem

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {'access_token': 'token123'}
        mock_post.return_value = mock_response

        token_payload = {'code': 'auth-code-123'}

        result = self.backend.get_token(token_payload)

        self.assertEqual(result, {'access_token': 'token123'})
        call_args = mock_post.call_args
        data = call_args[1]['data']
        self.assertEqual(
            data['redirect_uri'], 'https://app.example.com/callback'
        )

    @override_settings(
        OIDC_RP_CLIENT_PRIVATE_KEY=None,  # Will be set per test
    )
    @patch('lung_cancer_screening.questions.auth.requests.post')
    def test_get_token_no_client_assertion(self, mock_post):
        token_payload = {'code': 'auth-code-123'}

        with patch.object(
            NHSLoginOIDCBackend.__bases__[0], 'get_token'
        ) as mock_parent_get_token:
            mock_parent_get_token.return_value = {'access_token': 'token'}

            result = self.backend.get_token(token_payload)

            self.assertEqual(result, {'access_token': 'token'})
            mock_parent_get_token.assert_called_once_with(token_payload)
            mock_post.assert_not_called()

    @patch('lung_cancer_screening.questions.auth.requests.post')
    def test_get_token_nhs_login_error_response(self, mock_post):
        settings.OIDC_RP_CLIENT_PRIVATE_KEY = self.test_private_key_pem

        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.text = 'Invalid request'
        mock_response.json.return_value = {'error': 'invalid_request'}
        mock_post.return_value = mock_response

        token_payload = {
            'redirect_uri': 'https://app.example.com/callback',
            'code': 'auth-code-123'
        }

        with self.assertRaises(ValueError) as context:
            self.backend.get_token(token_payload)

        self.assertIn('Token request failed: 400', str(context.exception))

    @patch('lung_cancer_screening.questions.auth.requests.post')
    def test_get_token_nhs_login_error_response_no_json(self, mock_post):
        settings.OIDC_RP_CLIENT_PRIVATE_KEY = self.test_private_key_pem

        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_response.json.side_effect = ValueError('Not JSON')
        mock_post.return_value = mock_response

        token_payload = {
            'redirect_uri': 'https://app.example.com/callback',
            'code': 'auth-code-123'
        }

        with self.assertRaises(ValueError) as context:
            self.backend.get_token(token_payload)

        self.assertIn('Token request failed: 500', str(context.exception))
