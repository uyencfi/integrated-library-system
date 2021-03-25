"""libsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from catalog import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.start, name='start'),
	path('home/', views.home, name='home'),	# AKA search results page. HOMEPAGE should be search page
	path('books/<int:book_id>/', views.book_details, name='book_details'),
	path('search/', views.search, name='search'),
	
	path('borrow/<int:book_id>/', views.borrow, name='borrow'),
	path('reserve/<int:book_id>/', views.reserve, name='reserve'),
	path('special-reserve/<int:book_id>/', views.special_reserve, name='special_reserve'),


	# need new HOMEPAGE. current home should be search results page.
	# Correct home: show welcome msg, nav bar, hamburger, EXPLORE button leading to search page

	path('signup/', accounts_views.signup, name='signup'),
	path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	# path('settings/account/', accounts_views.UserUpdateView.as_view(), name='my_account'),	# change user info, not needed

	path('my-fines', views.my_fines, name='my_fines'),
	path('make-payment', views.make_payment, name='make_payment'),
	path('my-books', views.my_books, name='my_books'),
	path('return/<int:book_id>/', views.return_book, name='return'),
	path('extend/<int:book_id>/', views.extend, name='extend'),

    path('admin/', admin.site.urls),
]
