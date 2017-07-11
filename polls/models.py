# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.db import models


# Create your models here.
class Poll(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def max_score(self):
        return sum([x.score for y in self.page_set.all()
                    for z in y.question_set.all()
                    for x in z.choice_set.all()
                    if x.score > 0])


class Page(models.Model):
    poll = models.ForeignKey(Poll)
    page_name = models.CharField(max_length=200)

    def __str__(self):
        return self.page_name


class Question(models.Model):
    page = models.ForeignKey(Page)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

    def max_score(self):
        return sum([x.score for x in self.choice_set.all() if x.score > 0])


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
