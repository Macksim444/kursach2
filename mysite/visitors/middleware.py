class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated and getattr(user, 'is_blocked', False):
            from django.contrib.auth import logout
            from django.shortcuts import redirect
            from django.urls import reverse
            logout(request)
            return redirect(reverse('login'))
        response = self.get_response(request)
        return response
