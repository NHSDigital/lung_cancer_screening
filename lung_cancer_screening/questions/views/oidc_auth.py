"""
OIDC authentication request view that uses OIDC_RP_REDIRECT_URI (BASE_URL)
so the IdP redirects back to the public hostname when running behind a proxy
that sends an internal Host header (e.g. Azure Front Door with origin_host_header).
"""
from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string

from mozilla_django_oidc.utils import (
    add_state_and_nonce_to_session,
)
from mozilla_django_oidc.views import OIDCAuthenticationRequestView


class NHSLoginAuthenticationRequestView(OIDCAuthenticationRequestView):
    """
    Use OIDC_RP_REDIRECT_URI for redirect_uri in the auth request
    instead of request.build_absolute_uri(), so the callback URL is the
    public hostname (BASE_URL) when the request Host is internal.
    """

    def get(self, request):
        state = get_random_string(self.get_settings("OIDC_STATE_SIZE", 32))
        redirect_field_name = self.get_settings("OIDC_REDIRECT_FIELD_NAME", "next")

        params = {
            "response_type": "code",
            "scope": self.get_settings("OIDC_RP_SCOPES", "openid email"),
            "client_id": self.OIDC_RP_CLIENT_ID,
            "redirect_uri": self.get_settings("OIDC_RP_REDIRECT_URI"),
            "state": state,
            # "vtr": self.get_settings("OIDC_RP_VTR"),
        }

        params.update(self.get_extra_params(request))

        if self.get_settings("OIDC_USE_NONCE", True):
            nonce = get_random_string(self.get_settings("OIDC_NONCE_SIZE", 32))
            params.update({"nonce": nonce})

        add_state_and_nonce_to_session(request, state, params)

        from mozilla_django_oidc.views import get_next_url

        request.session["oidc_login_next"] = get_next_url(
            request, redirect_field_name
        )

        query = urlencode(params)
        redirect_url = "{url}?{query}".format(
            url=self.OIDC_OP_AUTH_ENDPOINT, query=query
        )
        return HttpResponseRedirect(redirect_url)
