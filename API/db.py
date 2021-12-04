import os
import pymysql
from flask import jsonify

# Create database environment variables
# db_user = os.environ.get('CLOUD_SQL_USERNAME')
# db_password = os.environ.get('CLOUD_SQL_PASSWORD')
# db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
# db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

db_user = 'prembhanderi'
db_password = 'justguess'
db_name = 'mydatabase'
db_connection_name = 'ece-461-pyapi:us-east1:project2-mysql-database'


def open_connection():
    cnx = None
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

    return cnx


def run_select_query(query):
    conn = open_connection()

    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            current_msg = result[0]
        else:
            return 'No response'

    conn.close()

    return current_msg


def run_update_query(query):
    conn = open_connection()

    with conn.cursor() as cursor:
        cursor.execute(query)
        conn.commit()
        result = cursor.fetchall()

        conn.close()

        if result:
            current_msg = result[0]
        else:
            return 'No response'


def run_delete_query(query):
    conn = open_connection()

    with conn.cursor() as cursor:
        cursor.execute(query)
        conn.commit()
        result = cursor.fetchall()

        conn.close()

        if result:
            current_msg = result[0]
        else:
            return 'No response'
