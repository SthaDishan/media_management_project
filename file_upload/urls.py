from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_view, name='get_view'),
    path('upload/', views.upload_file, name='upload_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete-all/', views.delete_all_file, name='delete_all_file'),
]