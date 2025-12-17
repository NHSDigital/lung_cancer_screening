import time
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect


SESSION_START_KEY = "_session_start_"
LAST_ACTIVITY_KEY = "_last_activity_"
INACTIVITY_TIMEOUT = 30 * 60
CONTINUOUS_USAGE_TIMEOUT = 12 * 60 * 60


class SessionTimeoutMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self._should_modify_session(request):
            return self.get_response(request)

        now = time.time()

        if self._expired(request.session, now):
            logout(request)
            return redirect(settings.LOGOUT_REDIRECT_URL)

        self._update_session(request.session, now)

        return self.get_response(request)


    def _should_modify_session(self, request):
        return False if request.session.is_empty() or not request.user.is_authenticated else True


    def _inactivity_expired(self, session, now):
        last_activity = session.get(LAST_ACTIVITY_KEY, now)
        return (now - last_activity) > INACTIVITY_TIMEOUT


    def _continuous_usage_expired(self, session, now):
        session_start = session.get(SESSION_START_KEY, now)
        return (now - session_start) > CONTINUOUS_USAGE_TIMEOUT


    def _expired(self, session, now):
        return (
            self._inactivity_expired(session, now) or
            self._continuous_usage_expired(session, now)
        )

    def _update_session(self, session, now):
        session[LAST_ACTIVITY_KEY] = now
        session.setdefault(SESSION_START_KEY, now)
        session.save()
