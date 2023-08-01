from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from shutafim.models import Apartment, ImageData
from django.core.mail import EmailMessage, get_connection
from django.conf import settings


def index(request):
    # max_id = request.GET.get('max_id')
    city = request.GET.get('city_choice')
    street = request.GET.get('street_choice')
    rent_price_from = request.GET.get('rent_price_from')
    rent_price_to = request.GET.get('rent_price_to')
    print('s3',rent_price_from, rent_price_to)
    gender = request.GET.get('gender')
    search_key = request.GET.get('search_key')
    print(gender, 'mmmm')
    floor = request.GET.get('floor')
    partners = request.GET.get('partners')
    entry_month = request.GET.get('entry_month')
    search_value = {'city': city if city else '', 'street': street if street else '', 'rent_price_from': rent_price_from, 
                    'rent_price_to': rent_price_to, 'gender':gender, 'search_key':search_key if search_key else '', 'entry_month':entry_month,
                    'floor':floor, 'partners':partners, }
    return render(request, 'index.html', {'apr':search_value})

@login_required
def api(request, apr_id = -1):
    if request.method == 'POST':
        city = request.POST.get('city_choice')
        street = request.POST.get('street_choice')
        floor = request.POST.get('floor')
        gender = request.POST.get('gender')
        entry_date = request.POST.get('entey_date')
        partners = request.POST.get('partners')
        rent_price = request.POST.get('rent')
        title = request.POST.get('title')
        details = request.POST.get('details')
        images, urlsexist = [], []
        for k in range(0,6):
            img = request.FILES.get('image'+str(k))
            if img: images.append(img)

        if apr_id == -1:
            newApr = Apartment(publisher=request.user, city = city, street=street, rent_price= rent_price, floor = floor, partners= partners, 
                                gender = gender, entry_date = entry_date, details=details, title = title)
            newApr.save()
            print('1111110',images)
            newApr.uploadImages(images)
        elif apr_id:
            apr = Apartment.objects.filter(pk = apr_id).all()
            if apr: 
                apr = apr[0]
                if apr.publisher_id == request.user.id:
                    apr.city = city
                    apr.street=street
                    apr.rent_price= int(rent_price)
                    apr.floor = int(floor)
                    apr.partners= partners
                    apr.gender = int(gender) 
                    apr.entry_date = entry_date
                    apr.details=details
                    apr. title = title
                    apr.save()
                    for k in range(0,6):
                        trp = request.POST.get(f'imagenochange{k}')
                        if trp: 
                            urlsexist.append(trp)
                    apr.updateImages(images, urlsexist)
    return redirect('myads')

@login_required
def delete_apr(request, apr_id=0):
    if apr_id:
        apr = Apartment.objects.filter(pk = apr_id).all()
        if apr:
            apr = apr[0]
            if request.method == 'POST' and apr.publisher_id == request.user.id:
                if apr.imagedata_set: 
                    try:
                        apr.deleteAllImages()
                    finally:
                        apr.delete()

    return redirect('myads')

    

@login_required
def newadd(request, apr_id = -1):
    if request.method == 'GET':
        if apr_id >0:
            apr = Apartment.objects.filter(pk = apr_id).all()
            if apr: 
                apr = apr[0]
                return render(request, 'addmanage.html', {'apr': apr, 'rdate':apr.entry_date.strftime('%Y-%m-%d')})
        return render(request, 'addmanage.html', {'apr': False, 'date_d': False})

def single_page_view(request, apr_id):
    apr = Apartment.objects.filter(pk = apr_id).all()
    if apr: 
        apr = apr[0]
    context = {'apr': apr}
    return render(request, 'singlepage.html', context)

@login_required
def myads(request):
    context = {'apartments': Apartment.objects.filter(publisher = request.user.id).all()}
    return render(request, 'myads.html', context)

def search(request):
    max_id = request.GET.get('max_id')
    city = request.GET.get('city_choice')
    street = request.GET.get('street_choice')
    print(street, '------------11')
    rent_price_from = request.GET.get('rent_price_from')
    rent_price_to = request.GET.get('rent_price_to')
    gender = request.GET.get('gender')
    search_key = request.GET.get('search_key')
    entry_month = request.GET.get('entry_month')
    floor = request.GET.get('floor')
    partners = request.GET.get('partners')

    query = Apartment.objects
    if max_id and max_id != '0': query = query.filter(id__lt = max_id)
    print(rent_price_from, rent_price_to)
    if rent_price_from: query = query.filter(rent_price__gte = int(rent_price_from))
    if rent_price_to: query = query.filter(rent_price__lte  = int(rent_price_to))
    print(query.count(), '--11--')
    if floor: query = query.filter(floor = floor)
    if partners: query = query.filter(partners = partners)
    if gender: 
        print(gender, 'kkkkk')
        if int(gender) != 3: query = query.filter(gender  = int(gender))
    if entry_month: query = query.filter(entry_date__month = int(entry_month.split('-')[1])) 
    if city: 
        query = query.filter(city__iexact  = city) 
        print(street, 'llllllp')
        if street: 
            query = query.filter(street__iexact = street)
    if search_key:
        query = query.filter(details__icontains = search_key) | query.filter(title__icontains = search_key)
    
    return JsonResponse([k.toJSON() for k in query.order_by('-id')[:12]], safe=False)
    
    
    

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
                return redirect('index')
        elif repassword != password: msg.append('the passwords not match')
        if not username or not password or not firstname or not firstname or not email or not lastname:
            msg.append('one of the fields is blank!')

        return render(request, 'login.html', {'username2': username, 'email': email, 'lastname':lastname, 'firstname':firstname, 'reg': 'reg', 'msg':msg})

def login_page(request):
    # send_email('amitm747@gmail.com', 'היי', "מה נשמע?")
    if request.user.is_authenticated:
        return redirect('index')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, f"log")
        return render(request, 'login.html', {'username1': username, 'log': 'log'})
    
    next = request.GET.get('next')
    if next:
        mes = ''
        if next== '/rest_password_sent/': mes = 'אם המייל שהזנת רשום, נשלח אליך קישור לאיפוס הסיסמא, נא לבדוק בתיבת המייל או בתיבת הודעות הספאם'
        elif next == 'set': mes = 'סיסמתך שונתה בהצלחה, ניתן להתחבר' 
        return render(request, 'login.html', {'reset': mes})
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('index')

def send_email(toemail, mysubject, mymessage):  
    with get_connection(  
        host=settings.EMAIL_HOST, 
    port=settings.EMAIL_PORT,  
    username=settings.EMAIL_HOST_USER, 
    password=settings.EMAIL_HOST_PASSWORD, 
    use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = mysubject 
        email_from = settings.EMAIL_HOST_USER  
        recipient_list = [toemail, ]  
        message = mymessage 
        EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()  
    
def send_email_to_publisher(request, apr_id = 0):
    mes_content = request.POST.get('mes_content')
    mes_from = request.POST.get('mes_from')
    mes_contact = request.POST.get('mes_contact')
    apr = Apartment.objects.filter(pk = apr_id).all()
    errmes = 1
    if apr and apr_id: 
        apr = apr[0]
        user_to = apr.publisher
        mail = f'{user_to.first_name} שלום, \n הושארה לך הודעה בנוגע לדירה שפרסמת באתר \n הדירה: {str(apr)}, {apr.get_url()}\n מאת: {mes_from}\n תוכן ההודעה: {mes_content} \n פרטים ליצירת קשר: {mes_contact} \n \n '
        print(mail)
        send_email(user_to.email, f'הודעה חדשה מ{mes_from} בקשר לדירה', mail)
        errmes = 2
    
    context = {'apr': apr, 'errmes': errmes}
    return render(request, 'singlepage.html', context)
