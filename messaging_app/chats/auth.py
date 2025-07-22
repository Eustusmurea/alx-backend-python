from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple is None:
            return None

        user, validated_token = user_auth_tuple

        if not user.is_active:
            raise AuthenticationFailed('User is inactive', code='user_inactive')

        return (user, validated_token)
    
    
