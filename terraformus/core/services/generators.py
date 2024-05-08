import uuid

from django.db import IntegrityError


def create_anonymous_user():
    from django.contrib.auth import get_user_model

    User = get_user_model()

    while True:
        # Generate a secure unique string
        security_string = str(uuid.uuid4())[:5]
        anonymous_username = f'Anonymous-{security_string}'

        try:
            # Create an Anonymous User and customized User model fields
            anonymous_user = User.objects.create_user(
                username=anonymous_username,
                first_name='Anonymous',
                last_name=security_string,
                password=None,
                email=None
            )

            break
        except IntegrityError:
            continue

    return anonymous_user
