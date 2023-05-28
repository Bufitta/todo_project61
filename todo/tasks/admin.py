from django.contrib import admin
from .models import Category, Task, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'user', 'priority', 'deadline', 'done', 'description')
    search_fields = ('title',)
    list_filter = ('done', 'deadline', 'category', 'priority')
    empty_value_display = '------'
    inlines = [AttachmentInline]


admin.site.register(Task, TaskAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
