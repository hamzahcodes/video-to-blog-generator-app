from django.urls import path
from . import views

app_name = "blog_generator"

urlpatterns = [
    path('', view=views.index, name='home'),
    path('login', view=views.user_login, name='login'),
    path('logout', view=views.user_logout, name='logout'),
    path('register', view=views.user_register, name='register'),
    path('generate-blog', view=views.generate_blog, name='generate-blog')
]