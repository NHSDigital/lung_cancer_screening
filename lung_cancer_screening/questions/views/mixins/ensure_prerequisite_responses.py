from django.shortcuts import redirect

class EnsurePrerequisiteResponsesMixin:
    def dispatch(self, request, *args, **kwargs):
        for (
            prerequisite_response,
            redirect_url,
        ) in self.get_prerequisite_responses_redirect_map().items():
            if not hasattr(self.get_object_parent(), prerequisite_response):
                return redirect(redirect_url)

        return super().dispatch(request, *args, **kwargs)


    def get_prerequisite_responses_redirect_map(self):
        return {}


    def get_object_parent(self):
        raise NotImplementedError("get_object_parent must be implemented")
