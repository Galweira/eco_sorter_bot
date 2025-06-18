from django.contrib import admin
from .models import Question, User, UserStat  # добавили UserStat
from import_export import resources
from import_export.admin import ImportExportModelAdmin

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'correct_answer', 'display_wrong_answers')
    search_fields = ('question', 'correct_answer')
    list_filter = ('correct_answer',)

    def display_wrong_answers(self, obj):
        return ", ".join(obj.wrong_answers.split(';'))
    display_wrong_answers.short_description = 'Неправильные ответы'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'score')
    search_fields = ('username', 'user_id')
    list_filter = ('score',)

# 👇 ВАЖНАЯ ЧАСТЬ ДЛЯ ПРОВЕРКИ ШАБЛОНА
class UserStatResource(resources.ModelResource):
    class Meta:
        model = UserStat

@admin.register(UserStat)
class UserStatAdmin(ImportExportModelAdmin):
    resource_class = UserStatResource
    list_display = ('date', 'new_users', 'quizzes_taken')
    search_fields = ('date',)
    change_list_template = 'admin/change_list.html'  # 👈 НОВЫЙ ПРАВИЛЬНЫЙ ПУТЬ

