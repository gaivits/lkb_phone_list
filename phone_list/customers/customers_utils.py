import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, Request, Depends, HTTPException, status
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
            sql = "select * from customers"  # Default SQL
            if pages is not None and limits is not None:
                if pages > 0 and limits > 0: # Add check to avoid negative limits or pages
                    offset = (pages - 1) * limits
                    sql = f"SELECT * FROM customers LIMIT {limits} OFFSET {offset}" # Use f-strings for cleaner formatting and to avoid potential SQL injection issues
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
            sql = "select * from customers where customers_id = %s "%(id)  # Default SQL
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

async def add(db,data:Request,customers):
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
            allow_many2many_fk = []
            fk_sql = "select staffs_id from staffs"
            check_fk = cursor.execute(fk_sql)
            check_fk = cursor.fetchall()
            allow_fk = ''
            customers['staffs_id']=sorted(customers['staffs_id'])
            for outc in range(len(check_fk)):
                if customers['staffs_id'][outc] in check_fk[0]:
                    allow_many2many_fk.append(customers['staffs_id'])
                    for inc in allow_many2many_fk[outc]:
                        allow_fk =','.join( str(allow_fk)+str(inc) )
                    break
                else:
                    raise HTTPException(status_code=400, detail="At least one staffs_id doesn't exist (mis-match)")
            
            sql = """
            INSERT INTO customers (customers_firstname, customers_lastname, customers_username, customers_phone, staffs_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            result = cursor.execute(sql, (
            customers['customers_firstname'],
            customers['customers_lastname'],
            customers['customers_username'],
            customers['customers_phone'],
            allow_fk
            ))
            result = cursor.fetchone()
            return result,db.commit()
        else:
            raise HTTPException(status_code=400, detail=f"You have no right")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

async def edit(db,data:Request,customers,id):
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
        if check_my_permission[2]==1 or check_my_permission[2]=='1' :
            allow_many2many_fk = []
            fk_sql = "select staffs_id from staffs"
            check_fk = cursor.execute(fk_sql)
            check_fk = cursor.fetchall()
            allow_fk = ''
            customers['staffs_id']=sorted(customers['staffs_id'])
            for outc in range(len(check_fk)):
                if customers['staffs_id'][outc] in check_fk[0]:
                    allow_many2many_fk.append(customers['staffs_id'])
                    for inc in allow_many2many_fk[outc]:
                        allow_fk =','.join( str(allow_fk)+str(inc) )
                    break
                else:
                    raise HTTPException(status_code=400, detail="At least one staffs_id doesn't exist (mis-match)")
            
            sql = """
            INSERT INTO customers (customers_firstname, customers_lastname, customers_username, customers_phone, staffs_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            result = cursor.execute(sql, (
            customers['customers_firstname'],
            customers['customers_lastname'],
            customers['customers_username'],
            customers['customers_phone'],
            allow_fk
            ))
            result = cursor.fetchone()
            return result,db.commit()
        else:
            raise HTTPException(status_code=400, detail=f"You have no right")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    

async def delete(db,data:Request,id):
    cookie = data.request.get('cookie')
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
            check_id = cursor.execute("select * from customers where customers_id=%d"%(id))
            check_id =cursor.fetchone()
            if check_id is not None:
                sql = 'delete from customers where customers_id=%d'%(id)
            else:
                raise HTTPException(status_code=400, detail="Id doesn't exist")
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