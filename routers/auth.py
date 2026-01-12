from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import User
from auth import hash_password, verify_password, create_token
from schemas import TokenResponse, MessageResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------------- SIGNUP ----------------
@router.post("/signup", response_model=MessageResponse)
def signup(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    user = User(
        username=username,
        password=hash_password(password),
    )

    db.add(user)
    db.commit()

    return {"message": "User created successfully"}


# ---------------- LOGIN ----------------
@router.post("/login", response_model=TokenResponse)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_token(user.username)

    # 🔐 Store JWT in HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # set True in production (HTTPS)
        max_age=60 * 60 * 2,  # 2 hours
    )

    return {
        "access_token": token,
        "token_type": "cookie",
    }


# ---------------- LOGOUT (OPTIONAL) ----------------
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        samesite="lax",
    )
    return {"message": "Logged out successfully"}

