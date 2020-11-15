"""
Views for the lists app of superlists
"""
# from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item, List

def home_page(request):
    """
    View to render our home page
    """
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-only-list/')
    return render(request, 'lists/home.html')

def new_list(request):
    """
    View to render a new list page
    """
    the_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=the_list)
    return redirect('/lists/the-only-list/')

def view_list(request):
    """
    View to render a list of to-do items
    """
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})
