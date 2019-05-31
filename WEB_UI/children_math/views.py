from django.shortcuts import render
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

# def index(request):
#     return render(request,'children_math/home.html')

def index(request):
    Answer_0 = request.POST.get('Answer_0')
    Answer_1 = request.POST.get('Answer_1')
    Answer_2 = request.POST.get('Answer_2')
    Answer_3 = request.POST.get('Answer_3')
    Answer_4 = request.POST.get('Answer_4')
    pd.set_option('display.max_colwidth', -1)
    df = DataFrame(np.random.randint(1, 30, size=10).reshape((5, 2)), columns=['First', 'Second'])
    list_feedback = []
    for i in range(5):
        list_feedback.append(f'<input id="feedback-Answer_{i}" type="text" name="Answer_{i}">')
    df['Result'] = list_feedback
    df.to_html('children_math/templates/children_math/includes/math_task_01.html',
               index=True, escape=False, justify='center')
    return render(request, 'children_math/home.html')
