from django.contrib import admin
from django.urls import path
from .views import login_view, logout_view, homepage_view, user_detail,delete_user,manage_users,edit_user,add_user
urlpatterns = [
    path('',homepage_view, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('manage/<str:user_type>/',manage_users,name='manage-users'),
    path('<str:user_type>/<int:user_id>/edit/',edit_user,name='edit'),
    path('<str:user_type>/<int:user_id>/detail/',user_detail,name='detail'),
    path('<str:user_type>/<int:user_id>/delete',delete_user,name='delete'),
    path('<str:user_type>/add',add_user,name='add')
]
