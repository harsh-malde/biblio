from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..security import hash_password, verify_password, create_access_token, get_current_user 
from ..database import get_db
from ..models import UsersDB
from ..schemas import UserCreate, UserOut
from ..security import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup", status_code=201, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = UsersDB(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UsersDB).filter(UsersDB.email == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def read_current_user(current_user: UsersDB = Depends(get_current_user)):
    return current_user