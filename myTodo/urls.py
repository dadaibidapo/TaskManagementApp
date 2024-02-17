from django.urls import path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, LoginPage,CustomRegistrationView
from django.contrib.auth.views import LogoutView
# upload_profile_image


urlpatterns = [
    
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', CustomRegistrationView.as_view(), name='register'),

    path('',TaskList.as_view(), name='tasks'),
    path('detail/<int:pk>/',TaskDetail.as_view(), name='detail'),
    path('create-task/',TaskCreate.as_view(), name='createTask'),
    path('update-task/<int:pk>/',TaskUpdate.as_view(), name='updateTask'),
    path('delete-task/<int:pk>/',TaskDelete.as_view(), name='deleteTask'),
]


