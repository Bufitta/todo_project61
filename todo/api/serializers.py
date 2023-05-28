import re
from rest_framework import serializers
from tasks.models import Task, Category, Attachment, User


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = ['id', 'file']


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='api:task-detail')
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    category = serializers.HyperlinkedRelatedField(view_name='api:12344-detail', queryset=Category.objects.all())
    category_name = serializers.CharField(source='category.title')
    priority = serializers.CharField(source='get_priority_display')
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'category', 'category_name', 'priority', 'done', 'deadline', 'attachments']


class CategorySerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['title', 'tasks']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']

    def validate_email(self, value):
        print('validate_email')
        if not re.match(r'^[\w.\-]{1,25}@yandex\.(by|ru|ua|com)$', value):
            raise serializers.ValidationError('only yandex!!!')
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('user exists')
        return value

    def validate(self, data):
        print('validate')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if not any([first_name, last_name]):
            raise serializers.ValidationError('first_name or last_name is required')
        return data

