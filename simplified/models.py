from django.db import models

class Foo(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return "Foo {} «{}»".format(self.id, self.name)
    def get_absolute_url(self):
        return "/simp/%i/edit/" % self.id
    

class Bar(models.Model):
    foo = models.ForeignKey(Foo)
    barname = models.CharField(max_length=10)
    def __str__(self):
        return "«{}» for Foo {}".format(self.barname, self.foo_id)


class Meep(models.Model):
    bar = models.ForeignKey(Bar)
    meepname = models.CharField(max_length=10)
    def __str__(self):
        return self.meepname