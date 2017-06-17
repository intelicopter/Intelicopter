from django.db import models


class Question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=500)
    text = models.CharField(max_length=20)
    rank = models.IntegerField(default=0)

    class Meta:
        db_table = "intelicopter_question"


class Option(models.Model):
    option_id = models.IntegerField(primary_key=True)
    option_text = models.CharField(max_length=500)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        db_table = "intelicopter_option"


class Trigger(models.Model):
    trigger_id = models.IntegerField(primary_key=True)
    trigger_text = models.CharField(max_length=500)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        db_table = "intelicopter_trigger"