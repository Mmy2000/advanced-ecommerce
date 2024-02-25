from django.shortcuts import render , redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate , login 

# Create your views here.

def register(request):
    form=RegistrationForm()
    context = {
        'form':form
    }
    return render(request,'accounts/register.html' , context)