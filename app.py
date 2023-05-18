import jwt
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials

from common.connections import get_collection_from_db
from common.jwt_tokens import decode_credentials, generate_token
from common.models.users import User, UserRole
from common.settings import USERS_COLLECTION_NAME, USERS_DB_NAME


docs_description = """
This is a description of the Reminder Prom API
"""

app = FastAPI(title="Reminder Prom API", description=docs_description, docs_url="/docs")



# Allow origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Getting required users collection
users_collection = get_collection_from_db(USERS_DB_NAME, USERS_COLLECTION_NAME)


# Routes
@app.get("/")
async def home_page():
    return {
        "Homepage": "This is a dev server"
    }


@app.post("/login")
async def login(user: User):
    user_data = users_collection.find_one(
        {"username": user.username, "password": user.password}
    )
    if not user_data:
        raise HTTPException(
            status_code=401, detail="Invalid username or password"
        )
    token = generate_token(user_data["username"], user_data["role"])
    return {"accessToken": token}


@app.get("/users/me")
async def get_user_me(credentials: HTTPAuthorizationCredentials):
    try:
        payload = decode_credentials(credentials.credentials)
        username = payload.get("username")
        if username:
            user_data = users_collection.find_one({"username": username})
            user = User.from_camel(user_data)
            return user.to_camel()
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (jwt.InvalidTokenError, jwt.DecodeError):
        pass
    raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/users/me")
async def update_user_me(
    user: User, credentials: HTTPAuthorizationCredentials
):
    try:
        payload = decode_credentials(credentials.credentials)
        username = payload.get("username")
        if username:
            user_data = user.to_camel()
            users_collection.update_one(
                {"username": username}, {"$set": user_data}
            )
            return {"message": "User updated successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (jwt.InvalidTokenError, jwt.DecodeError):
        pass
    raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/admin/users")
async def get_users(credentials: HTTPAuthorizationCredentials):
    try:
        payload = decode_credentials(credentials.credentials)
        username = payload.get("username")
        role = payload.get("role")
        if username and role == UserRole.ADMIN:
            users_data = users_collection.find({}, {"password": 0})
            users = [
                User.from_camel(user_data).to_camel()
                for user_data in users_data
            ]
            return {"users": users}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (jwt.InvalidTokenError, jwt.DecodeError):
        pass
    raise HTTPException(status_code=401, detail="Invalid token")


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
