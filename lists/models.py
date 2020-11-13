"""
The models for the list app
"""
from django.db import models

class Item(models.Model):
    """
    Model that holds a single to-do list item
    """
    text = models.TextField(default='')


    def __str__(self):
        return self.text
