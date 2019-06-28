"""WEB_UI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.children_math_main, name='children_math_main'),
	path('children_math_01_task', views.children_math_01_task, name='children_math_01_task'),
    path('children_math_01_result', views.children_math_01_result, name='children_math_01_result'),
    path('children_math_02_task', views.children_math_02_task, name='children_math_02_task'),
    path('children_math_02_result', views.children_math_02_result, name='children_math_02_result'),
]
