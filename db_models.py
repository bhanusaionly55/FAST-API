from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

# ✅ User table
class User(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)


# ✅ Notes table (linked to user)
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("credentials.id"))  # 🔥 important
    content = Column(String)