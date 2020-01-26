from django.db import models

from django.db import models

# Create your models here.

class Planet(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Sith(models.Model):
    name = models.CharField(max_length=200)
    workPlanet = models.ForeignKey(Planet, on_delete=models.PROTECT)
    countOfHandShadow = models.IntegerField()

    def __str__(self):
        return self.name

class Recruit(models.Model):
    name = models.CharField(max_length=200)
    planetOfResidence = models.ForeignKey(Planet, on_delete=models.PROTECT)
    age = models.IntegerField()
    email = models.EmailField(max_length = 254)
    rankOfHandShadow = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.AutoField(primary_key=True)

class Question(models.Model):
    question = models.CharField(max_length=350)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ('question',)

class TestHandShadow(models.Model):
    orderСode   = models.ForeignKey(Order, on_delete=models.PROTECT)
    question  = models.ManyToManyField(Question)

    class Meta:
        ordering = ('orderСode',)

class Answer(models.Model):
    answer  = models.CharField(max_length=350)

    def __str__(self):
        return self.answer


class Result(models.Model):
    recruit = models.ForeignKey(Recruit, on_delete=models.PROTECT)
    test = models.ForeignKey(TestHandShadow, on_delete=models.PROTECT)
    answer  = models.ManyToManyField(Answer)

    # question = models.ForeignKey(question, on_delete=models.PROTECT)



# models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE, )
