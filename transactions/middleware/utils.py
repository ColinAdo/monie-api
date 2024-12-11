import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get('user_id')
        return User.objects.get(id=user_id)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None