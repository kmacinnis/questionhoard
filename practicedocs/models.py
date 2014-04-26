from django.db import models
from django.contrib.auth.models import User
from questions.models import Question


class DocumentRecipe(models.Model):
    title = models.CharField(max_length=60)
    created_by = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title


class BlockRecipe(models.Model):
    '''
    A block is a set of exercises created from the same question.
    '''
    document = models.ForeignKey(DocumentRecipe)
    order = models.IntegerField()
    question = models.ForeignKey(Question, db_index=True)
    num_exercises = models.IntegerField()
    num_columns = models.IntegerField(default=1)
    space_after = models.CharField(max_length=30)


class Document(models.Model):
    title = models.CharField(max_length=60)
    recipe = models.ForeignKey(DocumentRecipe)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    def __str__(self):
        return self.title


class Block(object):
    document = models.ForeignKey(Document)
    order = models.IntegerField()
    recipe = models.ForeignKey(BlockRecipe)


class Exercise(models.Model):
    question = models.ForeignKey(Question, db_index=True)
    vardict = picklefield.PickledObjectField()
    def __str__(self):
        return "Exercise «{0}»".format(self.id)








