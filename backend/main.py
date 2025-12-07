from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.db import SessionLocal, engine, Base

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):

    query = text("SELECT id, file_name, status FROM dummy")

    result = db.execute(query).fetchall()

    return {
        "status": "connected",
        "rows": len(result),
        "data": [dict(row._mapping) for row in result]
    }

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)