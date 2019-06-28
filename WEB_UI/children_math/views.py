from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pandas import DataFrame
import numpy as np
from .models import Task01
from .models import Task02
from .models import Contest01

from os.path import join
import sqlite3
import pandas as pd

from .children_math_modules import math_result_estimate
import david_lib

dir_david = david_lib.dir_david
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)

# Collect the data from database

def collect_data_from_db_task01():
    query = """SELECT * FROM V_CHILDREN_MATH_TASK01;"""
    con = sqlite3.connect(file_sqlite_db_path)
    con.execute(query)
    df = pd.read_sql(query, con, parse_dates=['REP_DATE'], index_col=['REP_DATE'])
    con.close()
    return df

pd.set_option('display.max_colwidth', -1)

@login_required
def children_math_main(request):
    df = collect_data_from_db_task01()
    if request.user.username:
        df = df[df.USER_NAME == request.user.username]
        today_task, solved_tasks = math_result_estimate.math_result_estimate(df)
        context = {'today_task': str(today_task), 'solved_tasks': str(solved_tasks)}
    else:
        context = {'today_task': '-', 'solved_tasks': '-'}
    return render(request, 'children_math/children_math_main.html', context)

@login_required
def children_math_01_task(request):
    df = DataFrame(np.random.randint(1, 30, size=10).reshape((5, 2)), columns=['First', 'Second'])
    df['Sign'] = np.random.choice(['-', '+'], 5)
    list_feedback = []
    for i in range(5):
        list_feedback.append(f'<input class="form-control" id="feedback-Answer_{i}" type="text" name="Answer_{i}">')
    df['Your Answer'] = list_feedback
    df.index.name = '#'
    df.reset_index(inplace=True)
    df[['#', 'First', 'Sign', 'Second', 'Your Answer']].to_html(
        f'children_math/templates/children_math/includes/{request.user.username}_math_01_task.html',
        index=False, escape=False, justify='center', classes="table table-striped")
    return render(request, 'children_math/children_math_01_task.html')

@login_required
def children_math_01_result(request):
    Answer_0 = request.POST.get('Answer_0')
    Answer_1 = request.POST.get('Answer_1')
    Answer_2 = request.POST.get('Answer_2')
    Answer_3 = request.POST.get('Answer_3')
    Answer_4 = request.POST.get('Answer_4')
    df_list = pd.read_html(
        f'children_math/templates/children_math/includes/{request.user.username}_math_01_task.html', index_col=0)
    df = df_list[0]
    df['Correct Answer'] = df.apply(lambda x:
                                    x['First'] + x['Second'] if x['Sign'] == '+' else x['First'] - x['Second'], axis=1)
    df['Your Answer'] = [Answer_0, Answer_1, Answer_2, Answer_3, Answer_4]
    df['Your Answer'] = df['Your Answer'].replace({'': 0}).astype('int')

    # for result in df[['First', 'Second', 'Sign', 'Your Answer']].values:
    #     task_01 = Task01(user_id=request.user.id, first=result[0], second=result[1], sign=result[2], user_answer=result[3])
    #     task_01.save()

    objs = [
        Task01(
            user_id=request.user.id,
            first=result[0],
            second=result[1],
            sign=result[2],
            user_answer=result[3]
        )
        for result in df[['First', 'Second', 'Sign', 'Your Answer']].values
    ]
    Task01.objects.bulk_create(objs)

    df['Result'] = df.apply(lambda x: 'OK' if x['Your Answer'] == x['Correct Answer'] else 'WRONG', axis=1)
    df.reset_index(inplace=True)
    df.to_html('children_math/templates/children_math/includes/math_01_answer.html',
               index=False, escape=False, justify='center', classes="table table-striped")
    return render(request, 'children_math/children_math_01_result.html', {'score': len(df[df['Result'] == 'OK'])})

contest01_task_id = 2

@login_required
def children_math_02_task(request):
    contest_task = Contest01.objects.get(id=contest01_task_id).task_description
    context = {'contest_task': contest_task}
    return render(request, 'children_math/children_math_02_task.html', context)

@login_required
def children_math_02_result(request):
    user_answer = str(request.POST.get('user_answer').strip())
    contest_answer = str(Contest01.objects.get(id=contest01_task_id).answer)
    if user_answer == contest_answer:
        user_result = 1
    else:
        user_result = 0
    task_02 = Task02(user_id=request.user.id, contest01_task_id=contest01_task_id, user_answer=user_answer)
    task_02.save()
    context = {'user_answer': user_answer, 'contest_answer': contest_answer, 'user_result': user_result}
    return render(request, 'children_math/children_math_02_result.html', context)