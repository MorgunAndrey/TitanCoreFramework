from sqlalchemy import Column, BigInteger, String, DateTime
from datetime import datetime
from config.database import Base

class Test(Base):
    __tablename__ = "test"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Test>"
