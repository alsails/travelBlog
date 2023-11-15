from django.views.generic import ListView, DetailView
from .models import Post, News
from .parsingNews import parse_and_save_data
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm
from .auth import custom_authenticate
from django.http import JsonResponse


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            errors = {
                'non_field_errors': [str(error) for error in form.non_field_errors()],
                'username': [str(error) for error in form['username'].errors],
                'email': [str(error) for error in form['email'].errors],
                'password1': [str(error) for error in form['password1'].errors],
                'password2': [str(error) for error in form['password2'].errors],
            }
            return JsonResponse({'status': 'error', 'errors': errors})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = custom_authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success'})
            else:
                error_message = 'Убедитесь, что правильно ввели имя пользователя и пароль.'
                return JsonResponse({'status': 'error', 'message': error_message}, safe=False)
        else:
            error_message = 'Пожалуйста, введите корректные данные для входа.'
            return JsonResponse({'status': 'error', 'message': error_message}, safe=False)
    return render(request, 'login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect("home")


class BlogList(ListView):
    model = Post
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user)
        context['username'] = self.request.user.username  # Получить имя пользователя
        return context


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username  # Получить имя пользователя
        return context


class NewsList(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news_list'
    ordering = ['-time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.now().date()
        context['yesterday'] = datetime.now().date() - timedelta(days=1)
        context['username'] = self.request.user.username
        return context

    def get(self, request, *args, **kwargs):
        parse_and_save_data()
        return super().get(request, *args, **kwargs)


class NewsDetailView(DetailView):
    model = News
    template_name = 'new_detail.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username  # Получить имя пользователя
        return context
