from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from model_utils.managers import InheritanceManager
from model_utils import Choices
import picklefield

from questions.models import Question, AnswerChoice



BASIC_QUESTION_TYPES = Choices(
    ('mc', 'multiple choice'), 
    ('oa', 'open answer'), 
)

FORM_NUMBER_STYLE = Choices(
    ('letter', 'Letter: Form A, Form B, Form C, …'),
    ('number', 'Number: Form 1, Form 2, Form 3, …'),
)


class ExamRecipe(models.Model):
    private_title = models.CharField(max_length=250)
    display_title = models.CharField(max_length=250)
    created_by = models.ForeignKey(User)
    form_number_style = models.CharField(
            max_length=10, choices=FORM_NUMBER_STYLE, default='number')
    number_of_forms = models.IntegerField(default=1)
    max_number_choices = models.IntegerField(default=5)
    frozen = models.BooleanField(default=False)
    
    def __str__(self):
        return self.private_title

    def get_absolute_url(self):
        return reverse('ExamRecipeDetail', args=(str(self.id),))


class ExamPartRecipe(models.Model):
    exam = models.ForeignKey(ExamRecipe)
    title = models.CharField(max_length=250)
    show_title = models.BooleanField(default=True)
    instructions = models.TextField(blank=True, null=True)
    order = models.IntegerField()
    QUESTION_TYPES = BASIC_QUESTION_TYPES + [('mix', 'mixture'),]
    question_style = models.CharField(max_length=3, choices=QUESTION_TYPES)
    
    def __str__(self):
        return "{0} ({1})".format(self.title,self.id)
    
    def question_style_text(self):
        return self.QUESTION_TYPES[self.question_style]
    
    def simple_questions_count(self):
        # TODO: This doesn't distinguish between questions and pools
        return self.examrecipeitem_set.select_subclasses(
                                        "examrecipequestion").count()
    def simple_questions_list(self):
        # TODO: This doesn't distinguish between questions and pools
        return self.examrecipeitem_set.select_subclasses(
                                        "examrecipequestion")
                                        


class ExamRecipeItem(models.Model):
    '''
    This class is intended to be inherited by 
    ExamRecipeQuestion and ExamRecipePool.
    
    
    '''
    objects = InheritanceManager()
    
    part = models.ForeignKey(ExamPartRecipe)
    order = models.IntegerField()
    name = models.CharField(max_length=250)
    question_style = models.CharField(max_length=3,choices=BASIC_QUESTION_TYPES)
    space_after = models.CharField(max_length=10, default="5mm")

    def __str__(self):
        return self.name


class ExamRecipeQuestion(ExamRecipeItem):
    question = models.ForeignKey(Question)


class ExamRecipePool(ExamRecipeItem):
    questions = models.ManyToManyField(Question, blank=True)
    choose = models.IntegerField()


class GeneratedSet(models.Model):
    recipe = models.ForeignKey(ExamRecipe, blank=True, null=True)
    created_by = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return "{d:%b} {d.day}, {d.year} at {d:%l}:{d:%M}{d:%p}".format(
                    d=self.date_created)


class Exam(models.Model):
    generated_set = models.ForeignKey(GeneratedSet)
    title = models.CharField(max_length=250)
    form = models.CharField(max_length=10)
    
    def __str__(self):
        return "{title} (Form {form})".format(title=self.title,form=self.form)


class ExamPart(models.Model):
    exam = models.ForeignKey(Exam)
    title = models.CharField(max_length=250)
    show_title = models.BooleanField(default=True)
    instructions = models.TextField(blank=True, null=True)
    order = models.IntegerField()
    question_style = models.CharField(max_length=3)


class ExamQuestion(models.Model):
    question = models.ForeignKey(Question)
    vardict = picklefield.PickledObjectField()
    part = models.ForeignKey(ExamPart)
    item = models.ForeignKey(ExamRecipeItem)
    order = models.IntegerField()
    question_text = models.TextField()
    space_after = models.CharField(max_length=10)


class ExamAnswerChoice(models.Model):
    exam_question = models.ForeignKey(ExamQuestion)
    
    position = models.IntegerField()
    choice_text = models.TextField()
    correct = models.BooleanField()
    comment = models.TextField(blank=True, null=True)







