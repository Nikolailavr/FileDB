from django.urls import path

from .views import UploadDataView, QueryDataView, PingView, FileUploadView

urlpatterns = [
    path('upload-file/', FileUploadView.as_view(), name='file-upload'),
    path('upload-json/', UploadDataView.as_view(), name='json-upload'),
    path('get/', QueryDataView.as_view(), name='query-data'),
    path('ping/', PingView.as_view(), name='ping'),
]
