from django.urls import path
from crisisManagementAssistant import views as CMA_views

urlpatterns = [
    path("", CMA_views.home_page, name="home_page"),
    path('download/<int:file_id>/', CMA_views.download_file, name='download_file'),
]
