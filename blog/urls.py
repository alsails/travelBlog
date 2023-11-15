from django.urls import path, include
from .views import BlogList, BlogDetailView, NewsList, NewsDetailView, signup, signin, signout

urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('news/', NewsList.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='new_detail'),
    path('', BlogList.as_view(), name='home'),
    path('home/', BlogList.as_view(), name='home'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
]
