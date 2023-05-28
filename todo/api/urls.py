from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoryViewSet, UserViewSet, AttachmentViewSet
from django.urls import path, include

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(r'tasks', TaskViewSet)
v1_router.register('categories', CategoryViewSet, basename='12344')
v1_router.register('users', UserViewSet)
# v1_router.register('attachments', AttachmentViewSet)
v1_router.register(r'tasks/(?P<task_id>\d+)/attachments', AttachmentViewSet, basename='attachments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
