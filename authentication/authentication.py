from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from .models import ServiceAccount

class ServiceTokenAuthentication(TokenAuthentication):
    keyword = 'Token'

    def authenticate_credentials(self, key):
        """
        Look up the Token, then its ServiceAccount, and attach
        the university code to request.auth for downstream use.
        """
        try:
            token = Token.objects.select_related('serviceaccount').get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        try:
            svc = token.serviceaccount
        except ServiceAccount.DoesNotExist:
            raise AuthenticationFailed('No matching service account')

        # Stash the university on the token object
        token.university = svc.university  
        return (None, token)
