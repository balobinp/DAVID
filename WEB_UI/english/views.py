from django.shortcuts import render
from django.db.models import Max
from django.contrib.auth.decorators import login_required
import numpy as np
import sqlite3
import pandas as pd
from os.path import join
from datetime import date

from .models import IrregularVerbs
from .models import IrregularVerbsResults
from children_math.children_math_modules import math01_result_estimate

import david_lib

dir_david = david_lib.dir_david
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)

def collect_data_from_db_irr_verb():
    query = """SELECT * FROM V_CHILDREN_ENG_IRR_VER;"""
    con = sqlite3.connect(file_sqlite_db_path)
    con.execute(query)
    df = pd.read_sql(query, con, parse_dates=['REP_DATE'], index_col=['REP_DATE'])
    con.close()
    return df

@login_required
def english_main(request):
    try: # If the table with results is empty there wil be an error
        today = date.today()
        df = collect_data_from_db_irr_verb()
        if request.user.username:
            df = df[df.USER_NAME == request.user.username]
            today_task01, solved_tasks01 = math01_result_estimate.math_result_estimate(df, today)

            context = {'today_task01': str(today_task01), 'solved_tasks01': str(solved_tasks01),}
        else:
            context = {'today_task01': '-', 'solved_tasks01': '-',}
    except:
        if request.user.username:
            context = {'today_task01': "NOK", 'solved_tasks01': "0"}
        else:
            context = {'today_task01': '-', 'solved_tasks01': '-'}

    return render(request, 'english/english_main.html', context)

@login_required
def irregular_verbs_task(request):
    if request.method == 'GET':
        irregular_verbs_max_id = IrregularVerbs.objects.aggregate(Max('id'))['id__max']
        irregular_verbs_ids = np.random.choice(range(1, irregular_verbs_max_id + 1), 3, replace=False)
        irregular_verbs = {'irregular_verbs': IrregularVerbs.objects.filter(id__in=irregular_verbs_ids),
                           'irregular_verbs_ids': ','.join(map(str, irregular_verbs_ids))}
        context = {'irregular_verbs': irregular_verbs}
        return render(request, 'english/irregular_verbs_task.html', context)

    elif request.method == 'POST':
        user_answer01 = str(request.POST.get('user_answer01').replace(' ', '').lower())
        user_answer02 = str(request.POST.get('user_answer02').replace(' ', '').lower())
        user_answer03 = str(request.POST.get('user_answer03').replace(' ', '').lower())
        user_answer_list = [user_answer01, user_answer02, user_answer03]
        irregular_verbs_ids = request.POST.get('irregular_verbs')
        irregular_verbs_ids = sorted([int(i) for i in irregular_verbs_ids.split(',')])
        irregular_verbs_list = [IrregularVerbs.objects.get(pk=irregular_verbs_id).get_all_fields()
                                for irregular_verbs_id in irregular_verbs_ids]
        score = sum([verbs[0] == verbs[1] for verbs in zip(user_answer_list, irregular_verbs_list)])

        objs = [
            IrregularVerbsResults(
                user_id=request.user.id,
                verb_id=result[0],
                user_answer=result[1]
            )
            for result in zip(irregular_verbs_ids, user_answer_list)
        ]
        IrregularVerbsResults.objects.bulk_create(objs)

        return render(request, 'english/irregular_verbs_result.html',
                      {'score': score, 'user_answers': user_answer_list})