from django.db import models
import picklefield
from django.contrib.auth.models import User
import questions.handling
from django.core.exceptions import ObjectDoesNotExist

import random

class Question(models.Model):
    name = models.CharField(unique=True, max_length=240)
    code = models.TextField(blank=True, null=True)
    question_text = models.TextField()
    prompt = models.CharField(max_length=240, blank=True, null=True)
    short_version = models.CharField(max_length=240, blank=True, null=True)
    symbol_vars = models.CharField(max_length=240, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    last_updated = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)
    packages = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return "/questions/%i/" % self.id
    
    def preview(self):
        # TODO: questions with graphics will need a graphic preview
        return questions.handling.preview_questiontext(self)
    
    @property
    def is_validated(self):
        try:
            return (self.validation.last_verified >= self.last_updated)
        except ObjectDoesNotExist:
            return False
    
    def random_vardict(self):
        if self.is_validated:
            return random.choice(self.validation.vardicts)
        else:
            raise ValueError("Question has not yet been validated.")


class Validation(models.Model):
    question = models.OneToOneField(Question)
    last_verified = models.DateTimeField(null=True)
    vardicts = picklefield.PickledObjectField(null=True)
    num_poss = models.IntegerField(default=0)
    validated_by = models.ForeignKey(User)
    def __str__(self):
        return 'Validation of  «{0}»'.format(self.question)


class RandVar(models.Model):
    question = models.ForeignKey(Question, db_index=True)
    varname = models.CharField(max_length=10, verbose_name="Variable")
    varposs = models.CharField(max_length=240, verbose_name="Set of possibile values")
    def __str__(self):
        return "Variable «{0}» in Question {1}".format(
                                    self.varname, self.question)


class Condition(models.Model):
    question = models.ForeignKey(Question, db_index=True)
    condition_text = models.CharField(max_length=240)
    def __str__(self):
        return "Condition «{0}» in Question {1}".format(
                                    self.condition_text, self.question)


class AnswerChoice(models.Model):
    CORRECT = 'CORR'
    TOP3 = 'TOP3'
    TOP4 = 'TOP4'
    DISTRACT = 'DIST'
    OTHER = 'OTHR'
    VARIANT = 'VANS'
    CHOICE_TYPES = (      
        (CORRECT, 'Correct Answer'),
        (TOP3, 'Distractor (Top 3)'),
        (TOP4, 'Distractor (Top 4)'),
        (DISTRACT, 'Distractor'),
        (OTHER, 'Unknown'),
        (VARIANT, 'Variant of Correct Answer'),
        )
    
    RANDOM = 'random'
    LAST = 'last'
    A = '0'
    B = '1'
    C = '2'
    D = '3'
    E = '4'
    PIN_TYPES = (
        (RANDOM, 'Random'),
        (LAST, 'Last'),
        (A,'A'),(B,'B'),(C,'C'),(D,'D'),(E,'E'),
    )
    
    question = models.ForeignKey(Question, db_index=True)
    choice_text = models.CharField(max_length=240, default='${choice_expr}$')
    choice_expr = models.CharField(max_length=240, blank=True, null=True)
    choice_type = models.CharField(max_length=20, choices=CHOICE_TYPES, default=DISTRACT)
    pin = models.CharField(max_length=6, choices=PIN_TYPES, default=RANDOM)
    comment = models.CharField(max_length=240, blank=True, null=True)
    def __str__(self):
        if self.choice_expr:
            return "Answer Choice «{0}» in Question {1}".format(
                                    self.choice_expr, self.question)
        return "Answer Choice «{0}» in Question {1}".format(
                                    self.choice_text, self.question)



class BadCodeWarning(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    warn_datetime = models.DateTimeField()
    field_name = models.CharField(max_length=50)
    code = models.TextField()
    
    DOUBLE_UNDERSCORE = 1
    OVER_NESTING = 2
    BYTE_STRINGS = 3
    
    ERROR_TYPES = (
        (DOUBLE_UNDERSCORE, 'Has double underscore'),
        (OVER_NESTING, 'Too many parentheses'),
        (BYTE_STRINGS, 'Uses explicit bytestrings'),
    )
    error_type = models.IntegerField()
    admin_comment = models.CharField(max_length=240, blank=True, null=True)
    def __str__(self):
        return "{user} at {time}".format(user=user, time=warn_datetime.isoformat())



