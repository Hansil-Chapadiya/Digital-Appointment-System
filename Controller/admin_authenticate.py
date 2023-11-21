from fastapi import HTTPException, Header, Depends, Request
from functools import wraps
from config import params
from Controller.db_init import get_database
import jwt

def get_current_user(f):
    @wraps(f)
    async def wrapper(request: Request, *args, **kwargs):
        token = request.headers.get('token')
        collection = await get_database()
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        try:
            decoded_token = jwt.decode(token, params['SECRET_KEY'], algorithms=['HS256'])
            email = decoded_token.get('email')
            user_details = await collection['Admin_hack'].find_one({"a_email": email})

            if user_details and email == user_details['a_email']:
                return await f(request, *args, **kwargs)
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except (jwt.InvalidTokenError, jwt.PyJWTError):
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return wrapper