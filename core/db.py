import os
from mysql.connector import connect, Error
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import Generator

load_dotenv()

def get_db() -> Generator:
    try:
        connection = connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        yield connection  # Yielding the connection allows it to be used as a dependency
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        if connection.is_connected():
            connection.close()
