# app/database/seeders/database_seeder.py
from sqlalchemy.orm import Session
from app.Models.User import User
from app.Models.UsersPasswordHistory import UsersPasswordHistory  # Импортируем модель истории паролей
from config.database import SessionLocal
import hashlib
from datetime import datetime
from app.Services.AuthService import AuthService

def seed():
    db: Session = SessionLocal()

    try:
        email = 'admin@gmail.com'
        password = 'Admin12345'
        existing = db.query(User).filter_by(email=email).first()
        
        if not existing:
            password_hash = AuthService.get_password_hash(password)
            
            # Создаем пользователя
            test_user = User(
                name='Titan',
                email=email,
                password=password_hash, 
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)  # Обновляем объект чтобы получить ID
            
            # Сохраняем пароль в историю
            password_history = UsersPasswordHistory(
                user_id=test_user.id,
                password=password_hash,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(password_history)
            db.commit()
            
            print(f"[Success] Пользователь {email} создан и пароль сохранен в историю")
        else:
            print(f"[Warning]️ Пользователь {email} уже существует")

    except Exception as e:
        print(f"[ERROR] Ошибка при вставке пользователя: {e}")
        db.rollback()
    finally:
        db.close()
