from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index', views.index),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^taskCenter_admin', views.FilteredTaskListView.as_view()),
    url(r'^taskCenter', views.taskCenter),
    url(r'^autoAnalyzeFiles', views.autoAnalyzeFiles),
    url(r'^reportHandle', views.FilteredCrashFileListView.as_view()),
    url(r'^userManagement', views.FilteredDeveloperListView.as_view()),
    url(r'^userCenter', views.userCenter),
    url(r'^createUser', views.createUser),
    url(r'^updatePassword', views.updatePassword),
    path("developer/<int:pk>/", views.developer_detail, name="developer_detail"),
    path("task/<int:pk>/", views.task_detail, name="task_detail"),
    path("crashFile/<int:pk>/", views.crashFile_detail, name="crashFile_detail"),
    url(r'^getCrashFiles', views.getCrashFiles),
    url(r'^createTask', views.createTask),
    url(r'^createDepartment', views.createDepartment),
]