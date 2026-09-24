from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from datetime import datetime
import os

engine = create_engine('sqlite:///fitbuddy.db', connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, index=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)
    intensity = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    plan = relationship("Plan", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Plan(Base):
    __tablename__ = 'plans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    original_plan = Column(Text)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="plan")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

def save_user(db: Session, user_data: dict):
    user = db.query(User).filter(User.user_id == user_data['user_id']).first()
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
    else:
        user = User(**user_data)
        db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

def save_plan(db: Session, user_id: str, plan: str, tip: str):
    existing_plan = db.query(Plan).filter(Plan.user_id == user_id).first()
    if existing_plan:
        existing_plan.original_plan = plan
        existing_plan.nutrition_tip = tip
        existing_plan.updated_plan = None
        existing_plan.feedback = None
        existing_plan.updated_at = datetime.utcnow()
    else:
        new_plan = Plan(user_id=user_id, original_plan=plan, nutrition_tip=tip)
        db.add(new_plan)
    db.commit()

def update_plan(db: Session, user_id: str, updated_plan: str, feedback: str):
    plan = db.query(Plan).filter(Plan.user_id == user_id).first()
    if plan:
        plan.updated_plan = updated_plan
        plan.feedback = feedback
        plan.updated_at = datetime.utcnow()
        db.commit()

def get_original_plan(db: Session, user_id: str) -> str:
    plan = db.query(Plan).filter(Plan.user_id == user_id).first()
    if plan:
        return plan.original_plan
    return None

def get_all_users(db: Session):
    return db.query(User).all()

def get_all_plans(db: Session):
    return db.query(Plan).all()

def delete_user(db: Session, user_id: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
