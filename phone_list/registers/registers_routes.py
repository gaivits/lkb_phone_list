import logging
from fastapi import APIRouter, Depends, HTTPException, Path,Query,Body
from mysql.connector import MySQLConnection
from core.db import *
from core.security import *
import pymysql
from phone_list.registers.registers_schemas import *
from phone_list.registers.registers_utils import *
from auth.auth_routes import *

router = APIRouter()

@router.get("/list")
async def get_regis_list(request:Request, db =Depends(get_db_connection), q : query_params = Depends()):
    
    result = await get_list(db, request,dict(q))
    if result is not None:
        return {"OK":result}

@router.get("/list/{id}")
async def get_one_regis(request:Request, db =Depends(get_db_connection),id:int=Path(...)):
    result = await get_one_list(db, request,id)
    if result is not None:
        return {"OK":result}

@router.post("/list")
async def add_regis(request:Request, db =Depends(get_db_connection),registers:None|registers_repository=registers_repository):
    result = await add(db, request,dict(registers))
    if result is not None:
        return {"OK":registers}
    
@router.put("/list/{id}")
async def update_regis(request:Request, db =Depends(get_db_connection),registers:None|registers_repository=registers_repository,id :int=Path(...)):
    #return 0
    result = await edit(db, request,dict(registers),id)
    if result is not None:
        return {"Updated":registers}

@router.delete("/list/{id}")
async def delete_regis(request:Request , db =Depends(get_db_connection),id :int=Path(...)):
    #return 0
    result = await delete(db, request,id)
    if result is not None:
        return {"Deleted":id}