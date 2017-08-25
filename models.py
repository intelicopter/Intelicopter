from django.db import models


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=500)
    question_type = models.IntegerField()  # 1 radio, 2 checkbox, 3 textbox, 4 number

    def __str__(self):
        return str(self.id) + ") " + self.text
    class Meta:
        app_label = 'intelicopter'


class Option(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=500)

    class Meta:
        app_label = 'intelicopter'


class Trigger(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='main_question_set')
    trigger_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='trigger_question_set')
    trigger_text = models.CharField(max_length=500)
    trigger_range = models.IntegerField(default=None, null=True)

    class Meta:
        app_label = 'intelicopter'


class Group(models.Model):
    # A group has multiple activities. An activity belongs to one group only.

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, default="")
    address = models.CharField(max_length=400, default="")
    postal_code = models.CharField(max_length=15, default="")
    contact_name = models.CharField(max_length=50, default="")
    contact_number = models.CharField(max_length=50, default="")
    contact_email = models.CharField(max_length=50, default="")

    class Meta:
        app_label = 'intelicopter'


class Activity(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, default="")
    address = models.CharField(max_length=400, default="")
    postal_code = models.CharField(max_length=15, default="")
    contact_name = models.CharField(max_length=50, default="")
    contact_number = models.CharField(max_length=50, default="")
    contact_email = models.CharField(max_length=50, default="")

    class Meta:
        app_label = 'intelicopter'


class Criterion(models.Model):
    id = models.IntegerField(primary_key=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    # -2:equals to or less than, -1:less than, 1:more than, 2:equals to or more than
    range = models.IntegerField(default=None, null=True)
    radio_group_id = models.IntegerField(default=None, null=True)

    class Meta:
        app_label = 'intelicopter'