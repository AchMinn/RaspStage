from django.shortcuts import redirect
from django.urls import resolve

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current URL
        current_url = resolve(request.path_info).url_name

        # Allow access to login, register, and guest pages for all users
        if current_url in ['login', 'register', 'logout', 'guest']:
            # If the user is already logged in, redirect them to the home page
            if request.user.is_authenticated and current_url == 'login':
                return redirect('home')
            return self.get_response(request)

        # Allow access to home page for all users
        if current_url == 'home':
            return self.get_response(request)

        # Allow access to all pages for superusers
        if request.user.is_authenticated and request.user.is_superuser:
            return self.get_response(request)


        # Allow access to all pages for staff users
        if request.user.is_authenticated and request.user.is_staff:
            return self.get_response(request)

        # Allow access to certain pages for regular users
        if request.user.is_authenticated and not request.user.is_superuser:
            allowed_urls = ['devices', 'rooms', 'guest', 'device-detail', 'room-detail', 'device-control']
            if current_url in allowed_urls:
                return self.get_response(request)


        # Redirect to the login page if the user is not allowed to access the current page
        return redirect('login')