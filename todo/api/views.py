import os
from rest_framework import viewsets
from .serializers import TaskSerializer, CategorySerializer, UserSerializer, AttachmentSerializer
from tasks.models import Task, Category, Attachment, User
from django.shortcuts import get_object_or_404
from django.conf import settings
from .permissions import IsOwner


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSerializer

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'), user=self.request.user)
        serializer.save(task=task)

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'), user=self.request.user)
        return task.attachments

    def perform_destroy(self, instance):
        filepath = f'{settings.MEDIA_ROOT}/{instance.file.name}'
        if os.path.exists(filepath):
            os.remove(filepath)
        instance.delete()

