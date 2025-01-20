import logging
from fastapi import APIRouter, Depends, HTTPException, Path
from mysql.connector import MySQLConnection
from core.db import *
from core.security import *
from staff.staff_schemas import *
from staff.staff_utils import *


router = APIRouter()


@router.post("/list")
async def get_staff_list(reuqest: StaffListSearchRequest, db: MySQLConnection = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        result = get_list(db, reuqest)
        return {"result_data": result}
    finally:
        if db.is_connected():
            db.close()


@router.post("/add")
async def add_staff(reuqest: AddStaffRequest, db: MySQLConnection = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        chk_dup = check_duplicate(db, reuqest.username)
        if (chk_dup):
            raise HTTPException(status_code=400, detail="The username is duplicated")

        result = add_data(db, reuqest)
        return {"result_data": result}
    finally:
        if db.is_connected():
            db.close()


@router.post("/delete/{id}")
async def delete_staff(id: int = Path(...), db: MySQLConnection = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        result = delete_data(db, id)
        return {"result_data": result}
    finally:
        if db.is_connected():
            db.close()

@router.post("/info/{id}")
async def info_staff(id: int = Path(...), db: MySQLConnection = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        result = data_info(db, id)
        return {"result_data": result}
    finally:
        if db.is_connected():
            db.close()


@router.post("/edit/{id}")
async def edit_staff(reuqest: EditStaffRequest, id: int = Path(...), db: MySQLConnection = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        chk_dup = check_duplicate_edit(db, reuqest.username, id)
        if (chk_dup):
            raise HTTPException(status_code=400, detail="The username is duplicated")

        result = edit_data(db, reuqest, id)
        return {"result_data": result}
    finally:
        if db.is_connected():
            db.close()



