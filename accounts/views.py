from django.shortcuts import render , redirect
from .forms import RegistrationForm , UserForm , ProfileForm
from django.contrib.auth import authenticate , login 
from .models import User , Profile
from products.models import Product
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from carts.models import Cart , CartItem
from carts.views import _cart_id
import requests
from orders.models import Order , OrderProduct
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address , Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
        

    else:
        form = RegistrationForm()
    context = {
        'form':form
    }
    return render(request,'accounts/register.html' , context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter( cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    cart_item = CartItem.objects.filter( user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation=item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity+=1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request,"Loged in successfully")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)                
            except:
                return redirect('profile')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
    
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

@login_required(login_url = 'login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)
        if new_password == confirm_password :
            success = user.check_password(current_password)
            if success :
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password Updated Successfully.')
                return redirect('profile')
            else:
                messages.error(request,'Please enter a valid current password.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request,'Password does not match.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return render(request , 'accounts/change_password.html')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST , instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            my_profile = profile_form.save(commit=False)
            my_profile.user = request.user
            my_profile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    context = {
        'profile':profile,
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request , 'profile/profile.html' , context)

@login_required(login_url='login')
def dashboard(request):
    profile=Profile.objects.get(user=request.user)
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_orderd=True)
    orders_count = orders.count()
    return render(request,'profile/dashboard.html',{
        'profile':profile,
        'orders':orders,
        'orders_count':orders_count,
    })

@login_required(login_url='login')
def orders(request):
    orders = Order.objects.filter(user=request.user,is_orderd=True).order_by('-created_at')
    context = {
        'orders':orders,
    }
    return render(request , 'profile/orders.html' , context)

def order_detail(request,order_id):
    profile=Profile.objects.get(user=request.user)
    orders = Order.objects.get(order_number=order_id)
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    context = {
        'profile':profile,
        'orders':orders,
        'order_detail':order_detail,
        'subtotal':subtotal,
    }
    return render(request,'profile/order_detail.html',context)
@login_required(login_url='login')
def favourite(request):
    products = Product.objects.filter(like=request.user)
    paginator = Paginator(products,6)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    return render(request , 'profile/favourite.html',{'products':paged_product})