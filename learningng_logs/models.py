from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    """Representa um assunto"""
    text = models.CharField(max_length=200)
    data_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)


    def __str__(self):
        """Imprimte uma string para representar o objeto"""
        return self.text


class Entry(models.Model):
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'entries'


    def __str__(self):
        """Uma representaçÃo em string do obj"""
        return self.text[:50] + "..."
