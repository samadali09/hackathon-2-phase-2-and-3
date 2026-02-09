import os
import json
import base64
from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# HTTP Bearer token scheme
security = HTTPBearer()

# Mock database for users (in-memory for demo)
# In a real app, this would be a proper database
class UserInDB(BaseModel):
    id: str
    email: str
    hashed_password: str
    name: Optional[str] = None

mock_users_db: dict[str, UserInDB] = {} # email -> UserInDB

# --- JWT Utility Functions ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()}) # Convert datetime to timestamp
    # For a real JWT, you'd use `jwt.encode` here.
    # For this mock, we'll just base64 encode the payload.
    encoded_jwt_payload = base64.b64encode(json.dumps(to_encode).encode('utf-8')).decode('utf-8').replace('=', '')
    # Mock signature
    mock_signature = base64.b64encode(SECRET_KEY.encode('utf-8')).decode('utf-8').replace('=', '')
    return f"header.{encoded_jwt_payload}.{mock_signature}"


def verify_mock_jwt_token(token: str) -> dict:
    """
    Verify mock JWT token and extract payload.

    For demo purposes, we're using a simple JWT-like format.
    In production, use proper JWT verification with python-jose.

    Args:
        token: JWT token string (format: header.payload.signature)

    Returns:
        dict: Token payload containing user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Split token into parts
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid token format")

        # Decode payload (middle part)
        payload_b64 = parts[1]
        # Add padding if needed
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += '=' * padding

        payload_json = base64.b64decode(payload_b64).decode('utf-8')
        payload = json.loads(payload_json)

        # Check token expiry for mock
        if "exp" in payload:
            expire_time = datetime.fromtimestamp(payload["exp"])
            if expire_time < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return payload
    except HTTPException:
        raise # Re-raise if it's already an HTTPException
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# --- Dependency for current user ID ---
def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extract user ID from JWT token.

    This dependency can be used in route handlers to get the authenticated user's ID.
    """
    token = credentials.credentials
    payload = verify_mock_jwt_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id

# --- Dependency for current user object ---
def get_current_user(
    current_user_id: str = Depends(get_current_user_id)
) -> UserInDB:
    """
    Retrieve the full user object for the authenticated user.
    """
    user = next((u for u in mock_users_db.values() if u.id == current_user_id), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def verify_user_access(path_user_id: str, token_user_id: str) -> None:
    """
    Verify that the user in the path matches the authenticated user.
    """
    if path_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
        )

# --- Schemas for Request/Response Bodies ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None

# --- API Router for Authentication ---
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=Token)
async def register_user(user_data: UserCreate):
    if user_data.email in mock_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # In a real app, hash the password
    hashed_password = user_data.password + "_hashed" # Mock hashing
    user_id = str(len(mock_users_db) + 1) # Simple mock ID

    user = UserInDB(
        id=user_id,
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name
    )
    mock_users_db[user.email] = user

    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/login", response_model=Token)
async def login_for_access_token(user_data: UserLogin):
    user = mock_users_db.get(user_data.email)

    if not user or user.hashed_password != user_data.password + "_hashed": # Mock password verification
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: UserInDB = Depends(get_current_user)):
    return UserResponse(id=current_user.id, email=current_user.email, name=current_user.name)