from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from model_utils import Choices
import picklefield


from questions.models import Question, AnswerChoice



BASIC_QUESTION_TYPES = Choices(
    ('mc', 'multiple choice'), 
    ('oa', 'open answer'), 
)



class ExamRecipe(models.Model):
    title = models.CharField(max_length=250)
    created_by = models.ForeignKey(User)
    form_number_style = models.CharField(max_length=10)
    number_of_forms = models.IntegerField(default=1)


class ExamPartRecipe(models.Model):
    exam = models.ForeignKey(ExamRecipe)
    title = models.CharField(max_length=250)
    show_title = models.BooleanField(default=True)
    instructions = models.TextField(blank=True, null=True)
    order = models.IntegerField()
    question_style = models.CharField(max_length=3,
        choices = BASIC_QUESTION_TYPES + [('mix', 'mixture'),])


class ExamRecipeItem(models.Model):
    '''
    This class is intended to be inherited by 
    
    '''
    objects = InheritanceManager()
    
    part = models.ForeignKey(ExamPartRecipe)
    order = models.IntegerField()
    name = models.CharField(max_length=250)
    question_style = models.CharField(max_length=3,choices=BASIC_QUESTION_TYPES)


class ExamRecpeQuestion(ExamRecipeItem):
    question = models.ForeignKey(Question)


class ExamRecipePool(ExamRecipeItem):
    questions = models.ManyToManyField(Question)
    choose = models.IntegerField()


class Exam(models.Model):
    title = models.CharField(max_length=250)
    created_by = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)
    form = models.CharField(max_length=10)


class ExamPart(models.Model):
    exam = models.ForeignKey(ExamRecipe)
    title = models.CharField(max_length=250)
    show_title = models.BooleanField(default=True)
    instructions = models.TextField(blank=True, null=True)
    order = models.IntegerField()


class ExamQuestion(models.Model):
    question = models.ForeignKey(Question)
    vardict = picklefield.PickledObjectField()
    part = models.ForeignKey(ExamPart)
    order = models.IntegerField()
    

class ExamAnswerChoice(models.Model):
    exam_question = models.ForeignKey(ExamQuestion)
    answer_choice = models.ForeignKey(AnswerChoice)
    choice_label = models.CharField(max_length=3)
    






