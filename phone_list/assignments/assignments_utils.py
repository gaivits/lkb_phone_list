import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, Request, Depends, HTTPException, status,Cookie
from datetime import datetime, timezone, timedelta

async def get_list(db, data:Request, q):
      # Initialize cursor outside the try block
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
            sql = "select * from assignments"  # Default SQL
            if pages is not None and limits is not None:
                if pages > 0 and limits > 0: # Add check to avoid negative limits or pages
                    offset = (pages - 1) * limits
                    sql = f"SELECT * FROM assignments LIMIT {limits} OFFSET {offset}" # Use f-strings for cleaner formatting and to avoid potential SQL injection issues
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

async def get_one_list(db, data:Request, id):
      # Initialize cursor outside the try block
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
            # allow_fk = None
            # fk_sql = "select permissions_id from permissions"
            # check_fk = cursor.execute(fk_sql)
            # check_fk = cursor.fetchone()
            # sql = str("select * from staffs where staffs_id = %d" %(id) )
            # result = cursor.execute(sql)
            # result = cursor.fetchone()
            # return result
            
            sql = "select * from assignments where assignments_id = %d" % (id)  # Default SQL
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

async def add(db,data,assignments):
    cursor = {}
    cookie = data.cookies.get('cookie')
    try:
        #########One2One#######
        cursor = db.cursor()
        fk_1 = "select assignments_type_id from assignments_type"
        check_fk1 = cursor.execute(fk_1)
        check_fk1 = cursor.fetchone()
        assignment_type_fk = 0
        if assignments['assignments_type_id'] in check_fk1:
            assignment_type_fk = assignments['assignments_type_id']
        else:
            raise HTTPException(status_code=400, detail="Foreign key doesn't exist")
        #########End One2One#######

        ##########Many2Many########
        allow_many2many_fk = []
        cursor = db.cursor()
        fk_sql = "select staffs_id from staffs"
        check_fk = cursor.execute(fk_sql)
        check_fk = cursor.fetchall()
        allow_fk = ''
        assignments['assignments_member']=sorted(assignments['assignments_member'])
        for outc in range(len(check_fk)):
            if assignments['assignments_member'][outc] in check_fk[outc]:
                allow_many2many_fk.append(assignments['assignments_member'])
                for inc in allow_many2many_fk[outc]:
                    allow_fk =','.join( str(allow_fk)+str(inc) )
                break
            else:
                raise HTTPException(status_code=400, detail="At least one staffs_id doesn't exist (mis-match)")
            
         ##########ENDMany2Many########
        
        check_my_permission=cursor.execute(""" select backend_users.username , 
        permissions.creates,permissions.updates,
        permissions.looks,
        permissions.deletes from backend_users 
        join 
        users_role on users_role.users_role_id=backend_users.users_role_id 
        join permissions on users_role.users_role_id = permissions.permissions_id where backend_users.username=%s """, (cookie,))
        check_my_permission=cursor.fetchone()
        if check_my_permission[1]==1 or check_my_permission[1]=='1' :
            # allow_fk = None
            # fk_sql = "select permissions_id from permissions"
            # check_fk = cursor.execute(fk_sql)
            # check_fk = cursor.fetchone()
            # sql = str("select * from staffs where staffs_id = %d" %(id) )
            # result = cursor.execute(sql)
            # result = cursor.fetchone()
            # return result
            
            sql = """
            INSERT INTO assignments (assignments_type_id, assignments_name,assignments_member)
            VALUES (%s, %s, %s)
            """
            result = cursor.execute(sql, (
            assignment_type_fk,
            assignments['assignments_name'],
            allow_fk
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

async def edit(db,data,assignments,id):
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
            fk_1 = "select assignments_type_id from assignments_type"
            check_fk1 = cursor.execute(fk_1)
            check_fk1 = cursor.fetchone()
            assignment_type_fk = 0
            if assignments['assignments_type_id'] in check_fk1:
                assignment_type_fk = assignments['assignments_type_id']
            else:
                raise HTTPException(status_code=400, detail="Foreign key doesn't exist")
            allow_many2many_fk = []
            cursor = db.cursor()
            fk_sql = "select staffs_id from staffs"
            check_fk = cursor.execute(fk_sql)
            check_fk = cursor.fetchall()
            allow_fk = ''
            assignments['assignments_member']=sorted(assignments['assignments_member'])
            for outc in range(len(check_fk)):
                if assignments['assignments_member'][outc] in check_fk[outc]:
                    allow_many2many_fk.append(assignments['assignments_member'])
                    for inc in allow_many2many_fk[outc]:
                        allow_fk =','.join( str(allow_fk)+str(inc) )
                    break
                else:
                    raise HTTPException(status_code=400, detail="At least one staffs_id doesn't exist (mis-match)")
            sql = """ update assignments 
            set 
            assignments_type_id = %s,
            assignments_name = %s,
            assignments_member = %s
            where assignments_id=%s """
            result = cursor.execute(sql, (
                assignment_type_fk,
                assignments['assignments_name'],
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
        join permissions on users_role.users_role_id = permissions.permissions_id where backend_users.username=%s """, (cookie,))
        check_my_permission=cursor.fetchone()
        if check_my_permission[4]=='1' or check_my_permission[4]==1:
            sql = "select * from assignments where assignments_id = %s"% (id)
            checks = cursor.execute(sql)
            checks = cursor.fetchone()
            if checks is None:
                raise HTTPException(status_code=400, detail="Id doesn't exist") 
            sql = "delete from assignments where assignments_id=%s"%(id)
            result = cursor.execute(sql)
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