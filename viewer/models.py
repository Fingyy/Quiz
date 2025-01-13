from django.db import models


class Game(models.Model):
    nick_name = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    category_id = models.IntegerField(null=True)
    category_name = models.CharField(max_length=100, null=True)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)

    def __str__(self):
        nick_name = self.nick_name or "N/A"  # Pokud je None, použije se "N/A"
        difficulty = self.difficulty or "N/A"
        category_name = (self.category_name[:10] if self.category_name else "N/A")
        total_questions = self.total_questions or 0
        correct_answers = self.correct_answers or 0
        duration = self.duration or "N/A"

        return (f"Nick: {nick_name} - Level: {difficulty} - Cat. name: {category_name} - "
                f"No. of Q: {total_questions} - Corr-A: {correct_answers} - Time: {duration}")

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

    def capitalize_difficulty(self):
        cap_difficulty = self.difficulty.title()
        return cap_difficulty
