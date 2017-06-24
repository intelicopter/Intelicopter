from django.db import models


class Question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=500)
    question_type = models.IntegerField # 1 radio, 2 checkbox, 3 textbox, 4 number

    class Meta:
        db_table = "intelicopter_question"


class Option(models.Model):
    option_id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=500)
    
    class Meta:
        db_table = "intelicopter_option"


class Trigger(models.Model):
    trigger_id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    trigger_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    trigger_text = models.CharField(max_length=500)

    class Meta:
        db_table = "intelicopter_trigger"