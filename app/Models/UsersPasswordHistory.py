from sqlalchemy import Column, String, BigInteger, DateTime
from datetime import datetime
from config.database import Base

class UsersPasswordHistory(Base):
    __tablename__ = "users_password_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UsersPasswordHistory>"
