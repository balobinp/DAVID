from django.shortcuts import render
from pandas import DataFrame
import pandas as pd
import numpy as np

# def index(request):
#     return render(request,'children_math/home.html')

pd.set_option('display.max_colwidth', -1)

def index(request):
    df = DataFrame(np.random.randint(1, 30, size=10).reshape((5, 2)), columns=['First', 'Second'])
    list_feedback = []
    for i in range(5):
        list_feedback.append(f'<input id="feedback-Answer_{i}" type="text" name="Answer_{i}">')
    df['Your Answer'] = list_feedback
    df.to_html('children_math/templates/children_math/includes/math_01_task.html',
               index=True, escape=False, justify='center')
    return render(request, 'children_math/home.html')

# print(dict_tasks['task_01'])

def math_result(request):
    Answer_0 = request.POST.get('Answer_0')
    Answer_1 = request.POST.get('Answer_1')
    Answer_2 = request.POST.get('Answer_2')
    Answer_3 = request.POST.get('Answer_3')
    Answer_4 = request.POST.get('Answer_4')
    df_list = pd.read_html('children_math/templates/children_math/includes/math_01_task.html', index_col=0)
    df = df_list[0]
    df['Correct Answer'] = df['First'] + df['Second']
    df['Your Answer'] = [Answer_0, Answer_1, Answer_2, Answer_3, Answer_4]
    df['Your Answer'] = df['Your Answer'].replace({'': 0}).astype('int')
    df['Result'] = df.apply(lambda x: 'OK' if x['Your Answer'] == x['Correct Answer'] else 'WRONG', axis=1)
    df.to_html('children_math/templates/children_math/includes/math_01_answer.html',
               index=True, escape=False, justify='center')
    return render(request, 'children_math/math_result.html', {'score': len(df[df['Result'] == 'OK'])})
