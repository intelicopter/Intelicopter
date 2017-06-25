from django.db import models


class Meta:
    db_table = 'intelicopter'


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=500)
    question_type = models.IntegerField()  # 1 radio, 2 checkbox, 3 textbox, 4 number

    class Meta:
        db_table = "intelicopter_question"


class Option(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=500)
    
    class Meta:
        db_table = "intelicopter_option"


class Trigger(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='main_question_set')
    trigger_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='trigger_question_set')
    trigger_text = models.CharField(max_length=500)

    class Meta:
        db_table = "intelicopter_trigger"