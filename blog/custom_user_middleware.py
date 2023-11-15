from .models import User
from django.contrib.auth.middleware import get_user


class CustomUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/admin/'):
            request.user = self.get_user(request)
        response = self.get_response(request)
        return response

    def get_user(self, request):
        try:
            user_id = request.session['_auth_user_id']
            return User.objects.get(pk=user_id, is_active=True)
        except (KeyError, User.DoesNotExist):
            return get_user(request)