"""Session timeout: 30 min inactivity or 12 h absolute."""
import time

from django.conf import settings
from django.shortcuts import redirect
from django.utils.http import urlencode


class SessionTimeoutMiddleware:
    """
    Expire session after INACTIVITY_TIMEOUT_SECONDS of inactivity
    or ABSOLUTE_TIMEOUT_SECONDS since session start.
    """

    INACTIVITY_TIMEOUT_SECONDS = 30 * 60
    ABSOLUTE_TIMEOUT_SECONDS = 12 * 60 * 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(request, "user", None) or not request.user.is_authenticated:
            return self.get_response(request)

        now = time.time()
        session = request.session

        if "_session_start" not in session:
            session["_session_start"] = now
        session_start = session["_session_start"]

        last_activity = session.get("_last_activity", now)
        last_activity_timed_out = (now - last_activity) > self.INACTIVITY_TIMEOUT_SECONDS
        absolutely_timed_out = (now - session_start) > self.ABSOLUTE_TIMEOUT_SECONDS

        if last_activity_timed_out or absolutely_timed_out:
            session.flush()
            login_url = settings.LOGIN_URL
            query = {"next": request.get_full_path()}
            return redirect(f"{login_url}?{urlencode(query)}")

        session["_last_activity"] = now
        return self.get_response(request)
