from django.db import models

class Question(models.Model):
    question = models.TextField()
    correct_answer = models.TextField()
    wrong_answers = models.TextField()

    def __str__(self):
        return self.question

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.username or f"User {self.user_id}"
    
class UserStat(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    new_users = models.IntegerField(default=0, verbose_name="Новые пользователи")
    quizzes_taken = models.IntegerField(default=0, verbose_name="Пройдено тестов")

    class Meta:
        verbose_name = "Статистика пользователя"
        verbose_name_plural = "Статистика пользователей"

    def __str__(self):
        return f"{self.date}: Пользователей - {self.new_users}, Тестов - {self.quizzes_taken}"