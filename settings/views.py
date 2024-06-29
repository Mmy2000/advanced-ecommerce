from django.shortcuts import render , get_object_or_404
from products.models import Product , Subcategory , Category
from .models import Settings , NewsLitter  , About , FAQ
from django.db.models import Count
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator


# Create your views here.
def home(request):
    trandy_paroduct = Product.objects.all().order_by('-views')[:4]
    just_arrived = Product.objects.all().order_by('-created_at')[:4]
    categories = Category.objects.all()

    context = {
        'trandy_product':trandy_paroduct,
        'just_arrived':just_arrived,
        'categories':categories,
    }
    return render(request , 'home.html' , context)

def subcategories(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)

    context = {
        'category': category,
        'subcategories': subcategories,
    }
    return render(request, 'subcategories.html', context)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            subject = "Welcome to EL SAADA Website"
            message = "Our team will contact you within 24hrs."
            email_from = settings.EMAIL_HOST_USER
            email = form.cleaned_data['email']
            recipient_list = email

            try:
                send_mail(subject, message, email_from, [recipient_list])
            except Exception as e:
                # Log the exception (optional)
                print(f"Failed to send email: {e}")

            messages.success(request, 'Your message was sent successfully.')
        else:
            messages.error(request, 'Please try again.')
    else:
        form = ContactForm()
    about = Settings.objects.last()
    context = {'form':form,
               'about':about}
    return render(request,'contact.html',context)

def newsletters(request):
    email = request.POST.get('email')
    NewsLitter.objects.create(email=email)
    return JsonResponse({'done':'done'})

def about(request):
    about = About.objects.last()
    faq = FAQ.objects.all()
    context = {
        'about':about,
        'faq':faq
    }
    return render(request , 'about.html' , context)

def custom_404_view(request, exception=None):
    return render(request, '404.html', {}, status=404)

