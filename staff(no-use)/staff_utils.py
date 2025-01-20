import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, Request, Depends, HTTPException, status
from staff.staff_schemas import *
from staff.staff_models import *
from datetime import datetime, timezone, timedelta


def get_list(db, data):
    cursor = db.cursor(dictionary=True)
    try:
        conditions = []
        params = []

        if data.username and data.username != '':
            conditions.append("username LIKE %s")
            params.append(f"%{data.username}%")

        if data.full_name and data.full_name != '':
            conditions.append("full_name LIKE %s")
            params.append(f"%{data.full_name}%")

        if data.status and data.status != '':
            conditions.append("disabled = %s")
            params.append(data.status)

        # Start SQL query for counting total records
        count_sql = "SELECT COUNT(*) as total FROM backend_users"
        if conditions:
            count_sql += " WHERE " + " AND ".join(conditions)

        cursor.execute(count_sql, params)
        total_count_result = cursor.fetchone()
        total_count = total_count_result['total'] if total_count_result else 0

        # เริ่มต้นคำสั่ง SQL
        sql = "SELECT * FROM backend_users"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        # Add ORDER BY clause if columns and values are specified
        if data.orderby_col and data.orderby_val:
            sql += f" ORDER BY {data.orderby_col} {data.orderby_val}"

        # Add pagination
        page = data.page if data.page else 1
        page_size = data.page_size if data.page_size else 10
        offset = (page - 1) * page_size
        sql += f" LIMIT %s OFFSET %s"
        params.extend([page_size, offset])

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            list_data = []
            for row in rows:
                if 'create_at' in row and isinstance(row['create_at'], datetime):
                    row['create_at'] = row['create_at'].isoformat()
                list_data.append(StaffListInTable(**row))
            return {
                'total_count': total_count,
                'list_data': list_data
            }
        return {
            'total_count': total_count,
            'list_data': []
        }
    except Error as e:
        print(f"Error while fetching data from MySQL: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()


def check_duplicate(db, username: str):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM backend_users WHERE username=%s", (username, ))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False
    except Error as e:
        print(f"Error while fetching data from MySQL: {e}")
        raise HTTPException(status_code=400, detail=str(e))


def add_data(db, data):
    cursor = db.cursor(dictionary=True)
    try:
        insert_query = """INSERT INTO backend_users (username, pwd, full_name, disabled, create_at) VALUES (%s, %s, %s, %s, %s)"""
        query_value = (data.username, data.pwd, data.full_name, data.disabled, data.create_at)
        cursor.execute(insert_query, query_value)
        db.commit()
        if cursor.rowcount == 1:
            return "Data saved successfully"
        else:
            raise HTTPException(status_code=400, detail="Data not saved")
    except Error as e:
        db.rollback()
        print(f"Failed to insert record into MySQL table: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()


def delete_data(db, id: int):
    cursor = db.cursor(dictionary=True)
    try:
        delete_query = """DELETE FROM backend_users WHERE id = %s"""
        values = (id,)
        cursor.execute(delete_query, values)
        db.commit()
        return "Data deleted successfully"
    except Error as e:
        print(f"Error while fetching data from MySQL: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()


def data_info(db, id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM backend_users WHERE id = %s", (id, ))
        row = cursor.fetchone()
        cursor.close()
        if row:
            # Ensure datetime fields are correctly formatted if necessary
            if 'create_at' in row and isinstance(row['create_at'], datetime):
                # Convert datetime to ISO format string
                row['create_at'] = row['create_at'].isoformat()

            return StaffInfo(**row)
        return None
    except Error as e:
        print(f"Error while fetching data from MySQL: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()


def check_duplicate_edit(db, username: str, id: int):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM backend_users WHERE username=%s AND id !=%s", (username, id))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False
    except Error as e:
        print(f"Error while fetching data from MySQL: {e}")
        raise HTTPException(status_code=400, detail=str(e))


def edit_data(db, data, id: int):
    cursor = db.cursor(dictionary=True)
    try:
        update_query = """
        UPDATE backend_users
        SET username = %s,
            pwd = %s,
            full_name = %s,
            disabled = %s,
            update_at = %s
        WHERE id = %s
        """
        values_query = (data.username, data.pwd, data.full_name, data.disabled, data.update_at, id)

        cursor.execute(update_query, values_query)
        db.commit()

        return "Update Data successfully"
    except Error as e:
        db.rollback()
        print(f"Failed to update record in MySQL table: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
