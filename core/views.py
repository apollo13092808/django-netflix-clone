import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from core.models import Movie, MovieList


# Create your views here.
@login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()
    featured_movie = movies[len(movies) - 1]

    context = {
        'movies': movies,
        'featured_movie': featured_movie,
    }
    return render(request=request, template_name='core/index.html', context=context)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request=request, user=user)
            return redirect(to='index')
        else:
            messages.info(request=request, message='Invalid credentials')
            return redirect('login')

    return render(request=request, template_name='core/login.html')


def sign_up(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request=request, message='Email already exists')
                return redirect(to='register')
            elif User.objects.filter(username=username).exists():
                messages.info(request=request, message='Username already exists')
                return redirect(to='register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Log user in
                user_login = authenticate(username=username, password=password)
                login(request=request, user=user_login)
                return redirect(to='index')
        else:
            messages.info(request=request, message='Passwords did not match')
            return redirect(to='register')
    else:
        return render(request=request, template_name='core/signup.html')


@login_required(login_url='login')
def sign_out(request):
    logout(request=request)
    return redirect(to='login')


@login_required(login_url='login')
def movie(request, movie_uuid):
    movie_detail = Movie.objects.get(uuid=movie_uuid)
    context = {
        'movie_detail': movie_detail,
    }
    return render(request=request, template_name='core/movie.html', context=context)


@login_required(login_url='login')
def genre(request, movie_genre):
    movies = Movie.objects.filter(genre=movie_genre)
    context = {
        'movies': movies,
        'movie_genre': movie_genre,
    }
    return render(request=request, template_name='core/genre.html', context=context)


@login_required(login_url='login')
def my_list(request):
    movie_list = MovieList.objects.filter(owner=request.user)
    user_movie_list = []
    for item in movie_list:
        user_movie_list.append(item.movie)
    context = {
        'movies': user_movie_list
    }
    return render(request=request, template_name='core/my_list.html', context=context)


@login_required(login_url='login')
def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None

        movie_obj = get_object_or_404(Movie, uuid=movie_id)
        movie_list, created = MovieList.objects.get_or_create(owner=request.user, movie=movie_obj)

        if created:
            response_data = {'status': 'success', 'message': 'Added ✓'}
        else:
            response_data = {'status': 'info', 'message': 'Movie already exists in your list'}

        return JsonResponse(data=response_data)
    else:
        return JsonResponse(data={'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        search_term = request.POST['search_term']
        movies = Movie.objects.filter(title__icontains=search_term)
        context = {
            'movies': movies,
            'search_term': search_term,
        }
        return render(request=request, template_name='core/search.html', context=context)
    else:
        return redirect(to='index')
