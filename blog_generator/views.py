from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError



def get_yt_title(ytLink) -> str:
    try:
        yt = YouTube(ytLink)
        return yt.title
    except VideoUnavailable:
        raise ValueError("The video is unavailable.")
    except RegexMatchError:
        raise ValueError("YouTube structure changed or invalid URL.")
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")


@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ytLink = data.get('link')

            if not ytLink:
                return JsonResponse({'error': 'No link provided'}, status=400)

            ytTitle = get_yt_title(ytLink)
            return JsonResponse({'content': ytTitle})

        except ValueError as ve:
            print('in value error')
            return JsonResponse({'error': str(ve)}, status=400)

        except Exception as e:
            return JsonResponse({'error': 'Internal server error', 'detail': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




@login_required
def index(request):
    return render(request, 'index.html')

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid Credentials'
            return render(request, 'login.html', { 'error_message': error_message })
        
    return render(request, 'login.html')


def user_register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['repeatPassword']

        if password == repeat_password:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html', { 'error_message' : error_message })
            
        else:
            error_message: str = 'Passwords do not match'
            return render(request, 'signup.html', { 'error_message' : error_message })
    

    return render(request, 'signup.html')


def user_logout(request):
    logout(request)
    return redirect('/')