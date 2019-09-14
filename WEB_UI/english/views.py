from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

# from django.http import HttpResponse
#
# def english_main(request):
#     return HttpResponse("<h2>HEY!</h2>")

@login_required
def english_main(request):
    if request.user.username:
        context = {'today_task01': "OK", 'solved_tasks01': "3"}
    else:
        context = {'today_task01': '-', 'solved_tasks01': '-'}
    return render(request, 'english/english_main.html', context)

@login_required
def irregular_verbs_task(request):
    if request.method == 'GET':
        irregular_verbs = [{'task_id': '1','inf':'get','past':'got','participle':'got','translation':'получать'},
                           {'task_id': '2','inf': 'take', 'past': 'took', 'participle': 'taken', 'translation': 'брать'},
                           {'task_id': '3','inf': 'go', 'past': 'went', 'participle': 'gone', 'translation': 'идти'},
                           ]
        context = {'irregular_verbs': irregular_verbs}
        return render(request, 'english/irregular_verbs_task.html', context)
    elif request.method == 'POST':
        user_answer = str(request.POST.get('user_answer').replace(' ', '').lower())
        return render(request, 'english/irregular_verbs_result.html', {'score': "5", 'user_answer': user_answer})