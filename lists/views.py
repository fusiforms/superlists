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
    return redirect(f'/lists/{the_list.id}/')

def view_list(request, list_id):
    """
    View to render a list of to-do items
    """
    the_list = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=the_list)
    return render(request, 'lists/list.html', {'list': the_list})

def add_item(request, list_id):
    """
    View to add an item to an existing list
    """
    the_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=the_list)
    return redirect(f'/lists/{the_list.id}/')
