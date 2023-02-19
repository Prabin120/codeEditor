from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('code/',views.code,name='code'),
    # path('save_file/',views.saveFile,name='save_file')
]