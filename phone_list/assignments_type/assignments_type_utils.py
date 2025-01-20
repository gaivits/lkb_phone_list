import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, Request, Depends, HTTPException, status
from datetime import datetime, timezone, timedelta

async def get_list(db, data:Request, q):
    cursor = {}
    cookie=data.cookies.get('cookie')
    try:
        cursor = db.cursor()
        check_my_permission=cursor.execute(""" select backend_users.username , 
        permissions.creates,permissions.updates,
        permissions.looks,
        permissions.deletes from backend_users 
        join 
        users_role on users_role.users_role_id=backend_users.users_role_id 
        join permissions on users_role.users_role_id = permissions.permissions_id where backend_users.username=%s """, (cookie,))
        check_my_permission=cursor.fetchone()
        if check_my_permission[3]==1 or check_my_permission[3]=='1' :
            pages = q.get('pages')  # Use .get() to avoid KeyError if key is missing
            limits = q.get('limits')
            sql = "select * from assignments_type"  # Default SQL
            if pages is not None and limits is not None:
                if pages > 0 and limits > 0: # Add check to avoid negative limits or pages
                    offset = (pages - 1) * limits
                    sql = f"SELECT * FROM assignments_type LIMIT {limits} OFFSET {offset}" # Use f-strings for cleaner formatting and to avoid potential SQL injection issues
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
                else:
                    raise HTTPException(status_code=400, detail="Pages and limits must be positive integers")
        else:
            raise HTTPException(status_code=400, detail="You have no rights")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

async def get_one_list(db,data:Request,id):
    cursor = {}
    cookie = data.cookies.get('cookie')
    try:
        cursor = db.cursor()
        check_my_permission=cursor.execute(""" select backend_users.username , 
        permissions.creates,permissions.updates,
        permissions.looks,
        permissions.deletes from backend_users 
        join 
        users_role on users_role.users_role_id=backend_users.users_role_id 
        join permissions on users_role.users_role_id = permissions.permissions_id where backend_users.username=%s """, (cookie,))
        check_my_permission=cursor.fetchone()
        if check_my_permission[3]==1 or check_my_permission[3]=='1' :
            sql = "select * from assignments_type where assignments_type_id = %s "%(id)  # Default SQL
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        else:
            raise HTTPException(status_code=400, detail="You have no rights")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

async def add(db,data:Request,assignments_type):
    cookie = data.cookies.get('cookie')
    cursor = {}
    try:
        cursor = db.cursor()
        check_my_permission=cursor.execute(""" select backend_users.username , 
        permissions.creates,permissions.updates,
        permissions.looks,
        permissions.deletes from backend_users 
        join 
        users_role on users_role.users_role_id=backend_users.users_role_id 
        join permissions on users_role.users_role_id = permissions.permissions_id where backend_users.username=%s """, (cookie,))
        check_my_permission=cursor.fetchone()
        if check_my_permission[1]==1 or check_my_permission[1]=='1' :
            sql = """
            INSERT INTO assignments_type ( assignments_type_name ,assignments_type_desc)
            VALUES (%s,%s)
            """
            result = cursor.execute(sql, (
            assignments_type['assignments_type_name'],
            assignments_type['assignments_type_desc']
            ))
            result = cursor.fetchone()
            return result,db.commit()
        else:
            raise HTTPException(status_code=400, detail="You have no rights")  
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

async def edit(db,data,assignments_type,id):
    cursor={}
    cookie = data.cookies.get('cookie')
    try:
        cursor = db.cursor()
        check_my_permission=cursor.execute(""" select backend_users.username , 
        permissions.creates,permissions.updates,
        permissions.looks,
        permissions.deletes from backend_users 
        join 
        users_role on users_role.users_role_id=backend_users.users_role_id 
        join permissions on users_role.users_role_id = permissions.permissions_id where backend_users.username=%s """, (cookie,))
        check_my_permission=cursor.fetchone()
        if check_my_permission[3]==1 or check_my_permission[3]=='1' :
            sql = """
                select * from assignments_type where assignments_type_id = %d
            """ % (id)
            result =cursor.execute(sql)
            if result is None:
                raise HTTPException(status_code=400, detail="Id doesn't exist") 
            sql = "update assignments_type set assignments_type_name=%s ,assignments_type_desc = %s where assignments_type_id=%s"
            result = cursor.execute(sql, (
            assignments_type['assignments_type_name'],
            assignments_type['assignments_type_desc'],
            id
            ))
            result = cursor.fetchone()
            return result,db.commit()
        else:
            raise HTTPException(status_code=400, detail="You have no rights")  
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


async def delete(db,data:Request,id):
    cookie = data.cookies.get('cookie')
    cursor={}
    try:
        cursor = db.cursor()
        check_my_permission=cursor.execute(""" select backend_users.username , 
        permissions.creates,permissions.updates,
        permissions.looks,
        permissions.deletes from backend_users 
        join 
        users_role on users_role.users_role_id=backend_users.users_role_id 
        join permissions on users_role.users_role_id = permissions.permissions_id where backend_users.username=%s """, (cookie,))
        check_my_permission=cursor.fetchone()
        if check_my_permission[4]==1 or check_my_permission[4]=='1' :
            check_id = cursor.execute("select * from assignments_type where assignments_type_id=%d"%(id))
            check_id =cursor.fetchone()
            if check_id:
                sql = 'delete from assignments_type where assignments_type_id=%d'%(id)
                result = cursor.execute(sql)
                result = cursor.fetchone()
                return result,db.commit()
            else:
                raise HTTPException(status_code=400, detail="Id doesn't exist")
        else:
            raise HTTPException(status_code=400, detail="You have no rights")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()