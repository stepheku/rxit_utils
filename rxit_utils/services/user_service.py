from rxit_utils.data.db_session import DbSession
from rxit_utils.data.users import User
from passlib.hash import pbkdf2_sha256
import typing


def create_user(username: str, email: str, password: str) -> User:
    user = User()
    user.username = username
    user.email = email
    user.hashed_password = hash_text(password)

    session = DbSession.factory()
    session.add(user)
    session.commit()

    return user


def login_user(username: str, password: str) -> typing.Optional[User]:
    if not username:
        return None

    session = DbSession.factory()
    user = session.query(User).filter(User.username == username).first()
    if not user:
        return None

    if not verify_hash(hashed_text=user.hashed_password, plain_text=password):
        return None

    return user


def find_user_by_id(user_id: int) -> typing.Optional[User]:
    session = DbSession.factory()
    user = session.query(User).filter(User.id == user_id).first()
    return user


def find_user_by_username(username: str) -> typing.Optional[User]:
    session = DbSession.factory()
    user = session.query(User).filter(User.username == username).first()
    return user


def hash_text(text: str) -> str:
    hashed_text = pbkdf2_sha256.hash(text)
    return hashed_text


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return pbkdf2_sha256.verify(plain_text, hashed_text)