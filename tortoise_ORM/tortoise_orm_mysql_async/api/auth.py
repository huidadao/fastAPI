from typing import List
from fastapi import APIRouter, status, HTTPException, Response
from .db import database, User
from .Schemas import LoginSchema
from passlib.hash import pbkdf2_sha256
from .Token import create_access_token 


router = APIRouter(
   tags = ['Auth']
)


@router.post('/login')
async def login(request: LoginSchema):
   query = User.select().where(User.c.username==request.username)
   user = await database.fetch_one(query=query)
   if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

   if not pbkdf2_sha256.verify(request.password, user.password):
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')
   
   access_token = create_access_token(data={"sub": user.username})
   return {"access_token": access_token, "token_type": "bearer"}