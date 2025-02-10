from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from db_connection import get_database
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/messages", tags=["messages"])

def get_collection() -> Collection:
    db = get_database("textME")
    return db["messages"]

class Message(BaseModel):
    de: EmailStr
    para: EmailStr
    asunto: str = Field(..., max_length=80)
    contenido: str
    adjunto: Optional[str] = None

@router.get("/{user_id}")
def get_user_messages(user_id: str, collection: Collection = Depends(get_collection)):
    messages = list(collection.find({"$or": [{"de": user_id}, {"para": user_id}]}).sort("stamp", -1))
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found")
    for msg in messages:
        msg["id"] = str(msg["_id"])
        del msg["_id"]
    return messages

@router.get("/detail/{message_id}")
def get_message_detail(message_id: str, collection: Collection = Depends(get_collection)):
    try:
        message = collection.find_one({"_id": ObjectId(message_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid message ID format")
    if message:
        message["id"] = str(message["_id"])
        del message["_id"]
        return message
    raise HTTPException(status_code=404, detail="Message not found")

@router.post("/")
def create_message(message: Message, collection: Collection = Depends(get_collection)):
    new_message = message.dict()
    new_message["stamp"] = datetime.utcnow()
    result = collection.insert_one(new_message)
    return {"id": str(result.inserted_id)}

