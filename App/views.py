import base64
from django.utils import timezone 
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect,render

from realEstate import settings
from .models import Notification, Property_type
from .models import Property
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import shutil


# Create your views here.
# Pages starts
def index(request):
    property_list=Property.objects.all()
    properties=Property.objects.filter(status="Available")
    return render(request, "pages/index.html",{'property_list':property_list,'properties':properties})

@login_required
def realEstate_dashboard(request): 
    saved_notification_count = Notification.objects.filter(status="Pending").count()
    new_posts = Notification.objects.filter(status="Pending").all()
    accepted_request=Notification.objects.filter(status="Accepted").count()
    rejected_request=Notification.objects.filter(status="Rejected").count()
    property_in_stock=Property.objects.all().count()
    Total_property_count=property_in_stock+accepted_request

   
    if request.method == 'POST':
        property_type = request.POST.get('propertyType')
        location = request.POST.get('propertyLocation')
        price_range = request.POST.get('priceRange')
        details = request.POST.get('propertyDetails')
        image = request.FILES.get('propertyImage')
        user=request.user

        if property_type and location and price_range and details:
            notification = Notification(
                property_type=property_type,
                location=location,
                price_range=price_range,
                details=details,
                user=user,
               
            )

            if image:
                notification.image = image

            notification.save()
            messages.success(request, 'request sent successfully')          
       
            return redirect ('broker_dashboard')
        
    else:   
        return render(request, "components/overview.html", {'notification':saved_notification_count,'new_posts': new_posts,'accepted_request':accepted_request,'rejected_request':rejected_request,'property_count':Total_property_count,'property_in_stock':property_in_stock})
  
def broker_dashboard(request):
    user=request.user
    notification=Notification.objects.filter(user=user)
    notification_count=Notification.objects.filter(user=user).count()
    
    property=Property_type.objects.all()
    
    messages_list = messages.get_messages(request)
    return render(request,"components/brokers.html",{'property_types': property,'messages': messages_list , 'notifications': notification, 'notification_count': notification_count})
  


def add_property_page(request):
    saved_notification_count = request.session.get('saved_notification_count', 0)
    new_posts = request.session.get('new_posts')
    property=Property_type.objects.all()
    return render(request,"components/add_property.html",{'property_types': property , 'notification':saved_notification_count ,'new_posts': new_posts})
    


def docs_page(request):
    saved_notification_count = request.session.get('saved_notification_count', 0)
    new_posts = request.session.get('new_posts')
    property_list=Property.objects.filter(status="Available")
    return render(request, "components/docs.html",{'property_list':property_list,'notification':saved_notification_count ,'new_posts': new_posts})


def property_table_page(request):
    saved_notification_count = request.session.get('saved_notification_count', 0)
    new_posts = request.session.get('new_posts')
    property_list=Property.objects.all()
    return render(request, "components/property_table.html",{'property_list':property_list,'notification':saved_notification_count ,'new_posts': new_posts})


def property_type_page(request):
    saved_notification_count = request.session.get('saved_notification_count', 0)
    new_posts = request.session.get('new_posts')
    return render(request, "components/add_property_type.html",{'notification':saved_notification_count ,'new_posts': new_posts}
 )

def broker_login_page(request):
    return render(request,'pages/broker_login.html')
def owner_login_page(request):
    return render(request,'pages/owner_login.html')

def broker_register_page(request):
    return render(request,'pages/broker_register.html')

def update_property_page(request,id):
    updateable_property=Property.objects.get(id=id)
    property_type=Property_type.objects.all()
    return render(request,'components/property_update.html',{'updateable_property':updateable_property,'property_types':property_type})

# pages End


# login and register begins
def owner_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)        
            return redirect("realEstate_dashboard")  # Redirect to the dashboard for superusers
        else:
            # Authentication failed, handle the error (e.g., show an error message).
            # return redirect('owner_login_page')
            return HttpResponse('failed')
    else:    


        return render(request,'pages/owner_login.html')
   


def broker_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']
        print(username,password)
        
        
        if password == password2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('broker_login_page')
                # return redirect('broker_login_page')  # Redirect to the login page or another desired page
            else:
                return render(request, 'pages/broker_register.html', {'error': 'Username is already taken.'})
        else:
            return render(request, 'pages/broker_register.html', {'error': 'Passwords do not match.'})
    else:  
        return render('broker_register_page')


def broker_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("broker_dashboard")
            
            # return redirect('#')  
        else:
            return HttpResponse('invalid username or password')
            # error_message = 'Invalid username or password.'

    return render(request, 'pages/broker_login.html')
    # return render(request,'pages/login.html')


# login and register ends here


# insertion begin
def property_type_db(request):
    if request.method == "POST":
        type = request.POST.get("property_type")
        try:
            existing_property = Property_type.objects.filter(property_type=type).first()
            if existing_property:
                messages.error(request, 'Data already exists',extra_tags='error')
                return HttpResponse('already existed')
            else:
                property = Property_type(property_type=type)
                property.save()
                messages.success(request, 'Data saved successfully',extra_tags='success')
                return redirect('property_type_page')
            
        except Exception as e:
            messages.error(request, f'Insertion failed: {str(e)}')
            return redirect("property_type_page")
    else:
        return redirect("property_type_page")
    


def property_db(request):
    if request.method == 'POST':
        type = request.POST.get('propertyType')
        location = request.POST.get('propertyLocation')
        price = request.POST.get('priceRange')
        details = request.POST.get('propertyDetails')
        image = request.FILES['propertyImage']

        


        property = Property(property_type=type, location=location, price_range=price, image=image, details=details)
        property.save()       
   
        return redirect("add_property_page")
    else:
        return HttpResponse("insertion failed")


           


    


# insertion ends

# search Begins
def property_search(request):
    properties=Property.objects.all()
    if request.method=='POST':
     type=request.POST.get('property_type')
     location=request.POST.get('location')
     price=request.POST.get('price_range')
     filters={}
     if type:
        filters['property_type__icontains'] = type  # Case-insensitive text search

     if location:
        filters['location__icontains'] = location  # Case-insensitive text search

     if price:
        filters['price_range'] = price  # Filter properties with price less than or equal to the provided value

     properties = Property.objects.filter(**filters)
     if properties:
        return render( request, './pages/search_result.html',{'properties':properties})
     else:
         return HttpResponse("search result not found")
    # else:
    #   return redirect( 'index')
# search end

# updation begins
def property_update_db(request, id):
    if request.method=='POST':        
        type=request.POST.get('propertyType')
        location=request.POST.get('propertyLocation')
        price=request.POST.get('priceRange')
        image=request.FILES.get('propertyImage')
        details=request.POST.get('propertyDetails')
      
        try:
          property=Property.objects.get(id=id) 
          property.property_type=type
          property.location=location
          property.price_range=price
          property.details=details
          if image:
            property.image=image 

          property.save()
          return HttpResponse("updated successfully")

         
        except property.DoesNotExist:
          return HttpResponse("property not found")
               
        
        
    else:
        return redirect ("update_property_page")
# updation ends

#deletion begins
def delete_property(request,id):
    property=Property.objects.get(id=id)
    property.delete()
    return redirect('property_table_page')

   

#deletion ends
#notification Begins
def accept_notification(request, notification_id):
    if request.method=='POST':
        notification = Notification.objects.get(pk=notification_id)
     
        notification.status = 'Accepted'
        notification.save()
        type=request.POST.get('propertyType')
        location=request.POST.get('propertyLocation')
        price=request.POST.get('priceRange')
        image=request.FILES.get('propertyImage')
      
        print(image)
        details=request.POST.get('propertyDetails')
        saved_notification=Property(property_type=type, location=location, price_range=price, image=image, details=details )
        saved_notification.save()
       

        
        
        return redirect(realEstate_dashboard)
    else:
        return HttpResponse("failed")



def reject_notification(request, notification_id):
    notification = Notification.objects.get(pk=notification_id)
    notification.status = 'Rejected'
    notification.save()
    return redirect('realEstate_dashboard')
#notification Ends

#sales begins
def mark_property_as_sold(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    property.status = 'Sold'
    property.sold_time = timezone.now() 
    property.save()
    return redirect('docs_page')
#sales ends



#logout begins
def log_out(request):
    logout(request)
    return redirect('owner_login')
#logout ends