from django.shortcuts import render
from products.models import Product , Subcategory
from django.db.models import Count
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.
def home(request):
    trandy_paroduct = Product.objects.all().order_by('-views')
    just_arrived = Product.objects.all().order_by('-created_at')
    category = Subcategory.objects.all().annotate(category_count=Count("product_subcategory"))[:3]

    context = {
        'trandy_product':trandy_paroduct,
        'just_arrived':just_arrived,
        'category':category,
    }
    return render(request , 'home.html' , context)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            subject = "Welcome to EShopper site"
            message = "Our team will contact you within 24hrs."
            email_from = settings.EMAIL_HOST_USER
            email = form.cleaned_data['email']
            recipient_list =email
            send_mail(subject, message, email_from, [recipient_list])
            messages.success(request, 'Your Message send successfully.')
        else:
            messages.error(request, 'Pls try agian.')
    
    form = ContactForm()
    context = {'form':form}
    return render(request,'contact.html',context)