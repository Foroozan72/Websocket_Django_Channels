from django.urls import path

from echo import views

urlpatterns = [
    path('', views.index , name='index'),
    path('image/', views.echo_image , name='echo_image'),
    path('chat/<str:username>', views.join_chat , name='join_chat'),
]
