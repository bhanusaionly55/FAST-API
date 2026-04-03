from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from db_models import Base, User, Note   # ✅ correct import
from models import UserLogin, UserResponse, JournalCreate, JournalResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ create tables (correct way)
Base.metadata.create_all(bind=engine)


# ✅ DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Login
@app.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return db_user


# ✅ Load journal
@app.get("/journal/{user_id}", response_model=JournalResponse)
def get_journal(user_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.user_id == user_id).first()
    return {"content": note.content if note else ""}


# ✅ Save / Update journal
@app.post("/journal/{user_id}")
def save_journal(user_id: int, journal: JournalCreate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.user_id == user_id).first()

    if note:
        note.content = journal.content
    else:
        note = Note(user_id=user_id, content=journal.content)
        db.add(note)

    db.commit()
    return {"message": "Saved successfully"}


# ✅New user

@app.post("/register")
def register(user: UserLogin, db: Session = Depends(get_db)):
    
    print("Incoming user:", user.username)

    existing = db.query(User).filter(User.username == user.username).first()

    print("Existing user:", existing)

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()

    return {"message": "User created"}
    
# ✅ Delete user and their notes

@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    # delete notes first
    db.query(Note).filter(Note.user_id == user_id).delete()

    # delete user
    db.query(User).filter(User.id == user_id).delete()

    db.commit()

    return {"message": "User deleted"}
