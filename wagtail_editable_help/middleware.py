from asgiref.local import Local


_local_data = Local()


class EditableHelpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user'):
            _local_data.user = request.user

        response = self.get_response(request)

        try:
            del _local_data.user
        except AttributeError:
            pass

        return response


def get_active_user():
    return getattr(_local_data, 'user', None)
