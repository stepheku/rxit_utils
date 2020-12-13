import sqlalchemy as sa
from rxit_utils.data.model_base import SqlAlchemyBase
import datetime

class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    username = sa.Column(sa.String, index=True, unique=True)
    hashed_password = sa.Column(sa.String, index=True)
    last_login = sa.Column(sa.DateTime, default=datetime.datetime.now)

    # login_action = sa.orm.relation("LoginAction", back_populates="login_action")

    def __repr__(self):
        return "<User {}>".format(self.username)