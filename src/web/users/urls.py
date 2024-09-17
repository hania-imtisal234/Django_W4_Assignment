from django.urls import path
from .views import CustomLoginView, CustomLogoutView, HomePageView, UserDetailView, DeleteUserView, EditUserView, CreateUserView, ManageUsersView


urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('manage/<str:user_type>/', ManageUsersView.as_view(), name='manage-users'),
    path('<str:user_type>/<int:user_id>/edit/',
         EditUserView.as_view(), name='edit'),
    path('<str:user_type>/<int:user_id>/detail/',
         UserDetailView.as_view(), name='detail'),
    path('<str:user_type>/<int:user_id>/delete/',
         DeleteUserView.as_view(), name='delete'),
    path('<str:user_type>/add/', CreateUserView.as_view(), name='add'),
]
