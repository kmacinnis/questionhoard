from django.db import models
from django.contrib.auth.models import User
from questions.models import Question
import os


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
    schema = models.ForeignKey(Schema)
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


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Textbook(models.Model):
    title = models.CharField(max_length=200)
    edition = models.CharField(max_length=10)
    authors = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20)
    image = models.ImageField(blank=True, null=True, upload_to=get_image_path)
    def __str__(self):
        return "{title}, {edition} ed.".format(
                title=self.title,edition=self.edition)


class CourseType(models.Model):
    name = models.CharField(max_length=200)
    schema = models.ForeignKey(Schema)
    textbook = models.ForeignKey(Textbook, blank=True, null=True)
    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey(User)
    start_date = models.DateField()
    end_date = models.DateField()
    semester = models.CharField(max_length=50)
    assistants = models.ManyToManyField(
        User, related_name='assisting_courses', blank=True
    )
    course_type = models.ForeignKey(CourseType)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return "{0} ({1})".format(self.name, self.instructor)



