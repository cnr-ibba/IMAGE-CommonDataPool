from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('organism/', views.ListCreateOrganismsView.as_view(), name='organismindex'),
    path('organism/<organism_id>/', views.OrganismsDetailsView.as_view(), name='organismdetail'),
    path('specimen/', views.ListCreateSpecimensView.as_view(), name='specimenindex'),
    path('specimen/<specimen_id>/', views.SpecimensDetailsView.as_view(), name='specimendetail'),
]
