from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('organism/', views.ListOrganismsView.as_view(), name='organismindex'),
    path('specimen/', views.ListSpecimensView.as_view(), name='specimenindex')
]