from django.shortcuts import render, redirect
from django.views import View
from nav.models import Office, SearchHistory
import json
from PIL import Image
from pyzbar.pyzbar import decode
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomSignupForm, CustomLoginForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


class IndexView(View):
    def get(self, request, *args, **kwargs):
        offices = Office.objects.all()
        offices_data = [
            {
                'name': office.name,
                'description': office.description,
                'location': office.location,
                'contact': office.contact,
                'email': office.email,
                'image': office.image.url if office.image else '',
                'longitude': office.longitude,
                'latitude': office.latitude,
            }
            for office in offices
        ]
        context = {
            'offices_json': json.dumps(offices_data)
        }
        return render(request, 'index.html', context)


def scan_qr(request):
    qr_link = None
    error_message = None

    if request.method == 'POST':
        # Get the uploaded file from the request.
        uploaded_file = request.FILES.get('qr_image')
        if not uploaded_file:
            error_message = "No file uploaded. Please select an image file."
        else:
            try:
                # Open the image using Pillow.
                image = Image.open(uploaded_file)
                # Attempt to decode any QR codes in the image.
                decoded_objects = decode(image)
                if decoded_objects:
                    # Get the data from the first decoded QR code.
                    qr_link = decoded_objects[0].data.decode('utf-8')
                else:
                    error_message = "No valid QR code found in the image."
            except Exception as e:
                error_message = f"Error processing the image: {e}"

    context = {
        'qr_link': qr_link,
        'error_message': error_message,
    }
    return render(request, 'scan_qr.html', context)



def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')  # Redirect to homepage after signup
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to homepage after login
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')



@require_POST
@login_required
def store_search(request):
    query = request.POST.get('query')
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    SearchHistory.objects.create(user=request.user, query=query)
    return JsonResponse({'message': 'Search query stored successfully'})


@login_required(login_url="/login/")
def search_history(request):
    history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'search_result.html', {'history': history})


@login_required
def settings_view(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            # Update the session to prevent logging out after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        password_form = PasswordChangeForm(request.user)
    
    context = {
        'password_form': password_form,
    }
    
    return render(request, 'settings.html', context)