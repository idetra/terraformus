# terraformus/tokens.py
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        if not user.is_active:
            raise ValueError('User account is disabled')
        return super().for_user(user)


class CustomAccessToken(AccessToken):
    @classmethod
    def for_user(cls, user_id):
        User = get_user_model()
        user = User.objects.get(pk=user_id)
        if not user.is_active:
            raise ValueError('User account is disabled')
        return super().for_user(user)
