import logging
from fastapi import APIRouter, Depends, HTTPException, Path,Query,Body,Request
from mysql.connector import MySQLConnection
from core.db import *
from core.security import *
import pymysql
from phone_list.assignments.assignments_schemas import *
from phone_list.assignments.assignments_utils import *
from auth.auth_routes import *

router = APIRouter()

@router.get("/list")
async def get_assignment_list(request:Request, db =Depends(get_db_connection), q : query_params = Depends()):
    
    result = await get_list(db, request,dict(q))
    if result is not None:
        return {"OK":result}

@router.get("/list/{id}")
async def get_one_assignment(request:Request, db =Depends(get_db_connection),id:int=Path(...)):
    result = await get_one_list(db, request,id)
    if result is not None:
        return {"OK":result}

@router.post("/list")
async def add_assignment(request:Request, db =Depends(get_db_connection),assignments:None|assignments_repository=assignments_repository):
    result = await add(db, request,dict(assignments))
    if result is not None:
        return {"OK":assignments}
    
@router.put("/list/{id}")
async def update_assignment(request:Request, db =Depends(get_db_connection),assignments:None|assignments_repository=assignments_repository,id :int=Path(...)):
    #return 0
    result = await edit(db, request,dict(assignments),id)
    if result is not None:
        return {"Updated":assignments}

@router.delete("/list/{id}")
async def delete_assignment(request:Request, db =Depends(get_db_connection),id :int=Path(...)):
    #return 0
    result = await delete(db, request,id)
    if result is not None:
        return {"Deleted":id}