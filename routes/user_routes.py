from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import UserCreate, User as UserSchema
from database import get_db
from auth import verify_password, get_password_hash, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Crear un usuario
@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Loguear usuario y obtener token
@router.post("/token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Obtener el usuario actual
@router.get("/me/", response_model=UserSchema)
def read_users_me(current_user: UserSchema = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # El uso de `oauth2_scheme` en `Depends` aquí no proporciona un objeto `UserSchema`. Necesitas obtener el usuario desde la base de datos.
    user = db.query(UserModel).filter(UserModel.username == current_user.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user