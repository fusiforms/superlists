"""
The models for the list app
"""
from django.db import models

class Item(models.Model):
    """
    Model that holds a single to-do list item
    """
    text = models.TextField(default='')
    list = models.ForeignKey('List', default=None,on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class List (models.Model):
    """
    Model that holds a whole to-do-list
    """

    def __str__(self):
        return 'Hello'
