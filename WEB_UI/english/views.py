from django.shortcuts import render
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from .models import IrregularVerbs
import numpy as np

@login_required
def english_main(request):
    if request.user.username:
        context = {'today_task01': "OK", 'solved_tasks01': "7"}
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
        return render(request, 'english/irregular_verbs_result.html',
                      {'score': score, 'user_answers': user_answer_list})