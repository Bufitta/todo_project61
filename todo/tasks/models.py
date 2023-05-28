from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория "{self.title}"'


class Task(models.Model):
    LOW = 'LW'
    MIDDLE = 'MD'
    HIGH = 'HG'

    PRIORITY_CHOICES = [
        (LOW, 'Низкий'),
        (MIDDLE, 'Средний'),
        (HIGH, 'Высокий')
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks', verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Название')
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Срок исполнения')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    done = models.BooleanField(default=False, verbose_name='Сделано')
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default=LOW, verbose_name='Приоритет')

    class Meta:
        ordering = ['-deadline', 'done']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        # constraints = [models.UniqueConstraint(fields=['category', 'title'], name='unique together')]

    def __str__(self):
        return f'Задача "{self.title}"'


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='uploads/', verbose_name='Файл')

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'

    def __str__(self):
        return self.file.name
