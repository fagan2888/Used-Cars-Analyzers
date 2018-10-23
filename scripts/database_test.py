#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#
## -*- coding: utf-8 -*-
#"""
#@author: Karina Bucheli

#This is a sample script that allows to get data from PostgreSQL.
#Uses psycopg2 as data driver

import psycopg2

try:
    conn = psycopg2.connect("dbname='car_analyzer' user='car_analyzer' host='142.93.190.0' password='georgetown'")
except:
    print ("Unable to connect to the database")
	
cur = conn.cursor()
cur.execute("""SELECT * from students""")
rows = cur.fetchall()
print ("\nStudents:\n")
for row in rows:
    print("   ", row[1])
