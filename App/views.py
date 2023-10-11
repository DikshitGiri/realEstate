from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Property_type
from .models import Property
from django.contrib import messages


# Create your views here.
# Pages starts
def index(request):
    return render(request, "pages/index.html")


def realEstate_dashboard(request):
    return render(request, "components/overview.html")


def add_property_page(request):
    property=Property_type.objects.all()
    return render(request,"components/add_property.html",{'property_types': property})
    


def docs_page(request):
    property_list=Property.objects.all()
    return render(request, "components/docs.html",{'property_list':property_list})


def property_table_page(request):
    property_list=Property.objects.all()
    return render(request, "components/property_table.html",{'property_list':property_list})


def property_type_page(request):
    return render(request, "components/add_property_type.html")


# pages End


# login and register begins
def estate_owner_login(request):
    return HttpResponse("welcome sir")


def broker_register(request):
    return HttpResponse("reg here")


def broker_login(request):
    return HttpResponse("hello broker")


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
                return HttpResponse('succeed')
            
        except Exception as e:
            messages.error(request, f'Insertion failed: {str(e)}')
            return redirect("property_type_page")
    else:
        return redirect("property_type_page")
    
def property_db(request):
    if request.method=='POST':        
        type=request.POST.get('propertyType')
        location=request.POST.get('propertyLocation')
        price=request.POST.get('priceRange')
        image=request.FILES.get('propertyImage')
        details=request.POST.get('propertyDetails')
        print(type,location,image)
        try:
            property= Property(property_type=type, location=location,price_range=price,image=image,details=details)
            property.save()
            return HttpResponse("insertion successfull")
        except Exception as e:
            return HttpResponse("failed")
        
        
        
    else:
        return redirect ("add_property_page")

           


    


# insertion ends
# retrival Begins



# retrival ends
