from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('experiment/', views.ListExperimentsView.as_view(), name='experimentindex'),
    path('sample/', views.ListSamplesView.as_view(), name='sampleindex')
]