from django.urls import path

from . import views

app_name = 'backend'


species2commonnames_list = views.SpeciesToCommonNameViewSet.as_view({
    'get': 'list'
})

dadislink_list = views.DADISLinkViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

dadislink_detail = views.DADISLinkViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

etag_list = views.EtagViewSet.as_view({
    'get': 'list',
})

etag_detail = views.EtagViewSet.as_view({
    'get': 'retrieve',
})

geoorganism_list = views.GeoOrganismViewSet.as_view({
    'get': 'list',
})

geoorganism_detail = views.GeoOrganismViewSet.as_view({
    'get': 'retrieve',
})

geospecimen_list = views.GeoSpecimenViewSet.as_view({
    'get': 'list',
})

geospecimen_detail = views.GeoSpecimenViewSet.as_view({
    'get': 'retrieve',
})


urlpatterns = [
    path('organism/', views.ListOrganismsView.as_view(),
         name='organismindex'),
    path('organism_short/', views.ListOrganismsViewShort.as_view(),
         name='organismindex_short'),
    path('organism/summary/', views.get_organisms_summary,
         name='organism_summary'),
    path('organism/graphical_summary/', views.get_organisms_graphical_summary,
         name='organism_graphical_summary'),

    path('organism.geojson/', geoorganism_list, name='geoorganism_list'),
    path('organism.geojson/<str:data_source_id>/',
         geoorganism_detail,
         name='geoorganism_detail'),

    path('organism/download/', views.download_organism_data,
         name='organism_download'),
    path('organism/<data_source_id>/', views.OrganismsDetailsView.as_view(),
         name='organismdetail'),
    path('specimen/', views.ListSpecimensView.as_view(),
         name='specimenindex'),
    path('specimen_short/', views.ListSpecimensViewShort.as_view(),
         name='specimenindex_short'),
    path('specimen/summary/', views.get_specimens_summary,
         name='specimen_summary'),
    path('specimen/graphical_summary/', views.get_specimens_graphical_summary,
         name='specimens_graphical_summary'),

    path('specimen.geojson/', geospecimen_list, name='geospecimen_list'),
    path('specimen.geojson/<str:data_source_id>/',
         geospecimen_detail,
         name='geospecimen_detail'),

    path('specimen/download/', views.download_specimen_data,
         name='specimen_download'),
    path('specimen/<data_source_id>/', views.SpecimensDetailsView.as_view(),
         name='specimendetail'),
    path('file/', views.ListCreateFilesView.as_view(), name='fileindex'),
    path('file/download/', views.download_file_data, name='file_download'),
    path('file/<specimen_id>/', views.FilesDetailsView.as_view(),
         name='filedetail'),
    path('species/', species2commonnames_list, name='species'),
    path('dadis_link/', dadislink_list, name='dadis_link'),
    path('dadis_link/<int:pk>/', dadislink_detail, name='dadis_link-detail'),
    path('etag/', etag_list, name='etag-list'),
    path('etag/<str:data_source_id>/', etag_detail, name='etag-detail'),
]
