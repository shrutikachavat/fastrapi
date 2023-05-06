

class AuthTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth_token = request.META['HTTP_AUTHORIZATION']
            request.session['auth_token'] = auth_token
        
        if 'auth_token' in request.session:
            auth_token = request.session['auth_token']
            params = {'auth_token': auth_token}
            request.requests_params = params

        response = self.get_response(request)

        # Add auth_token to response headers
        response.set_cookie(key="auth_token",
                            value=f"Token c966e8d92d8a491cc04d41e7130c609804d1dfb6")
        
        return response