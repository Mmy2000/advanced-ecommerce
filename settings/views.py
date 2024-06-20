from django.shortcuts import render
from products.models import Product , Subcategory
from .models import Settings , NewsLitter , Post
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
    category = Subcategory.objects.all().annotate(category_count=Count("product_subcategory"))[:3]

    context = {
        'trandy_product':trandy_paroduct,
        'just_arrived':just_arrived,
        'category':category,
    }
    return render(request , 'home.html' , context)
def blog(request):
    post = Post.objects.all()
    paginator = Paginator(post,6)
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)
    context = {
        'post':paged_posts
    }
    return render(request , 'blog_list.html' , context)
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

from django.http import HttpResponseNotFound

def custom_404_view(request, exception=None):
    return render(request, '404.html', {}, status=404)