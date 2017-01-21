from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from time import strftime

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class data(models.Model):
    SATISFACTION_CHOICE=[]
    for i in range(1,11):
        SATISFACTION_CHOICE+=[(i,i)]
    date = models.DateField(default=strftime("%d/%m/%Y"))
    treatment = models.CharField(max_length=64)
    notes = models.TextField(blank=True)
    satisfaction = models.IntegerField(choices=SATISFACTION_CHOICE)
    def __str__(self):
        return self.treatment
    
class UserProfile(models.Model):
    GENDER_CHOICE=(
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Intersex', 'Intersex'),
    )
    user = models.OneToOneField(User)
    birthDate= models.DateField()
    legalName = models.CharField(max_length=64)
    knownName = models.CharField(max_length=64, blank=True)
    gender = models.CharField(max_length=32)
    birthGender = models.CharField(max_length=8, choices=GENDER_CHOICE)
    def __str__(self):
        return self.user.username
    
