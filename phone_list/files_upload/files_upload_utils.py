import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, Request,Response, Depends, HTTPException, status
from fastapi.responses import FileResponse
from datetime import datetime, timezone, timedelta
import pandas as pd

import os
import uuid
from dependencies.common import *
async def upload(db, data:Request, files):
    cursor = {}
    cookie=data.cookies.get('cookie')
    try:
        cursor = db.cursor()
        new_files = files.values.tolist()
        for i in range(len(new_files)):
            customers_firstname = new_files[i][1]
            customers_lastname = new_files[i][2]
            customers_username = new_files[i][3]
            customers_phone = new_files[i][4]
            staffs_id = new_files[i][5]
            if customers_phone:
                customers_phone = str(customers_phone)
                if customers_phone[0] != '0':
                    customers_phone = '0'+customers_phone
                else:
                    validate_phone(customers_phone)
            cursor.execute("SELECT 1 FROM staffs WHERE staffs_id = %s", (staffs_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail=f"Invalid staffs_id: {staffs_id} at row {i+1}")
            sql = """
            INSERT INTO customers (customers_firstname, customers_lastname, customers_username, customers_phone, staffs_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            val = (customers_firstname, customers_lastname, customers_username, customers_phone, staffs_id)
            cursor.execute(sql, val)
        db.commit()  # Commit AFTER the loop
        return {'message': str(len(new_files)) + " record(s) inserted"} # Correct message
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()



async def export_sql_to_excel(request : Request, db):
    cursor = {}
    cookie = request.cookies.get('cookie')
    try:
        cursor = db.cursor()
        if cookie == 'admin':
            result = cursor.execute("select * from customers")
            result = cursor.fetchall()
            my_data = []
            for i in range(len(result)):
                my_data.append({
                    'customers_id': result[i][0],
                    'customer_firstname' :result[i][1],
                    'customer_lastname': result[i][2],
                    'customer_username':result[i][3],
                    'customer_phone':result[i][4],
                    'create_at':result[i][5],
                    'update_at':result[i][6],
                })
            df = pd.DataFrame(my_data)
            unique_name = str(uuid.uuid4())
            temp_file= unique_name+".xlsx"
            file_name = "task.xlsx"
            df.to_excel(file_name, index=False)
            file_response = FileResponse(path=str(os.getcwd()),filename=file_name)
            return file_response
        else:
            result = cursor.execute("select * from customers")
            result = cursor.fetchall()
            my_data = []
            blind_num = " "
            for i in range(len(result)):
                if len(result[i][4]) < 3:
                     blind_num = result[i][4]
                else:
                     blind_num =  result[i][4][:-3] + "***"
                my_data.append({
                    'customers_id': result[i][0],
                    'customer_firstname' :result[i][1],
                    'customer_lastname': result[i][2],
                    'customer_username':result[i][3],
                    'customer_phone':blind_num,
                    'create_at':result[i][5],
                    'update_at':result[i][6],
                })
            df = pd.DataFrame(my_data)
            unique_name = str(uuid.uuid4())
            temp_file= unique_name+".xlsx"
            file_name = "task.xlsx"
            df.to_excel(file_name, index=False)
            file_response = FileResponse(path=str(os.getcwd()),filename=file_name)
            return file_response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
