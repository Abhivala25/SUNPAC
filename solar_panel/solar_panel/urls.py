"""
URL configuration for solar_panel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from solar_app.views import *
# from solar_app.views import  * login, profilepage , delete , adminpage , productpage, logout ,home,NewCategoryView ,signup, insert2 , gridview ,more,moresolar,morebattery,morebulb,home2,insert
from django.conf import settings
from django.conf.urls.static import static

# from .views import productpage


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),# Use a different path for the login page
    path('', home, name='home'),
    path('home2', home2, name='home2'),
    path('newcategory/', NewCategoryView.as_view(), name='newcategory'),
    # path('insert2', insert2, name='insert2'),
    path('signup/', signup, name='signup'),
    path('more/', more, name='more'),
    path('moresolar/', moresolar, name='moresolar'),
    path('morebattery/', morebattery, name='morebattery'),
    path('morebulb/', morebulb, name='morebulb'),
    path('insert/', insert, name='insert'),
    path('insert2/', insert2.as_view(), name='insert2'),
    path('gridview/', gridview, name='gridview'),
    path('productpage/<int:category_id>/', productpage, name='productpage'),
    path('profilepage/', profilepage , name='profilepage'),
    path('adminpage/', adminpage , name='adminpage'),
    path('delete_user/' , delete_user , name='delete_user'),
    path('delete_category/' , delete_category , name='delete_category'),
    path('aboutus_page/' , aboutus_page , name='aboutus_page'),
    path('admin_user/' , admin_user , name='admin_user'),
    path('admin_category/' , admin_category , name='admin_category'),
    path('privacy/' , privacy , name='privacy'),
    path('payment_page/<int:category_id>/' , payment_page , name='payment_page'),
    path('user_list/' , user_list , name='user_list'),
    path('blog_page/' , blog_page , name='blog_page'),
    path('otp_page/' , otp_page , name='otp_page'),
    path('contactus/', contactus , name='contactus'),
    path('payout_success/', payout_success , name='payout_success'),
    path('cart/', cart ,name='cart'),
    path('success/', success , name='success'),
    path('ordered_item/', ordered_item ,name='ordered_item'),
    path('cart_added/', cart_added , name='cart_added'),
    path('generate_invoice/<int:category_id>/', generate_invoice, name='generate_invoice'),
    path('admin_invoice/', admin_invoice, name='admin_invoice'),     # Invoice records page
    path('reset_invoice/', reset_invoice, name='reset_invoice'),     # Reset invoices action
    path('delete_invoice/', delete_invoice, name='delete_invoice'),
    path('reset/', reset , name='reset'),

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
