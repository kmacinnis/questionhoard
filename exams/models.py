from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from model_utils.managers import InheritanceManager
from model_utils import Choices
import picklefield

from questions.models import Question, AnswerChoice
from organization.models import Course



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
    course = models.ForeignKey(Course)
    
    def __str__(self):
        return self.private_title

    def get_absolute_url(self):
        return reverse('ExamRecipeDetail', args=(str(self.id),))

    def schema(self):
        return self.course.course_type.schema


class ExamPartRecipe(models.Model):
    exam = models.ForeignKey(ExamRecipe)
    title = models.CharField(max_length=250)
    show_title = models.BooleanField(default=True)
    instructions = models.TextField(blank=True, null=True)
    order = models.IntegerField()
    QUESTION_TYPES = BASIC_QUESTION_TYPES + [('mix', 'mixture'),]
    question_style = models.CharField(max_length=3, choices=QUESTION_TYPES)
    shuffled = models.BooleanField(default=False)
    
    def __str__(self):
        return "{0} ({1})".format(self.title,self.id)
    
    def question_style_text(self):
        return self.QUESTION_TYPES[self.question_style]
    
    def question_count(self):
        simple_qs = len(self.simple_questions_list())
        pool_qs = sum([p.choose for p in self.pool_list()])
        return simple_qs + pool_qs

    def simple_questions_list(self):
        all_items = self.examrecipeitem_set.select_subclasses()
        return [item for item in all_items if type(item)==ExamRecipeQuestion]

    def pool_list(self):
        all_items = self.examrecipeitem_set.select_subclasses()
        return [item for item in all_items if type(item)==ExamRecipePool]
                                        


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
    def exam(self):
        return self.part.exam
    def type(self):
        return ExamRecipeItem.objects.get_subclass(id=self.id).type()
    class Meta:
        ordering = ['order']


class ExamRecipeQuestion(ExamRecipeItem):
    question = models.ForeignKey(Question)
    
    def description(self):
        return "Question: {}".format(self.name)

    def type(self):
        return 'question'


class ExamRecipePool(ExamRecipeItem):
    questions = models.ManyToManyField(Question, blank=True)
    choose = models.IntegerField()

    def __str__(self):
        return 'Pool: {}'.format(self.name)

    def description(self):
        qlist = '; '.join([q.name for q in self.questions.all()])
        return 'Pool (Choose {0} randomly): {1}'.format(self.choose, qlist)

    def type(self):
        return 'pool'


class GeneratedSet(models.Model):
    recipe = models.ForeignKey(ExamRecipe, blank=True, null=True)
    created_by = models.ForeignKey(User)
    course = models.ForeignKey(Course)
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
    class Meta:
        ordering = ['generated_set','form']


class ExamPart(models.Model):
    exam = models.ForeignKey(Exam)
    title = models.CharField(max_length=250)
    show_title = models.BooleanField(default=True)
    instructions = models.TextField(blank=True, null=True)
    order = models.IntegerField()
    question_style = models.CharField(max_length=3)

    class Meta:
        ordering = ['exam','order']


class ExamQuestion(models.Model):
    question = models.ForeignKey(Question)
    vardict = picklefield.PickledObjectField()
    part = models.ForeignKey(ExamPart)
    item = models.ForeignKey(ExamRecipeItem)
    order = models.IntegerField()
    question_text = models.TextField()
    space_after = models.CharField(max_length=10)

    class Meta:
        ordering = ['part','order']


class ExamAnswerChoice(models.Model):
    exam_question = models.ForeignKey(ExamQuestion)
    position = models.IntegerField()
    choice_text = models.TextField()
    correct = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['position']


FONTS = Choices(
    ('concmath', 'Computer Concrete'),
    ('cmbright','Computer Modern Bright'),
    ('kpfonts','Kepler'),
    ('kmath,kerkis', 'Kerkis'),
    ('mathpazo','Palatino (mathpazo)'),
    ('sitx', 'Times (sitx)'),
)


class FormattingPreferences(models.Model):
    user = models.OneToOneField(User)
    font = models.CharField(max_length=30, choices=FONTS, default='mathpazo')
    font_size = models.CharField(max_length=4, default=12)

    first_page_header_different = models.BooleanField(default=False)
    header_left = models.CharField(max_length=150, blank=True, null=True)
    header_center = models.CharField(max_length=150, blank=True, null=True)
    header_right = models.CharField(max_length=150, blank=True, null=True)
    first_page_header_left = models.CharField(max_length=150, blank=True, null=True)
    first_page_header_center = models.CharField(max_length=150, blank=True, null=True)
    first_page_header_right = models.CharField(max_length=150, blank=True, null=True)

    first_page_footer_different = models.BooleanField(default=False)
    footer_left = models.CharField(max_length=150, blank=True, null=True)
    footer_center = models.CharField(max_length=150, blank=True, null=True)
    footer_right = models.CharField(max_length=150, blank=True, null=True)
    first_page_footer_left = models.CharField(max_length=150, blank=True, null=True)
    first_page_footer_center = models.CharField(max_length=150, blank=True, null=True)
    first_page_footer_right = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return 'Preferences for {}'.format(self.user)





