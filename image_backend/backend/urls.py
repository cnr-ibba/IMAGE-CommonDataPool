from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('organism/', views.ListCreateOrganismsView.as_view(),
         name='organismindex'),
    path('organism_short/', views.ListCreateOrganismsViewShort.as_view(),
         name='organismindex_short'),
    path('organism/summary/', views.get_organisms_summary,
         name='organism_summary'),
    path('organism/<organism_id>/', views.OrganismsDetailsView.as_view(),
         name='organismdetail'),
    path('specimen/', views.ListCreateSpecimensView.as_view(),
         name='specimenindex'),
    path('specimen_short/', views.ListCreateSpecimensViewShort.as_view(),
         name='specimenindex_short'),
    path('specimen/summary/', views.get_specimens_summary,
         name='specimen_summary'),
    path('specimen/<specimen_id>/', views.SpecimensDetailsView.as_view(),
         name='specimendetail')
]
