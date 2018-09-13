import sqlite3
import os.path
import pytz
from os import listdir, getcwd
from IPython.core.display import Image 
from datetime import datetime, date
from pytz import timezone
import sys
import traceback #add
import io, base64 #add
import os #add
import errno #add
import numpy as np #add
import cv2 #add

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

#Create or open a database
def create_or_open_db(db_file):
    #os.path.exists(path) - returns True if path points to an existing path or open file descriptor
    db_is_new = not os.path.exists(db_file)
    #create a link to the database
    conn = sqlite3.connect(db_file) #,detect_types=sqlite3.PARSE_DECLTYPES
    if db_is_new:
        print('Creating schema main')
        conn.execute("PRAGMA foreign_keys = ON;")
        sql = '''create table if not exists PICTURES(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PICTURE BLOB,
        [timestamp] timestamp);'''
        conn.execute(sql) # shortcut for conn.cursor().execute(sql)
        sql2 = "create table if not exists CLASSES( ID_CLASS INTEGER PRIMARY KEY AUTOINCREMENT, CLASS TEXT, UNIQUE (CLASS) ON CONFLICT ABORT);" #CLASS TEXT, UNIQUE (CLASS) ON CONFLICT IGNORE
        conn.execute(sql2) # shortcut for conn.cursor().execute(sql)
        sql3 = '''create table if not exists CHILD_PICTURES( PICTURES_ID INTEGER, CLASSES_ID_CLASS INTEGER,
        CHILD_PICTURE BLOB, FOREIGN KEY(PICTURES_ID) REFERENCES PICTURES(ID) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY(CLASSES_ID_CLASS) REFERENCES CLASSES(ID_CLASS) ON UPDATE CASCADE ON DELETE CASCADE);'''
        conn.execute(sql3) # shortcut for conn.cursor().execute(sql)
    else:
        print('Schema exists main\n')
    return conn

#Insert (image) into the database table PICTURES
def insert_picture(conn, picture_file):
    try:
        #binary mode reading
        with io.BytesIO(picture_file) as input_file:
            ablob = input_file.read()
    except Exception as e:
        print('Error main:\n', traceback.format_exc())
    else:
        sql = '''INSERT INTO PICTURES
        (PICTURE, timestamp)
        VALUES(?, ?);'''
        conn.execute(sql,[sqlite3.Binary(ablob), datetime.strftime(datetime.now(pytz.timezone('Europe/Moscow')), "%d.%m.%Y %H:%M:%S")])
        conn.commit()

        #sql = "SELECT PICTURE " +\
        #"FROM PICTURES WHERE id = :id"

        #param = {'id': picture_id}
        #cursor.execute(sql, param)
        print('The image was obtained (main)\n')

#Deleting an entry for id table PICTURES
def delete_picture(conn, picture_id):
    try:

        sql = "DELETE FROM PICTURES WHERE id = :id"
        param = {'id': picture_id}

        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute(sql, param)
        conn.commit()
    
    except sqlite3.Error:
        print("Error sqlite3 delete_picture")
        return 1
    
    else:
        return 0

#Extracting the image table PICTURES
def extract_picture(cursor, picture_id): #ADD picture_file

    '''
    #ADD
    make_sure_path_exists(picture_file)
    pic = os.path.abspath(picture_file)
    #os.path.exists (path) - Returns True if path points to an existing path or open file descriptor
    if os.path.exists(pic):
        if os.path.isdir(pic):
            pic = pic + "/frame_" + str(picture_id) + ".png"
            print("Extract picture completed successfully")
        else:
            print("Directory not found")
            return 1
    else:
        print("Path incorrect")
        return 1
    '''

    try:
        #PICTURE
        sql = "SELECT PICTURE " +\
           "FROM PICTURES WHERE id = :id"
        
        param = {'id': picture_id}
        cursor.execute(sql, param)
    
    except sqlite3.Error:
        print("Error sqlite3 extract_picture")
        return 1

    else:    
        #.fetchone() method returns one record as a tuple, if there is no more record, then it returns No
        return cursor.fetchone() #DELETE

    '''
    #ADD
        record = cursor.fetchone()
        if record != None:
            ablob, *_ = record
            with open(pic, 'wb') as output_file:
                output_file.write(base64.b64decode(ablob))
        else:
            print("Error id not found")
            return 1
    '''

#Extracting the image table CHILD_PICTURES
def child_extract_picture(cursor, picture_id): #ADD picture_file_child

    '''
    #ADD
    #Create a folder if it does not exist
    make_sure_path_exists(picture_file_child)
    #Full path to picture_file_child
    pic_child = os.path.abspath(picture_file_child)
    '''

    try:
        #PICTURE
        sql = '''SELECT CHILD_PICTURES.rowid, CHILD_PICTURES.CHILD_PICTURE, CLASSES.CLASS
            FROM CHILD_PICTURES 
            INNER JOIN CLASSES
            ON CHILD_PICTURES.CLASSES_ID_CLASS = CLASSES.ID_CLASS 
            WHERE CHILD_PICTURES.PICTURES_ID = :id;'''

        param = {'id': picture_id}
        cursor.execute(sql, param)
    
    except sqlite3.Error:
        print("Error sqlite3 child_extract_picture")
        return 1

    else:
        return cursor.fetchall() #DELETE

        '''
        records = cursor.fetchall()
        if records != None:
            for record in records:
                rowid, ablob, CLASSES_ID_CLASS, *_ = record
                #os.path.exists (path) - Returns True if path points to an existing path or open file descriptor
                if os.path.exists(pic_child):
                    if os.path.isdir(pic_child):
                        el_pic_child = pic_child + "/frame_" + str(picture_id) + "(" + str(rowid) + ")" + "_class_" + str(CLASSES_ID_CLASS) + ".png"
                        nparr = np.fromstring(ablob, np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
                        cv2.imwrite(el_pic_child, img)
                        print("Extract picture_child completed successfully")
                    else:
                        print("Directory not found")
                        return 1
                else:
                    print("Path incorrect")
                    return 1
        else:
            print("Error id not found")
            return 1
        '''

#Insert (image) into the database table CHILD_PICTURES
def child_insert_picture(conn, class_name, picture_file_child):
    try:
        #binary mode reading
        with io.BytesIO(picture_file_child) as input_file:
            ablob = input_file.read()
    except Exception as e:
        
        print('Error:\n', traceback.format_exc())
    else:
        sql = '''INSERT INTO CHILD_PICTURES
        (PICTURES_ID, CLASSES_ID_CLASS, CHILD_PICTURE) 
        VALUES((SELECT ID FROM PICTURES ORDER BY ID DESC LIMIT 1), (SELECT ID_CLASS FROM CLASSES WHERE ?=CLASSES.CLASS), ?)'''
        conn.execute(sql,[class_name, sqlite3.Binary(ablob)])
        conn.commit()
        print('The image was obtained (child)\n')

#---------------Functions for working with the database------------------------

#Create or open a database
#def create_or_open_db(db_file)

#Adding a new record to table PICTURES
#Accepts the name of the database (the database is the same where this file is) and the path to the image
def add_record(db_name, picture_file):

    #Open the database
    conn = create_or_open_db(db_name)

    #Adding a new record
    insert_picture(conn, picture_file)

    #Close the database
    conn.close()
    

#Adding a new entry table CHILD_PICTURES
#Accepts the name of the database (the database is the same where this file is) and the path to the image
def add_record_child(db_name, class_name, picture_file_child):

    #Open the database
    conn = create_or_open_db(db_name)

    #Adding a new record
    child_insert_picture(conn, class_name, picture_file_child)

    #Close the database
    conn.close()

#Deleting an entry for id table PICTURES
def del_record(db_name, id_record):

    create_or_open_db(db_name)
    
    #Open the database
    conn = create_or_open_db(db_name)

    #Delete the record
    delete_picture(conn, id_record)

    #Close the database
    conn.close()

#Extraction of record on id table PICTURES
def extr_record(db_name, id_record): #ADD picture_file
    conn = create_or_open_db(db_name)
    cur = conn.cursor()
    result = extract_picture(cur, id_record) #ADD picture_file #DELETE result
    cur.close()
    conn.close()
    return result #DELETE

#Extracting the record by id table CHILD_PICTURES
def child_extr_record(db_name, id_record): #ADD picture_file_child
    conn = create_or_open_db(db_name)
    cur = conn.cursor()
    result = child_extract_picture(cur, id_record) #ADD picture_file_child #DELETE result
    cur.close()
    conn.close()
    return result #DELETE

#Delete all records from the database
def del_all(db_name):
    conn = create_or_open_db(db_name)
    conn.execute("DELETE FROM CLASSES")
    conn.execute("DELETE FROM CHILD_PICTURES")
    conn.execute("DELETE FROM PICTURES")
    conn.commit()
    conn.close()

#Adding a new entry to table CLASSES
def add_record_class(db_name, class_name):
    
    #Open the database
    conn = create_or_open_db(db_name)

    try:
        sql = '''INSERT INTO CLASSES (CLASS) VALUES(?);'''
        conn.execute(sql, [class_name])
    except Exception as e:
        print("This class already exists\n")
    else:
        conn.commit()
        print("New class successfully added\n")

    #Close the database
    conn.close()

#Sql request
def sql_exec(db_name, sql_request):

    #Open the database
    conn = create_or_open_db(db_name)
    cur = conn.cursor()

    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        cur.execute(sql_request)
        conn.commit()
    
    except sqlite3.Error:
        print("Error sqlite3 sql_exec")
        #Close the database
        cur.close()
        conn.close()
        return 1
    
    else:
        result = cur.fetchall()
        #Close the database
        cur.close()
        conn.close()
        return result

#Examples
#db = 'test.db'
#add_record(db, binary_data)
#del_all(db)
#del_record(db, 2)

#original_picture = extr_record(db, 1)
#cut_picture = child_extr_record(db, 1)
#cut_picture2 = child_extr_record(db, 2)

'''
#Exmaple sql request
db = 'test.db'
result = sql_exec(db, "SELECT rowid, PICTURES_ID, CLASSES_ID_CLASS  FROM CHILD_PICTURES")
print(result)
for k in range( len(result) ):
    print(result[k])
'''