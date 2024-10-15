from rest_framework_simplejwt.tokens import RefreshToken


class CustomToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        # Include user validation logic such as checking if the user is active
        if not user.is_active:
            raise ValueError('User account is disabled')
        return super().for_user(user)
