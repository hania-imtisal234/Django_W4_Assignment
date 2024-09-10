from django.contrib import admin
from django.urls import path
from .views import login_view, logout_view, homepage_view, user_detail,delete_user,manage_users,edit_user,add_user
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomLoginView, CustomLogoutView, HomePageView, UserDetailView, DeleteUserView,  EditUserView, CreateUserView, ManageUsersView
# from .views import RegisterView


urlpatterns = [

   #path('',homepage_view, name='index'),

    path('', HomePageView.as_view(), name='index'),

    ###
    # path('login/', login_view, name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Use the class-based view here

    ###
    # path('logout/', logout_view, name='logout'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    ###
    # path('manage/<str:user_type>/',manage_users,name='manage-users'),
    path('manage/<str:user_type>/',ManageUsersView.as_view(),name='manage-users'),

    ###
    # path('<str:user_type>/<int:user_id>/edit/',edit_user,name='edit'),
    path('<str:user_type>/<int:user_id>/edit/',EditUserView.as_view(),name='edit'),

    ###
    # path('<str:user_type>/<int:user_id>/detail/',user_detail,name='detail'),
    path('<str:user_type>/<int:user_id>/detail/',UserDetailView.as_view(),name='detail'),

    ###
    # path('<str:user_type>/<int:user_id>/delete',delete_user,name='delete'),
    path('<str:user_type>/<int:user_id>/delete',DeleteUserView.as_view(),name='delete'),

    ####
    # path('<str:user_type>/add',add_user,name='add')
    path('<str:user_type>/add',CreateUserView.as_view(),name='add')
]
