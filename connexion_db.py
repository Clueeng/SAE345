from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
import pymysql.cursors
import os
from dotenv import load_dotenv
import logging

load_dotenv()

def get_db():
        
    print(f'Connecting to {os.environ.get("DATABASE")}'
            f'with login {os.environ.get("LOGIN")} password {os.environ.get("PASSWORD")}'
            f'and host {os.environ.get("HOST")}')
            
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host=os.environ.get("HOST"),
            user=os.environ.get("LOGIN"),
            password=os.environ.get("PASSWORD"),
            port=os.environ.get("DB_HOST"),
            database=os.environ.get("DATABASE"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        log = logging.getLogger('test')
        log.setLevel(logging.DEBUG)
        
        log.info(f'Connecting to {os.environ.get("DATABASE")}'
              f'with login {os.environ.get("LOGIN")} password {os.environ.get("PASSWORD")}'
              f'and host {os.environ.get("HOST")}')
        activate_db_options(db)
    return db

def activate_db_options(db):
    cursor = db.cursor()
    # Vérifier et activer l'option ONLY_FULL_GROUP_BY si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'sql_mode'")
    result = cursor.fetchone()
    if result:
        modes = result['Value'].split(',')
        if 'ONLY_FULL_GROUP_BY' not in modes:
            print('MYSQL : il manque le mode ONLY_FULL_GROUP_BY')   # mettre en commentaire
            cursor.execute("SET sql_mode=(SELECT CONCAT(@@sql_mode, ',ONLY_FULL_GROUP_BY'))")
            db.commit()
        else:
            print('MYSQL : mode ONLY_FULL_GROUP_BY  ok')   # mettre en commentaire
    # Vérifier et activer l'option lower_case_table_names si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names'")
    result = cursor.fetchone()
    if result:
        if result['Value'] != '0':
            print('MYSQL : valeur de la variable globale lower_case_table_names differente de 0')   # mettre en commentaire
            cursor.execute("SET GLOBAL lower_case_table_names = 0")
            db.commit()
        else :
            print('MYSQL : variable globale lower_case_table_names=0  ok')    # mettre en commentaire
    cursor.close()
