import logging
from fastapi import APIRouter, Depends, HTTPException, Path,Query,Body,Request
from mysql.connector import MySQLConnection
from core.db import *
from core.security import *
import pymysql
from phone_list.staffs.staffs_schemas import *
from phone_list.staffs.staffs_utils import *
from auth.auth_routes import *
import re
router = APIRouter()

@router.get("/list")
async def get_staffs_list(request:Request =Request, db =Depends(get_db_connection), q : query_params = Depends()):
    result = await get_list(db, request,dict(q))
    if result is not None:
        return {"OK":result}

@router.get("/list/{id}")
async def get_one_staffs(request:Request =Request, db =Depends(get_db_connection),id:int=Path(...)):
    result = await get_one_list(db, request,id)
    if result is not None:
        return {"OK":result}

@router.post("/list")
async def add_staffs(request:Request =Request, db =Depends(get_db_connection),staffs:None|staffs_repository=staffs_repository):
    staffs = dict(staffs)
    staffs['username'] = request.cookies.get("cookie")
    result = await add(db, request,dict(staffs))
    if result is not None:
        return {"OK":staffs}
    
@router.put("/list/{id}")
async def update_staffs(request:Request=Request, db =Depends(get_db_connection),staffs:None|staffs_repository=staffs_repository,id :int=Path(...)):
    #return 0
    staffs = dict(staffs)
    staffs['username'] = request.cookies.get("cookie")
    result = await edit(db, request,dict(staffs),id)
    if result is not None:
        return {"Updated":staffs}

@router.delete("/list/{id}")
async def delete_staffs(request:Request=Request, db =Depends(get_db_connection),id :int=Path(...)):
    #return 0
    result = await delete(db, request,id)
    if result is not None:
        return {"Deleted":id}