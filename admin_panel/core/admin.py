from django.contrib import admin
from .models import Question, User

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
