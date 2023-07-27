from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
from django.http import JsonResponse
from shutafim.models import Apartment





# Create your views here.


def index(request):
    context = {'apartments': Apartment.objects.all()}
    return render(request, 'index.html', context)

def myads(request):

    context = {'apartments': Apartment.objects.filter(id = request.user.id).all()}
    return render(request, 'myads.html', context)

def search(request):
    max_id = request.GET.get('max_id')
    city = request.GET.get('city')
    street = request.GET.get('street')
    rent_price_from = request.GET.get('rent_price_from')
    rent_price_to = request.GET.get('rent_price_to')
    gender = request.GET.get('gender')
    search_key = request.GET.get('search_key')
    query = Apartment.objects
    if max_id: query = query.filter(id__lt = max_id)
    if rent_price_from: query = query.filter(rent_price__gte = int(rent_price_from))
    if rent_price_to: query = query.filter(rent_price__lte  = int(rent_price_to))
    if gender: query = query.filter(gender  = int(gender))
    if city: 
        query = query.filter(city__iexact  = city)
        if street: query = query.filter(street__iexact = street)
    if search_key:
        query = query.filter(details__icontains = search_key) | query.filter(title__icontains = search_key)
    
    return JsonResponse([k.toJSON() for k in query.all().order_by('-id').all()], safe=False)
    
    
    

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        msg = []
        if repassword == password and password and username and email and firstname and lastname:
            try:
                user = User.objects.create_user(username=username, email=email, first_name = firstname, last_name = lastname, password=password)
                user.save()
            except Exception as e:
                msg.append(e)
                print(e)
            user1 = authenticate(request, username = username, password = password)
            if user1:
                login(request, user1)
                return redirect('dashboard')
        elif repassword != password: msg.append('the passwords not match')
        if not username or not password or not firstname or not firstname or not email or not lastname:
            msg.append('one of the fields is blank!')

        return render(request, 'login.html', {'username2': username, 'email': email, 'lastname':lastname, 'firstname':firstname, 'reg': 'reg', 'msg':msg})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, f"log")
        return render(request, 'login.html', {'username1': username, 'log': 'log'})
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('index')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

