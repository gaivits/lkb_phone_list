import logging
from fastapi import APIRouter, Depends, HTTPException, Path,Query,Body,UploadFile,File
from mysql.connector import MySQLConnection
from core.db import *
from core.security import *
import pymysql
from phone_list.files_upload.files_upload_schemas import *
from phone_list.files_upload.files_upload_utils import *
from auth.auth_routes import *
import pandas as pd
import io
router = APIRouter()

@router.post("/import")
async def upload_file(request:Request, db =Depends(get_db_connection), ffile:UploadFile = File(...)):
    if ffile.headers['content-type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or ffile.headers['content-type']=="	application/vnd.ms-excel":
        contents = await ffile.read()
        df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
    result = await upload(db, request,df)
    if result is not None:
        return {"OK":result}

@router.get("/export")
async def export_file(request:Request,db=Depends(get_db_connection)):
    result = await export_sql_to_excel(request,db)
    if result is not None:
        return {"OK":result}
        
                

            