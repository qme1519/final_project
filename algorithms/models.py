from django.db import models
import os

# define category model with name as attribute
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# define algorithm model with algorithm properties
class Algorithm(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FilePathField(path="algorithms/img")
    categories = models.ManyToManyField("Category", related_name="algorithms")
    bestCase = models.TextField()
    worstCase = models.TextField()
    purpose = models.CharField(max_length=50)
    def __str__(self):
        return self.title
