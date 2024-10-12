from typing import Tuple

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


def validate_refresh_token(token):
    try:
        token = RefreshToken(token)
        token.check_blacklist()

        return True
    except InvalidToken or TokenError:
        return False


def validate_access_token(token):
    try:
        AccessToken(token)
        return True
    except InvalidToken or TokenError:
        return False


def get_tokens(response) -> Tuple[RefreshToken, AccessToken]:
    refresh = response.data.get("refresh_token")
    access = response.data.get("access_token")
    return refresh, access
