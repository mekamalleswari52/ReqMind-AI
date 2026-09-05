from ..models.user import User
from ..utils.security import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session

def create_user(db: Session, full_name: str, email: str, password: str):
    user = User(full_name=full_name, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "user": user}
