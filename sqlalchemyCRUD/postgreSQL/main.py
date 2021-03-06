import databases, sqlalchemy, uuid, datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Postgres Database
DATABASE_URL = "postgresql://postgres:$Billga2te$@localhost/dbfastapi"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
  "users",
  metadata,
  sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
  sqlalchemy.Column("username", sqlalchemy.String),
  sqlalchemy.Column("password", sqlalchemy.String),
  sqlalchemy.Column("first_name", sqlalchemy.String),
  sqlalchemy.Column("last_name", sqlalchemy.String),
  sqlalchemy.Column("gender", sqlalchemy.CHAR),
  sqlalchemy.Column("create_at", sqlalchemy.String),
  sqlalchemy.Column("status", sqlalchemy.CHAR)
)

engine = sqlalchemy.create_engine(
  DATABASE_URL
)
metadata.create_all(engine)

# Models
class UserList(BaseModel):
  id: str
  username: str
  password: str
  first_name: str
  last_name: str
  gender: str
  create_at: str
  status: str

class UserEntry(BaseModel):
  username: str = Field(..., example="potinejj")
  password: str = Field(..., example="potinejj")
  first_name: str = Field(..., example="John")
  last_name: str = Field(..., example="Alex")
  gender: str = Field(..., example="M")

class UserUpdate(BaseModel):
  id: str = Field(..., example="Enter your id")
  first_name: str = Field(..., example="John")
  last_name: str = Field(..., example="Alex")
  gender: str = Field(..., example="M")
  status: str = Field(..., example="1")

class UserDelete(BaseModel):
  id: str = Field(..., example="Enter your id")


app = FastAPI()


@app.on_event("startup")
async def startup():
  await database.connect()


@app.on_event("shutdown")
async def shutdown():
  await database.disconnect()


@app.get("/users", response_model=List[UserList])
async def find_all_users():
  query = users.select()
  return await database.fetch_all(query)


@app.post("/users", response_model=UserList)
async def register_user(user:UserEntry):
  gID = str(uuid.uuid1())
  gDate = str(datetime.datetime.now())
  query = users.insert().values(
    id = gID,
    username = user.username,
    password = pwd_context.hash(user.password),
    first_name = user.first_name,
    last_name = user.last_name,
    gender = user.gender,
    create_at = gDate,
    status = "1"
  )
  await database.execute(query)
  return {
    "id": gID,
    **user.dict(),
    "create_at": gDate,
    "status": "1"
  }


@app.get("/users/{userId}", response_model=UserList)
async def find_user_by_id(userId:str):
  query = users.select().where(users.c.id == userId)
  return await database.fetch_one(query)


@app.put("/users", response_model=UserList)
async def update_user(user: UserUpdate):
  gDate = str(datetime.datetime.now())
  query = users.update().where(users.c.id == user.id). \
    values(
      first_name = user.first_name,
      last_name = user.last_name,
      gender = user.gender,
      create_at = gDate,
      status = user.status
    )
  await database.execute(query)
  return await find_user_by_id(user.id)


@app.delete("/users/{userId}")
async def delete_user(user:UserDelete):
  query = users.delete().where(users.c.id == user.id)
  await database.execute(query)
  return {
    "status": True,
    "message": "This user has been deleted successfully."
  }
