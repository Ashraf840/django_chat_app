from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.roomsList, name='roomsList'),
    # path('detail/', views.roomDetail, name='roomDetail'),
    path('<str:slug>/', views.roomDetail, name='roomDetail'),
]