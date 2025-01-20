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
            sql = "select * from permissions"  # Default SQL
            if pages is not None and limits is not None:
                if pages > 0 and limits > 0: # Add check to avoid negative limits or pages
                    offset = (pages - 1) * limits
                    sql = f"SELECT * FROM permissions LIMIT {limits} OFFSET {offset}" # Use f-strings for cleaner formatting and to avoid potential SQL injection issues
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
            sql = "select * from permissions where permissions_id = %s "%(id)  # Default SQL
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

async def add(db,data:Request,permissions):
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
            INSERT INTO permissions ( creates ,updates,looks,deletes)
            VALUES (%s,%s,%s,%s)
            """
            result = cursor.execute(sql, (
            permissions['creates'],
            permissions['updates'],
            permissions['looks'],
            permissions['deletes'],
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

async def edit(db,data,permissions,id):
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
                select * from permissions where permissions_id = %d 
            """ % (id)
            result =cursor.execute(sql)
            if result is None:
                raise HTTPException(status_code=400, detail="Id doesn't exist") 
            sql = "update permissions set creates=%s ,updates = %s,looks=%s , deletes=%s where permissions_id=%s "
            result = cursor.execute(sql, (
            permissions['creates'],
            permissions['updates'],
            permissions['looks'],
            permissions['deletes'],
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
                return result
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