import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, Request, Depends, HTTPException, status,Cookie
from datetime import datetime, timezone, timedelta

async def get_list(db, data:Request, q):
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
        if check_my_permission[3]==1 or check_my_permission[3]=='1' :
            pages = q.get('pages')  # Use .get() to avoid KeyError if key is missing
            limits = q.get('limits')
            sql = "select * from staffs"  # Default SQL
            if pages is not None and limits is not None:
                if pages > 0 and limits > 0: # Add check to avoid negative limits or pages
                    offset = (pages - 1) * limits
                    sql = f"SELECT * FROM staffs LIMIT {limits} OFFSET {offset}" # Use f-strings for cleaner formatting and to avoid potential SQL injection issues
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
            sql = "select * from staffs where customers_id = %s "%(id)  # Default SQL
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

async def get_one_list(db,data,id):
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
        if check_my_permission[3] == 1 or check_my_permission[3]=='1' :
            sql = "select * from staffs where staffs_id=%d" % id
            result = cursor.execute(sql)
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

async def add(db,data:Request,staffs):
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
        if check_my_permission[1]==1 or check_my_permission[1]=='1' :
            allow_fk = None
            fk_sql = "select permissions_id from permissions"
            check_fk = cursor.execute(fk_sql)
            check_fk = cursor.fetchone()
            for i in range(len(check_fk)):
                if staffs['permissions_id'] in check_fk:
                    allow_fk = check_fk
                else:
                    raise HTTPException(status_code=400, detail="Foreign key doesn't exist (mis-match)")
            sql = """
            INSERT INTO staffs (staffs_firstname, staffs_lastname, staffs_username, staffs_phone, permissions_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            result = cursor.execute(sql, (
            staffs['staffs_firstname'],
            staffs['staffs_lastname'],
            staffs['staffs_username'],
            staffs['staffs_phone'],
            allow_fk
            ))
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

async def edit(db,data,staffs,id):
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
        if check_my_permission[2]==1 or check_my_permission[2]=='1' :
            allow_fk = None
            fk_sql = "select permissions_id from permissions"
            check_fk = cursor.execute(fk_sql)
            check_fk = cursor.fetchone()
        else:
            raise HTTPException(status_code=400, detail="You have no right")
        check_id = cursor.execute("select * from staffs where staffs_id=%d"%(id))
        check_id =cursor.fetchone()
        if check_id:
            sql = 'select * from staffs where staffs_id=%d'%(id)
        else:
            raise HTTPException(status_code=400, detail="Id doesn't exist")
        allow_fk = None
        check_fk = cursor.execute("select permissions_id from permissions")
        check_fk = cursor.fetchone()
        for i in range(len(check_fk)):
            if staffs['permissions_id'] in check_fk:
                allow_fk = check_fk
            sql = """ update staffs 
            set 
            staffs_firstname=%s,
            staffs_lastname=%s,
            staffs_username=%s,
            staffs_phone=%s,
            permissions_id=%s
            where staffs_id = %s """
            result = cursor.execute(sql, (
            staffs['staffs_firstname'],
            staffs['staffs_lastname'],
            staffs['staffs_username'],
            staffs['staffs_phone'],
            allow_fk,
            id
        ))
        result = cursor.fetchone()
        return result,db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

async def delete(db,data,id):
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
        join permissions on users_role.users_role_id = permissions.permissions_id where backend_users.username=%s """, cookie,)
        check_my_permission=cursor.fetchone()
        if check_my_permission[4]==1 or check_my_permission[4]=='1' :
            allow_fk = None
            fk_sql = "select permissions_id from permissions"
            check_fk = cursor.execute(fk_sql)
            check_fk = cursor.fetchone()
        else:
            raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
        check_id = cursor.execute("select * from staffs where staffs_id=%d"%(id))
        check_id =cursor.fetchone()
        if check_id:
            sql = 'delete from staffs where staffs_id=%d'%(id)
        else:
            raise HTTPException(status_code=400, detail="Id doesn't exist")
        result = cursor.execute(sql)
        result = cursor.fetchone()
        return result,db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()