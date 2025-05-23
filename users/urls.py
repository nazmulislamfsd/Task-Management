from django.urls import path
from users.views import sign_up, sign_in, logOut, activate_user, admin_dashboard, assign_role, create_group, group_list

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('log-out/', logOut, name='log-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin-dashboard/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin-dashboard/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list')
]
