from .utils import decode_jwt_token
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        scope['user'] = None  
        
        if b'cookie' in headers:
            cookies = headers[b'cookie'].decode()
            token = self.get_jwt_token_from_cookies(cookies)
            if token:
                user = await self.get_user_from_token(token) 
                if user: 
                    scope['user'] = user
                else:
                    logger.error("User could not be retrieved from the token.")

        return await self.inner(scope, receive, send)

    def get_jwt_token_from_cookies(self, cookies):
        cookie_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies.split("; ")}
        return cookie_dict.get("access")

    async def get_user_from_token(self, token):
        # Decode the token and return the user object
        try:
            user = await database_sync_to_async(decode_jwt_token)(token)  
            return user
        except Exception as e:
            logger.error(f"Failed to decode token: {e}")
            return None