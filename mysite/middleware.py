from django.conf import settings
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseServerError, HttpResponseNotFound

class RoleBasedAccessMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path

        if path.startswith(settings.MEDIA_URL):
            return None

        user_role = request.session.get('userlogin')

        access_rules = {
            'django_user': [
                '/homepage/', '/add/', '/edit/', '/delete/', '/createsection/', '/assignsections/', '/delete_section/',
                '/login/', '/login_view/', '/signup/', '/logout/'
            ],
            'userlogin': [
                '/homepage/', '/logout/', '/login/', '/signup/'
            ]
        }

        if user_role in access_rules:
            allowed_paths = access_rules[user_role]
            if user_role == 'django_user' or any(path.startswith(allowed_path) for allowed_path in allowed_paths):
                return None

            return render(request, '404.html', status=404)

        return None


class CustomErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return self.handle_404(request, response)
        elif response.status_code == 500:
            return self.handle_500(request, response)
        return response

    def handle_404(self, request, response):
        return render(request, '404.html', status=404)

    def handle_500(self, request, response):
        return render(request, '500.html', status=500)