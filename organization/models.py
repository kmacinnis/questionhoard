from django.db import models
from django.contrib.auth.models import User
from questions.models import Question



class Schema(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name


class Objective(models.Model):
    short = models.CharField(max_length=120)
    long = models.TextField()
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    questions = models.ManyToManyField(Question)
    def __str__(self):
        return self.short


class Topic(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    order = models.IntegerField()
    def __str__(self):
        return self.name


class Subtopic(models.Model):
    name = models.CharField(max_length=120)
    topic = models.ForeignKey(Topic)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    objectives = models.ManyToManyField(Objective)
    order = models.IntegerField()
    def __str__(self):
        return self.name


