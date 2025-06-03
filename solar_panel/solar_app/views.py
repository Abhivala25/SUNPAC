# Create your views here.
from django.shortcuts import render ,redirect ,get_object_or_404 
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
import solar_app.views
from .models import *
from django.views.generic import CreateView
from .models import Category
from .forms import CategoryForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy , reverse
from django.db.models import Q
from django.shortcuts import redirect
import random
from django.core.mail import send_mail
from .models import User
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect
from twilio.rest import Client
from datetime import datetime, timedelta
from django.utils import timezone
import random

# from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

# from .views import productpage
def verify_otp_sms(phone_number, entered_otp):
    account_sid = "AC886c80da9d760a7a329f19fbb71576a8"
    auth_token = "fe3bba794e8b0d2439f8a465cd83ce04"
    verify_sid = "VA820e04041df502e0171faf4d8f1f00ee"

    client = Client(account_sid, auth_token)

    try:
        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=phone_number, code=entered_otp)
        return verification_check.status
    except Exception as e:
        print(f"Error during OTP verification: {e}")
        return None
    

def send_otp_sms(phone_number):
    account_sid = "AC886c80da9d760a7a329f19fbb71576a8"
    auth_token = "fe3bba794e8b0d2439f8a465cd83ce04"
    verify_sid = "VA820e04041df502e0171faf4d8f1f00ee"
    twilio_phone_number = "+17603645757"
    
    client = Client(account_sid, auth_token)
    
    verification = client.verify.v2.services(verify_sid) \
      .verifications \
      .create(to=phone_number, channel="sms")
    print(verification.status)
    
    
def login(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        if not email or not password:
            cus_msg = '~ Incomplete Form '
            return render(request, "login.html", {'cus_msg': cus_msg})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            cus_msg = '~ No user found'
            return render(request, "login.html", {'cus_msg': cus_msg})
        
        if not password==user.password:
            cus_msg = '~ Invalid Password'
            return render(request, "login.html", {'cus_msg': cus_msg})
        else:
            request.session['is_authenticated'] = True
            request.session['user_id'] = user.id
            request.session['is_admin'] = user.is_admin
            # request.session['is_admin'] = user.is_admin
            # request.session['is_subscribed'] = user.is_subscribed
            cus_msg = 'Login successful'
            return redirect('home2')
        # # Authenticate user
        # user = User.objects.get(request, email=email, password=password)
        
        
        # if user is not None:
        #     # Authentication successful, login user
        #     auth_login(request, user)
        #     # Store user's ID in session
        #     request.session['user_id'] = user.id
        #     # Redirect to home page
        #     return redirect('home2')  # Assuming 'home' is the name of your home page URL
        # else:
        #     # Authentication failed, render login page with error message
        #     return render(request, "login.html", {'error_message': 'Invalid email or password.'})
    
    return render(request, 'login.html')
    
    
    #  if request.method == 'POST':
    #         umail = request.POST.get('u-mail') 
    #     password = request.POST.get('u-cpass')
    #     hashed_password = make_password(password)

        # user = User.objects.filter(name=username, password=hashed_password).first()

        
       
    
    
    
    
#    if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         # Authenticate user using email and password
#         user = authenticate(request, email=email, password=password)
        
#         if user is not None:
           
#             login(request, user)
#             request.session['abhi_id'] = user.id  
#             request.session['is_authenticated'] = True
#             return redirect('login/')
#         else:
           
#             messages.error(request, 'Invalid email or password')
           
    
#    return render(request, 'login.html')

            
def custom_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('is_authenticated', False):
            return redirect('login') 
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def logout(request):
 
    request.session['is_authenticated'] = False
   
    return redirect('home')

# def login(request):
    
#     if request.method == 'POST':
            # Get form data
        
        # name = request.POST.get('name', '')
        
        # uemail = request.POST.get('email')
        # upassword = request.POST.get('password')
        
        
        # user1 = User.objects.filter(email=uemail).first()

        # if not uemail or not upassword:
          
        #     return render(request, "login2.html", {'error_message': 'Incomplete form data'})

        # if user1 is None:
          
        #     return render(request, "login2.html", {'error_message': 'Invalid username.'})

      
        # if user1.password != upassword:
          
        #     return render(request, "login2.html", {'error_message': 'Invalid password.'})


       
    #     return redirect('/')
    # return render(request, 'login.html')
    
    
    
def generate_otp():
        return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for registration is: {otp}'
    from_email = 'abhivala55@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
        
    
    
@csrf_exempt
def signup(request):
   
    if request.method == 'POST':
            # Get form data
        
        # name = request.POST.get('name', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        address = request.POST.get('address')
        
        
        uemail = request.POST.get('uemail')
        upassword = request.POST.get('upassword')
        
        request.session['user_email'] = email
        request.session['phone_number']=phone_number
        
        user = User( name=name, 
                    email=email, 
                    password=password , 
                    phone_number=phone_number,
                    city=city,
                    address=address)
        
        
        user.save()
        otp = generate_otp()
        request.session['otp'] = otp
        send_otp_email(email, otp)
        send_otp_sms(phone_number)
        return redirect('otp_page')
    return render(request, 'signup.html')



class NewCategoryView(CreateView):
    model = Category  
    form_class = CategoryForm
    template_name = 'insert2.html' 
    success_url = reverse_lazy('home2')
    
    
class insert2(CreateView):
    model = Category
    fields =  ['pimg', 'price', 'wattage', 'voltage', 'warrenty', 'title', 'description1', 'solar_panel', 'solar_heater', 'inverter', 'solar_cooker', 'luminous', 'loom', 'hi_mo', 'discount_10', 'discount_20', 'discount_30', 'first_name', 'last_name', 'email', 'phone', 'description']
    template_name = name='insert2.html'
    success_url = reverse_lazy('insert2')
    
    def form_valid(self, form):
        
        if 'pimg' in self.request.FILES:
            form.instance.pimg = self.request.FILES['pimg']
     
        product_name = self.request.POST.get('product_name')
        if product_name:
            if product_name == "1":
                form.instance.solar_panel = True
            elif product_name == "2":
                form.instance.solar_heater = True
            elif product_name == "3":
                form.instance.inverter = True
            elif product_name == "4":
                form.instance.solar_cooker = True
                
        product_brand = self.request.POST.get('product_brand')
        if product_brand:
            if product_brand == "5":
                form.instance.luminous = True
            elif product_brand == "6":
                form.instance.loom = True
            elif product_brand == "7":
                form.instance.hi_mo = True
                
        discount = self.request.POST.get('discount')
        if discount:
            if discount == "8":
                form.instance.discount_10 = True
            elif discount == "9":
                form.instance.discount_20 = True
            elif discount == "10":
                form.instance.discount_30 = True
                form.save()
        return super().form_valid(form)
    
# def insert(request):
#     if request.method == 'POST':
#         try:
            
#             price = 2000
#             first_name = "gida"
#             last_name = "bapu"
#             email = "gida@gmail.com"
#             phone = 9090909090
#             # Extract data from the form
#             # price = request.POST.get('price')
#             # first_name = request.POST.get('first_name')
#             # last_name = request.POST.get('last_name')
#             # email = request.POST.get('email')
#             # phone = request.POST.get('phone')
#             # description = request.POST.get('description')
#             # products = request.POST.getlist('product_name')  # Corrected to match HTML field name
#             # product_brands = request.POST.getlist('product_brand')  # Corrected to match HTML field name
#             # wattage = request.POST.getlist('wattage')  # Corrected to match HTML field name
#             # discount = request.POST.getlist('discount')  # Corrected to match HTML field name

#             # Create a new Product object and save it to the database
#             product = Product(
#                 price=price,
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email,
#                 phone=phone,
#                 # description=description,
#                 # solar_panel=('Solar Panel' in products),
#                 # solar_heater=('Solar Heater' in products),
#                 # inverter=('Inverters' in products),  # Adjusted to match the value in the form
#                 # solar_cooker=('Solar Cooker' in products),
#                 # luminous=('luminous' in product_brands),
#                 # loom=('loom' in product_brands),
#                 # hi_mo=('hi-mo' in product_brands),
#                 # less_than_300w=('less300' in wattage),  # Adjusted to match the value in the form
#                 # greater_than_300w=('greater300' in wattage),  # Adjusted to match the value in the form
#                 # discount_10=('10%' in discount),
#                 # discount_20=('20%' in discount),
#                 # discount_30=('30%' in discount)
#             )
            
#             product.save()
#             return HttpResponse("Data inserted successfully!")
#         except Exception as e:
#             return HttpResponse(f"Error: {e}")  # Return an error message if an exception occurs

#     return render(request, 'insert.html')

# views.py

# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import Product  # Replace YourModelName with your actual model name

# def insert_data(request):
#     if request.method == 'POST':
#         # Extract data from POST request
#         first_name = request.POST.get('first_name', '')
#         last_name = request.POST.get('last_name', '')
#         email = request.POST.get('email', '')
#         phone = request.POST.get('phone', '')

#         # Create an instance of your model with extracted data
#         new_entry = Product(first_name=first_name, last_name=last_name, email=email, phone=phone)
        
#         # Save the new entry to the database
#         new_entry.save()

#         return HttpResponse("Data inserted successfully!")  # You can customize this response
#     else:
#         return HttpResponse("Invalid request method!")


# views.py




# views.py

def home(request):
    return render(request, 'home.html')


def home2(request):
    return render(request, 'home2.html')

def more(request):
    return render(request, 'more.html')


def moresolar(request):
    return render(request, 'moresolar.html')


def morebattery(request):
    return render(request, 'morebattery.html')

def morebulb(request):
    return render(request, 'morebulb.html')


def insert(request):
    return render(request, 'insert.html')


@csrf_exempt
def gridview(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    if query:
        categories = categories.filter(Q(title__icontains=query))
        
        # categories = Category.objects.all()

   
    price_filter = request.GET.get('price-group')
    product_filter = request.GET.get('product-group')
    brand_filter = request.GET.get('brand-group')
    discount_filter = request.GET.get('discount-group')
    

   
    filter_conditions = Q()


   
    if price_filter == '1':
        filter_conditions &= Q(price__gte=10000, price__lte=100000)
    elif price_filter == '2':
        filter_conditions &= Q(price__gt=100000, price__lte=200000)
    elif price_filter == '3':
        filter_conditions &= Q(price__gt=200000, price__lte=300000)



    if product_filter == '4':
        filter_conditions &= Q(solar_panel=True)
    elif product_filter == '5':
        filter_conditions &= Q(inverter=True)
    elif product_filter == '6':
        filter_conditions &= Q(solar_heater=True)
    elif product_filter == '7':
        filter_conditions &= Q(solar_cooker=True)
        
    if brand_filter == '8':
        filter_conditions &= Q(luminous=True)
    elif brand_filter == '9':
        filter_conditions &= Q(loom=True)
    elif brand_filter == '10':
        filter_conditions &= Q(hi_mo=True)
    
    if  discount_filter == '11':
        filter_conditions &= Q(discount_10=True)
    elif  discount_filter == '12':
        filter_conditions &= Q(discount_20=True)
    elif  discount_filter == '13':
        filter_conditions &= Q(discount_30=True)
        
    categories = categories.filter(filter_conditions)
    
    return render(request, 'gridview.html', {'categories': categories})

@custom_login_required
def productpage(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        buy1=request.POST.get('buy')
        cart1=request.POST.get('cart')
        if cart1 is not None:
            category.cart=user_id 
            category.save()
        if buy1 is not None:
            category.buy = user_id
            category.arrival_time = datetime.now().date() + timedelta(days=7)
            category.status = "under delivery"
            category.save()
            return redirect('payment_page', category_id=category_id)
    return render(request, 'productpage.html', {'category': category})


@custom_login_required
def profilepage(request):
   
    user_id = request.session.get('user_id')
    print(user_id)
    
    user_data = None
    
    try:
        cart = Category.objects.filter(cart=user_id)
        buy = Category.objects.filter(buy=user_id)
        print(cart)
        user_data = User.objects.get(id=user_id)
    except User.DoesNotExist:
        pass
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        address = request.POST.get('address')
        password = request.POST.get('password')
       
        if user_data:
            user_data.name = name
            user_data.email = email
            user_data.phone_number = phone_number
            user_data.city = city
            user_data.address = address
            user_data.password = password

            user_data.save()

            return redirect('profilepage')
        else:
            pass
    return render(request, 'profilepage.html', {'user_data': user_data,'cart':cart,'buy':buy})
  
  
def custom_admin_required(view_func):
    def _warapped_view(request, *args, **kwargs):
        if not request.session.get('is_admin', False):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _warapped_view

@custom_admin_required
def adminpage(request):
    users = User.objects.all()
    category_list = Category.objects.all()
    if request.method == 'POST':
       
        pimg = request.FILES.get('pimg')
        price = request.POST.get('price')
        wattage = request.POST.get('wattage')
        voltage = request.POST.get('voltage')
        warrenty = request.POST.get('warrenty')
        title = request.POST.get('title')
        description = request.POST.get('description')
        product_name = request.POST.get('product_name')
        product_brand = request.POST.get('product_brand')
        discount = request.POST.get('discount')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

     
        category = Category(
            pimg=pimg,
            price=price,
            wattage=wattage,
            voltage=voltage,
            warrenty=warrenty,
            title=title,
            description=description,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
       
       
        if product_name == "1":
            category.solar_panel = True
        elif product_name == "2":
            category.solar_heater = True
        elif product_name == "3":
            category.inverter = True
        elif product_name == "4":
            category.solar_cooker = True

        if product_brand == "5":
            category.luminous = True
        elif product_brand == "6":
            category.loom = True
        elif product_brand == "7":
            category.hi_mo = True

        if discount == "8":
            category.discount_10 = True
        elif discount == "9":
            category.discount_20 = True
        elif discount == "10":
            category.discount_30 = True

        category.save()

        return redirect('adminpage') 
    return render(request, 'adminpage.html', {'users': users , 'category_list': category_list})

def delete_user(request):
   
    if request.method == 'POST':
        id =  request.POST.get("uid")
        btn = request.POST.get("btn")
        user = User.objects.get(id=id)
        button_dlt=request.POST.get("dlt")
        button_upt=request.POST.get("upt")
        if  button_upt  is not None:
             user.is_admin=request.POST.get("is_admin") == 'on'
             user.save()
            # is_admin = request.POST.get("is_admin")
            # if is_admin == 'true':
            #     user.is_admin = True
            #     user.save()
            # else:
            #     user.is_admin = False
            #     user.save()
        
        elif button_dlt is not None:
            user.delete()
        
    return  redirect(reverse('adminpage'))

def delete_category(request):
    
    if request.method == 'POST':
        id =  request.POST.get("pid")
        btn = request.POST.get("btn")
        user = Category.objects.get(id=id)
        
        user.delete()
        
    return  redirect(reverse('adminpage'))

def reset(request):
    if request.method == 'POST':
        button_rst=request.POST.get("btn_reset")
        if button_rst is not None:
            product=Category.objects.filter(arrival_time=timezone.now().date()) 
            for i in product:
                i.status="-"
                i.arrival_time=None   
                i.save()  
    return redirect(reverse('adminpage'))

def  aboutus_page(request):
    return render(request, 'aboutus_page.html')

def  admin_user(request):
     users = User.objects.all()
     return render(request, 'admin_user.html', {'users': users})
 
def  admin_category(request):
     category_list = Category.objects.all()
     return render(request, 'admin_category.html', {'category_list': category_list})


def  privacy(request):
    return render(request, 'privacy.html')

def  payment_page(request, category_id):
    price = request.GET.get('price')
    user_id = request.session.get('user_id')
    
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'payment_page.html', {'category': category})

def blog_page(request):
    return render(request, 'blog_page.html')

def otp_page(request):
    
    email = request.session.get('user_email')
    otp = request.session.get('otp')
    phone_number = request.session.get('phone_number')
    cus_msg = "Enter Valid OTP..."
    
    if request.method == 'POST':
       enetr_otp = request.POST.get('otp')
       phone_verification_status = verify_otp_sms(phone_number, enetr_otp)
       
       if enetr_otp==otp or phone_verification_status == 'approved':
            del request.session['otp']
            del request.session['user_email'] 
            del request.session['phone_number']
        
            messages.success(request, 'OTP verified. You are now logged in.')
            return redirect('login') 
       else:
            cus_msg = "~ Invalid OTP or User"

    return render(request, "otp_page.html",{'cus_msg': cus_msg})  
 




def  user_list(request):
      
        
    user_id = request.session.get('user_id')
    
    categories = Category.objects.filter(owner_id=user_id)
    
    return render(request, 'user_list.html', {'categories': categories})
   
   
def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        description1 = request.POST.get('description1')

        new_contact = Contact(name=name, 
                              email=email, 
                              phone_number=phone_number, 
                              city=city, 
                              description1=description1)
        new_contact.save()
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contactus')
    return render(request, 'contactus.html')


def payout_success(request):
    return render(request, 'payout_success.html')

def cart(request):
    user_id = request.session.get('user_id')
    cart = Category.objects.filter(cart=user_id)
    return render(request, 'cart.html',{'cart': cart})

def cart(request):
    user_id = request.session.get('user_id')
    carts = Category.objects.filter(cart=user_id)
    if request.method=='POST':
        carts.update(cart=0)
        return redirect('cart')
    return render(request, 'cart.html',{'carts': carts})

def success(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    buy_items = Category.objects.filter(buy=user_id)
    return render(request, 'success.html', {'user': user, 'buy_items': buy_items})
    # return render(request, 'success.html', {'user': user, 'category': category})

def generate_gstin():
    """Generate a random GSTIN-like number (15 characters)."""
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    gstin = '27'  # Maharashtra state code
    gstin += ''.join(random.choices(chars + digits, k=10))
    gstin += '1Z'
    gstin += random.choice(chars)
    return gstin

def generate_invoice(request, category_id):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    product = get_object_or_404(Category, pk=category_id)

    original_price = product.price

    # Determine discount
    discount_rate = 0
    if product.discount_10:
        discount_rate = 10
    elif product.discount_20:
        discount_rate = 20
    elif product.discount_30:
        discount_rate = 30

    discount_amount = (discount_rate / 100) * original_price
    discounted_price = original_price - discount_amount

    # GST Calculation (18%)
    gst_rate = 18
    gst_amount = (gst_rate / 100) * discounted_price
    final_price = discounted_price + gst_amount

    invoice_id = f"INV-{random.randint(100000, 999999)}"
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    gst_number = generate_gstin()

    # Save Invoice
    invoice = Invoice.objects.create(
        invoice_id=invoice_id,
        date=current_date,
        time=current_time,
        name=user.name,
        phone=user.phone_number,
        city=user.city,
        address=user.address,
        title=product.title,
        price=product.price,
        discount_10=product.discount_10,
        discount_20=product.discount_20,
        discount_30=product.discount_30,
        gstin=gst_number,
        total=final_price,
        arrival_time=product.arrival_time,
        status=product.status
    )

    context = {
        'user': user,
        'product': product,
        'invoice_id': invoice_id,
        'current_date': current_date.strftime("%d-%m-%Y"),
        'current_time': current_time.strftime("%I:%M %p"),
        'original_price': original_price,
        'discount_rate': discount_rate,
        'discount_amount': discount_amount,
        'discounted_price': discounted_price,
        'gst_rate': gst_rate,
        'gst_amount': gst_amount,
        'final_price': final_price,
        'gst_number': gst_number,
        'arrival_time': product.arrival_time,
        'status': product.status
    }

    return render(request, 'generate_invoice.html', context)

def ordered_item(request):
    user_id = request.session.get('user_id')
    buys = Category.objects.filter(buy=user_id)
    if request.method=='POST':
        buys.update(buy=0)
        return redirect('ordered_item')
    return render(request, 'ordered_item.html',{'buys': buys})

def cart_added(request):
    return render(request, 'cart_added.html')







# def clear(request):
    
#     return redirect(request, 'ordered_item.html',{'orders':orders})

def admin_invoice(request):
    invoice_list = Invoice.objects.all().order_by('-date', '-time')  # Show latest first
    return render(request, 'admin_invoice.html', {'invoice_list': invoice_list})

@csrf_exempt
def reset_invoice(request):
    if request.method == 'POST':
        Invoice.objects.all().delete()
    return redirect('admin_invoice')

@csrf_exempt
def delete_invoice(request):
    if request.method == 'POST':
        invoice_id = request.POST.get('invoice_id')
        invoice = get_object_or_404(Invoice, id=invoice_id)
        invoice.delete()
    return redirect('admin_invoice')