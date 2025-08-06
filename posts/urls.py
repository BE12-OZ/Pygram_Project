from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/update/', views.post_update, name='post_update'),
    path('tag/<str:tag_name>/', views.post_list, name='post_list_by_tag'),
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('<int:pk>/toggle_like/', views.toggle_like, name='toggle_like'),
]
