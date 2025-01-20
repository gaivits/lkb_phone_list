import logging
from fastapi import APIRouter, Depends, HTTPException, Path,Query,Body
from mysql.connector import MySQLConnection
from core.db import *
from core.security import *
import pymysql
from phone_list.customers.customers_schemas import *
from phone_list.customers.customers_utils import *
from auth.auth_routes import *

router = APIRouter()

@router.get("/list")
async def get_cust_list(request:Request, db =Depends(get_db_connection), q : query_params = Depends()):
    
    result = await get_list(db, request,dict(q))
    if result is not None:
        return {"OK":result}

@router.get("/list/{id}")
async def get_one_cust(request:Request, db =Depends(get_db_connection),id:int=Path(...)):
    result = await get_one_list(db, request,id)
    if result is not None:
        return {"OK":result}

@router.post("/list")
async def add_cust(request:Request, db =Depends(get_db_connection),customers:None|customers_repository=customers_repository):
    result = await add(db, request,dict(customers))
    if result is not None:
        return {"OK":customers}
    
@router.put("/list/{id}")
async def update_cust(request:Request, db =Depends(get_db_connection),customers:None|customers_repository=customers_repository,id :int=Path(...)):
    #return 0
    result = await edit(db, request,dict(customers),id)
    if result is not None:
        return {"Updated":customers}

@router.delete("/list/{id}")
async def delete_cust(request:Request , db =Depends(get_db_connection),id :int=Path(...)):
    #return 0
    result = await delete(db, request,id)
    if result is not None:
        return {"Deleted":id}