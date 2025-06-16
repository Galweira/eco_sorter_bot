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
