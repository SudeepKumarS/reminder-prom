import traceback
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.connections import get_collection_from_db
from common.helper.passwords import hash_password, verify_password
from common.models.input.models import LoginUserInput, UserSignUpInput
from common.models.output.response_model import Response
from common.models.output.users import User
from common.logger import logger
from common.settings import USERS_COLLECTION_NAME, USERS_DB_NAME


docs_description = """
This is a description of the Reminder Prom API
"""

app = FastAPI(title="Reminder Prom API", description=docs_description, docs_url="/docs")



# Allow origins
origins = ["*"]

# Adding middleware and cross origins to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/")
async def home_page() -> Response:
    """
    Root Home page of the API
    """
    try:
        return Response(statusCode=200, message="Success!")
    except Exception as e:
        logger.error(f"Failed to execute: {e}")
        logger.error(traceback.format_exc())
        return Response(statusCode=400, message="Failed!")


@app.get("/check-username", tags=["Checker"])
async def check_username_exists(username: str) -> Response:
    """
    To Check if a user with name already exists or not. IF exists,
    suggesst some other usernames
    """
    try:
        # Getting required users collection
        users_collection = get_collection_from_db(USERS_DB_NAME, USERS_COLLECTION_NAME)
        db_repsonse = users_collection.find_one({"username": username})
        if db_repsonse:
            return Response(statusCode=409, message="User with this username already exists")
        return Response(statusCode=200, message="User can register with this username")
    except Exception as e:
        logger.error(f"Failed with error: {e}")
        logger.error(traceback.format_exc())
        return Response(statusCode=400, message="Failed while execution")


@app.post("/signup", tags=["Sign-up"])
async def user_sign_up(user: UserSignUpInput):
    """
    To sign-up as a user can be either a guest/registered user
    """
    try:
        # Getting required users collection
        users_collection = get_collection_from_db(USERS_DB_NAME, USERS_COLLECTION_NAME)
        user.password = hash_password(user.password)
        user_model = User(**user.dict())
        users_collection.insert_one(user_model.to_database())
        return Response(statusCode=200, data=user_model.dict_repsonse(), message="Successfully registered the user")
    except Exception as e:
        logger.error(f"Failed error: {e}")
        logger.error(traceback.format_exc())
        return Response(statusCode=400, message="Failed to register the user")


@app.post("/login", tags=["Login"])
async def login_user(user: LoginUserInput) -> Response:
    """
    To method used the login the user
    """
    try:
        # Getting required users collection
        users_collection = get_collection_from_db(USERS_DB_NAME, USERS_COLLECTION_NAME)
        db_response = users_collection.find_one(
            {
                "$or": [
                    {"email": user.username}, 
                    {"username": user.username}
                ]
            }
        )
        if not db_response:
            return Response(statusCode=404, message="Could not find user with these details")
        user_model = User.from_database(db_response)
        if not verify_password(user.password, user_model.password):
            return Response(statusCode=401, message="Invalid Password")
        return Response(statusCode=200, data=user_model.dict_repsonse(), message="Success!")
    except Exception as e:
        logger.error(f"Failed due to: {e}")
        logger.error(traceback.format_exc())
        return Response(statusCode=400, message="Failed during Execution")


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
