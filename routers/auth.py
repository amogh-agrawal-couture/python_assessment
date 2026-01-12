from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import User
from auth import hash_password, verify_password, create_token
from schemas import TokenResponse, MessageResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=MessageResponse)
def signup(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user = User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()

    return {"message": "User created successfully"}


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return {
        "access_token": create_token(user.username),
        "token_type": "bearer",
    }
