from django.urls import path

from crisisManagementAssistant import views as CMA_views


urlpatterns = [

    path("", CMA_views.view_all_files, name="view_all_files"),

    path("upload_file/", CMA_views.upload_file, name="upload_file"),

    path('view/<slug:slug>/', CMA_views.view_file, name='view_file'),

    path('download/<int:file_id>/', CMA_views.download_file, name='download_file'),

    path('delete/<int:file_id>/', CMA_views.delete_file, name='delete_file'),

    path('manage/', CMA_views.manage, name='manage'),

    path('manage/add/', CMA_views.add_to_group, name='add_to_group'),

    path('manage/remove/', CMA_views.remove_from_group, name='remove_from_group'),

    path('manage/leave/', CMA_views.leave_group, name='leave_group'),

    path('manage/delete/', CMA_views.delete_group, name='delete_group'),

    path('manage/new/', CMA_views.new_group, name='new_group'),

    path("chat/", CMA_views.view_all_chats, name="view_all_chats"),

    path('chat/view/<slug:slug>/', CMA_views.view_chat, name='view_chat'),

    path("chat/new", CMA_views.new_chat, name="new_chat"),

    path('chat/delete/<slug:slug>/', CMA_views.delete_chat, name='delete_chat'),

    path('chat/regencontext/<slug:slug>/', CMA_views.regen_context_chat, name='regen_context_chat'),
]


