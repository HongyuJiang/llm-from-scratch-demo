import configparser
import os

import mysql.connector
import sqlite3
from sqlalchemy import create_engine


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../', 'config.ini'))


def create_table(table_name, table_schema):
    # 创建MySQL数据库连接并将CSV数据导入
    conn = mysql.connector.connect(
        host=config['mysql']['host'],
        user=config['mysql']['user'],
        password=config['mysql']['password'],
        database=config['mysql']['database']
    )
    cursor = conn.cursor()

    # 检查表是否已经存在
    cursor.execute(f"drop table {table_name}")
    cursor.execute(table_schema)
    conn.close()


def create_mysql_engine():
    engine = create_engine(f"mysql+mysqlconnector://{config['mysql']['user']}:{config['mysql']['password']}@{config['mysql']['host']}/{config['mysql']['database']}")
    return engine


def create_sqlite_db():
    # 创建SQLite数据库并将CSV数据导入
    conn = sqlite3.connect(":memory:")
    return conn
