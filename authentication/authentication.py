from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

class ServiceTokenAuthentication(TokenAuthentication):
    """
    Looks up the incoming Token, then finds the matching ServiceAccount.
    On success, returns (None, service_account) so that in views:
        request.auth == service_account
        request.auth.university == <University instance>
    """
    keyword = 'Token'

    def authenticate_credentials(self, key):
        # this returns (user, token), but we actually want token → ServiceAccount
        user, token = super().authenticate_credentials(key)
        try:
            sa = token.service_account
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid service token")
        return (None, sa)
