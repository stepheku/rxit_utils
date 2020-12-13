import sqlalchemy as sa
from rxit_utils.data.model_base import SqlAlchemyBase
from sqlalchemy import orm
import datetime

class LoginAction(SqlAlchemyBase):
    __tablename__ = "login_action"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    action_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    action = sa.Column(sa.String)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    # user = orm.relation("User", back_populates="users")

    def __repr__(self):
        return "<LoginAction {}>".format(action)