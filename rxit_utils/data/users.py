import sqlalchemy as sa
from rxit_utils.data.model_base import SqlAlchemyBase
import datetime

class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    user_name = sa.Column(sa.String, index=True, unique=True)
    hashed_password = sa.Column(sa.String, index=True)
    last_login = sa.Column(sa.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "<User {}>".format(user_name)