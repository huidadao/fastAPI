from fastapi import FastAPI
from schemas import Blog

from database import SessionLocal, engine

app = FastAPI()

# Dependency
def get_db():
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()

@app.post('/blog')
def create(blog: Blog):
  return {'title':blog.title, 'body':blog.body}