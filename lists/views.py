"""
Views for the lists app of superlists
"""
# from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item

def home_page(request):
    """
    View to render our home page
    """
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    return render(request, 'lists/home.html', {'items': Item.objects.all()})
