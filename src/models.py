from sqlalchemy import Column, Integer, Sequence, String,  DateTime, func
from src.main import db
import datetime
import jwt

class Base(db.Model):
    __abstract__ = True
    
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class User(Base):
    """
    Table schema
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def save(self):
        """
        Persist the user in the database
        :param user:
        :return:
        """
        print("In User save %s " % self)
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()

        return self.id

    @staticmethod
    def get_by_id(user_id):
        """
        Filter a user by Id.
        :param user_id:
        :return: User or None
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        """
        Check a user by their email address
        :param email:
        :return:
        """
        return User.query.filter_by(email=email).first()
