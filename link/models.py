from django.db import models

class Application(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/')
    link = models.URLField()
    section = models.CharField(max_length=150)
    
    class Meta:
        db_table = 'Applicationlink'


class Userslogin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'Userslogin'


class Section(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Section'

    def __str__(self):
        return self.name


class Assignsection(models.Model):
    user = models.OneToOneField(Userslogin, on_delete=models.CASCADE, unique=True)
    sections = models.ManyToManyField(Section)

    class Meta:
        db_table = 'user_data_table'

    def __str__(self):
        return self.user.username
