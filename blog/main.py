from fastapi import FastAPI
from schemas import Blog

app = FastAPI()

@app.post('/blog')
def create(blog: Blog):
  return {'title':blog.title, 'body':blog.body}