from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='shops'),
    path('aboutproduct/<int:my_id>/', views.quickview),
    path('checkout/',views.checkout),
    path('tracker/',views.tracker),
    path('handlerequest/',views.handlerequest),
    path('search/',views.search),
    path('signup/',views.sign_up),
    path('login/',views.handlelogin),
    path('logout/',views.handlelogout),
    path('takingreply/',views.takingreply)
]
