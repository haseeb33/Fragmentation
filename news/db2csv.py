#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 17:49:31 2019

@author: khan
"""
import sqlite3
from sqlite3 import Error
import csv

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None
 
def select_all_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM longform")
    rows = cur.fetchall()
    return rows
 
def select_task_by_priority(conn, priority):
    cur = conn.cursor()
    cur.execute("SELECT * FROM longform WHERE priority=?", (priority,))
    rows = cur.fetchall()
    return rows 
 
database = "/Users/khan/Documents/Thesis/Code/fragmentation/news_data/all-the-news.db"
 
# create a database connection
conn = create_connection(database)
with conn:
    #print("1. Query task by priority:")
    #select_task_by_priority(conn,1)
 
    print("2. Query all tasks")
    rows = select_all_tasks(conn)
    print("Done")
    with open("news.csv", "w") as f:
        writer = csv.writer(f)
        for i in rows:
            ls = []
            ls.append(i[3]); ls.append(i[5]); ls.append(i[6]); ls.append(i[4])
            writer.writerow(ls)
            
 
