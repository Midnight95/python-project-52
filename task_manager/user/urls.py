from django.urls import path

from task_manager.user import views

urlpatterns = [
        path(
            '',
            views.UserListView.as_view(),
            name='user_list'
            ),
        path(
            'create/',
            views.UserCreateView.as_view(),
            name='user_create'
            ),
        path(
            '<int:pk>/update/',
            views.UserUpdateView.as_view(),
            name='update_user'
            ),
        path(
            '<int:pk>/delete/',
            views.UserDeleteView.as_view(),
            name='delete_user'
            ),
        ]
