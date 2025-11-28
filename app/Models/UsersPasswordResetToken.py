# /app/Models/UsersPasswordResetToken.py
from sqlalchemy import Column, String, BigInteger, DateTime
from datetime import datetime, timedelta
from config.database import Base

class UsersPasswordResetToken(Base):
    __tablename__ = "users_password_reset_tokens"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Время жизни токена (1 час)
    TOKEN_EXPIRATION_HOURS = 1
    
    def is_expired(self):
        """Проверяет, истек ли срок действия токена"""
        if self.created_at is None:
            return True
            
        # Игнорируем проверку типов для этой операции
        expiration_time = self.created_at + timedelta(hours=self.TOKEN_EXPIRATION_HOURS)  # type: ignore
        return datetime.utcnow() > expiration_time
    
    def __repr__(self):
        return f"<UsersPasswordResetToken(email='{self.email}')>"