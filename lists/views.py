"""
Views for the lists app of superlists
"""
# from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    """
    View to render our home page
    """
    return render(request,
                  'lists/home.html',
                  {'new_item_text': request.POST.get('item_text', '')}
                 )
