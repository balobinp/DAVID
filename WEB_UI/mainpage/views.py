from django.shortcuts import render

from os.path import join
import sqlite3
import pandas as pd

from . import math_result_estimate
import david_lib

dir_david = david_lib.dir_david
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)


# Collect the data from database

def collect_data_from_db():
    query = """SELECT * FROM V_CHILDREN_MATH_TASK01;"""
    con = sqlite3.connect(file_sqlite_db_path)
    con.execute(query)
    df = pd.read_sql(query, con, parse_dates=['REP_DATE'], index_col=['REP_DATE'])
    con.close()
    return df

def index(request):
    df = collect_data_from_db()
    if request.user.username:
        df = df[df.USER_NAME == request.user.username]
        today_task, solved_tasks = math_result_estimate.math_result_estimate(df)
        context = {'today_task': str(today_task), 'solved_tasks': str(solved_tasks)}
    else:
        context = {'today_task': '-', 'solved_tasks': '-'}
    return render(request, 'mainpage/mainpage.html', context)

