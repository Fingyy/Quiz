from django.db import models


class Game(models.Model):
    nick_name = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return (f"{self.nick_name} - {self.difficulty} - {self.category} - {self.total_questions} - "
                f"{self.correct_answers} - {self.duration}")

