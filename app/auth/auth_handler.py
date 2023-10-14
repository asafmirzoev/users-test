import jwt, time, traceback

from app.core.Database import get_environment_variables


env = get_environment_variables()


def signJWT(user_id: str) -> dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, env.JWT_SECRET, algorithm=env.JWT_ALGORITHM)

    return {"access_token": token}


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, env.JWT_SECRET, algorithms=[env.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        print(traceback.format_exc())
        return