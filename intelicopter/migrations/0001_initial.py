# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-22 10:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(default=None, max_length=2000)),
                ('address', models.CharField(default=None, max_length=400)),
                ('postal_code', models.CharField(default=None, max_length=15)),
                ('contact_name', models.CharField(default=None, max_length=50)),
                ('contact_number', models.CharField(default=None, max_length=50)),
                ('contact_email', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('question_text', models.CharField(max_length=500)),
                ('range', models.IntegerField(default=None)),
                ('radio_group_id', models.IntegerField(default=None)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intelicopter.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(default=None, max_length=2000)),
                ('address', models.CharField(default=None, max_length=400)),
                ('postal_code', models.CharField(default=None, max_length=15)),
                ('contact_name', models.CharField(default=None, max_length=50)),
                ('contact_number', models.CharField(default=None, max_length=50)),
                ('contact_email', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('option_text', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=500)),
                ('question_type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('trigger_text', models.CharField(max_length=500)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_question_set', to='intelicopter.Question')),
                ('trigger_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trigger_question_set', to='intelicopter.Question')),
            ],
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intelicopter.Question'),
        ),
        migrations.AddField(
            model_name='criterion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intelicopter.Question'),
        ),
        migrations.AddField(
            model_name='activity',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intelicopter.Group'),
        ),
    ]
