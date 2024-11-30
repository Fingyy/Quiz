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

    def success_rate(self):
        rate = (int(self.correct_answers) / int(self.total_questions)) * 100
        return round(rate)

    def duration_format(self):
        duration = round(self.duration)
        minutes = duration // 60
        seconds = duration % 60
        if minutes > 0 and seconds > 0:
            return f"{minutes} min {seconds} sec"
        elif minutes > 0 and seconds < 1:
            return f"{minutes} min"
        elif minutes < 1 and seconds < 1:
            return f"<1 sec"
        else:
            return f"{seconds} sec"
