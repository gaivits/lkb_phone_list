import logging
from fastapi import APIRouter, Depends, HTTPException, Path,Query,Body
from mysql.connector import MySQLConnection
from core.db import *
from core.security import *
import pymysql
from phone_list.users_role.users_role_schemas import *
from phone_list.users_role.users_role_utils import *
from auth.auth_routes import *
import re
router = APIRouter()

@router.get("/list")
async def get_users_role_list(request:Request, db =Depends(get_db_connection), q : query_params = Depends()):
    result = await get_list(db, request,dict(q))
    if result is not None:
        return {"OK":result}

@router.get("/list/{id}")
async def get_one_users_role(request:Request, db =Depends(get_db_connection),id:int=Path(...)):
    result = await get_one_list(db, request,id)
    if result is not None:
        return {"OK":result}

@router.post("/list")
async def add_users_role(request:Request, db =Depends(get_db_connection),users_role:None|users_role_repository=users_role_repository):
    result = await add(db, request,dict(users_role))
    if result is not None:
        return {"OK":users_role}
    
@router.put("/list/{id}")
async def update_users_role(request:Request, db =Depends(get_db_connection),users_role:None|users_role_repository=users_role_repository,id :int=Path(...)):
    #return 0
    result = await edit(db, request,dict(users_role),id)
    if result is not None:
        return {"Updated":users_role}

@router.delete("/list/{id}")
async def delete_users_role(request:None|str =None, db =Depends(get_db_connection),id :int=Path(...)):
    #return 0
    result = await delete(db, request,id)
    if result is not None:
        return {"Deleted":id}