from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UserSerializer , ForgotPasswordSerializer , ResetPasswordSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User , Profile
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializer import ProfileSerializer , ProfileSerializer2 , UserSerializer2
from rest_framework.parsers import MultiPartParser, FormParser
from products.models import Product
from products.serializer import ProductsSerializer


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Activation link sent to your email, please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return Response({
                'message': 'User registered successfully',
                'refresh token': str(refresh),
                'access token': str(refresh.access_token),
                'mail_subject': mail_subject
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate( email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh token': str(refresh),
            'access token': str(refresh.access_token),
            'message':'Loged in successfully'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def forgot_password_api(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            try:
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                return Response({'message': 'Password reset email has been sent to your email address.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Failed to send email. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Account does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def resetpassword_validate_api(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return Response({'message': 'Token is valid. Proceed to reset password.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password_api(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        uid = request.session.get('uid')
        if uid:
            try:
                user = User.objects.get(pk=uid)
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Session expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_api(request):
    if request.method == "POST":
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Ensure all required fields are provided
        if not all([current_password, new_password, confirm_password]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the authenticated user
        user = User.objects.get(username=request.user.username)

        # Verify that the new passwords match
        if new_password == confirm_password:
            # Attempt to authenticate the user with the current password
            success = user.check_password(current_password)
            if success:
                # Update the password if authentication succeeds
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
            else:
                # Return an error if the current password is incorrect
                return Response({'error': 'Invalid current password.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return an error if the new passwords do not match
            return Response({'error': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.get(user=self.request.user)
    


class EditProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        user_serializer = UserSerializer2(user, context={'request': request})
        profile_serializer = ProfileSerializer2(profile, context={'request': request})
        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        user_data = {
            'username': request.data.get('username'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email')
        }
        profile_data = {
            'address': request.data.get('address'),
            'image': request.FILES.get('image'),  # Handle file upload
            'country': request.data.get('country'),
            'city': request.data.get('city'),
            'company': request.data.get('company'),
            'headline': request.data.get('headline'),
            'about': request.data.get('about'),
            'address_line_1': request.data.get('address_line_1'),
            'address_line_2': request.data.get('address_line_2')
        }

        user_serializer = UserSerializer2(user, data=user_data, partial=True, context={'request': request})
        profile_serializer = ProfileSerializer2(profile, data=profile_data, partial=True, context={'request': request})

        user_valid = user_serializer.is_valid()
        profile_valid = profile_serializer.is_valid()

        if user_valid and profile_valid:
            user_serializer.save()
            profile_serializer.save()
            return Response({
                'user': user_serializer.data,
                'profile': profile_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'user_errors': user_serializer.errors if not user_valid else {},
            'profile_errors': profile_serializer.errors if not profile_valid else {}
        }, status=status.HTTP_400_BAD_REQUEST)


class FavouriteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(like=request.user)
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)