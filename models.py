from pydantic import BaseModel


# 🔐 Login request (what frontend sends)
class UserLogin(BaseModel):
    username: str
    password: str


# 👤 User response (what backend returns)
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True   # for SQLAlchemy compatibility


# 📝 Journal request (DONE button)
class JournalCreate(BaseModel):
    content: str


# 📝 Journal response (when loading page)
class JournalResponse(BaseModel):
    content: str

    class Config:
        from_attributes = True