from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import backend.models as models, backend.schemas as schemas
from backend.database import SessionLocal, engine, Base

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

app = FastAPI()
# Зависимость для подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clients", response_model=schemas.ClientOut)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(name=client.name, email=client.email)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients", response_model=list[schemas.ClientOut])
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()
