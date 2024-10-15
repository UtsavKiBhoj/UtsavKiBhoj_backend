from django.urls import path
from .views import RegisterUser, LoginUser, UpdateUser, DeleteUser, UserListView, LogoutUser, getUserByID

urlpatterns = [
    path('signup/', RegisterUser.as_view(), name='register_user'),
    path('login/', LoginUser.as_view(), name='login_user'),
    path('usersList/', UserListView.as_view(), name='user-list'),
    path('details/<int:user_id>/',getUserByID.as_view(),  name='get_user_by_id'),
    path('update/<int:pk>/', UpdateUser.as_view(), name='update_user'),
    path('delete/<int:user_id>/', DeleteUser.as_view(), name='user-delete'),
    path('logout/', LogoutUser.as_view(), name='logout_user'),
]