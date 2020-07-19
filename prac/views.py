from django.http import HttpResponse, request
from django.shortcuts import render


# HOME PAGE
def home(request):
    return render(request,'home.html')
