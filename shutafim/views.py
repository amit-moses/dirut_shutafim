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
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
import random
  
class Recaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label="")
    
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

def send_vaildation_email(email, name, user_id, token):
    mes = f'שלום {name}, \n תודה שנרשמת לאתר! רצינו לוודא שזה באמת המייל שלך מאחר ותוכל להגדיר שאתה מעוניין לקבל הודעות ממשתמשים שיתעניינו בדירות שתפרסם באתר.\n על מנת להשלים את תהליך ההרשמה יש ללחוץ על הקישור המופיע במייל זה. לאחר לחיצה עליו, חשבונך יופעל.\n הקישור: \n{settings.MY_URL}vaild/{user_id}/{token} \n תודה!'
    send_email(email, 'אימות כתובת המייל' ,mes)

def get_max_id():
    query = Apartment.objects.order_by('-id')
    if query: return query.first().id
    else: return 0

def index(request):
    sort_val = request.GET.get('sort_val',0)
    city = request.GET.get('city_choice','')
    street = request.GET.get('street_choice','')
    rent_price_from = request.GET.get('rent_price_from','')
    rent_price_to = request.GET.get('rent_price_to','')
    gender = request.GET.get('gender','')
    search_key = request.GET.get('search_key','')
    floor = request.GET.get('floor','')
    partners = request.GET.get('partners','')
    entry_month = request.GET.get('entry_month','')
    kosher = request.GET.get('kosher',0)
    type = request.GET.get('type',0)
    search_value = {'city': city, 'street': street, 'rent_price_from': rent_price_from, 
                    'rent_price_to': rent_price_to, 'gender':gender, 'search_key':search_key, 'entry_month':entry_month,
                    'floor':floor, 'partners':partners, 'kosher': kosher, 'type':type}
    return render(request, 'index.html', {'apr':search_value, 'sort_val': int(sort_val),'max_index':get_max_id(), 'title_page':'dirot-shutafim'})

@login_required
def api(request, apr_id = -1):
    user = request.user
    if user: 
        if user.last_name != '1': return render(request, 'login.html', {'log': 'נא לאמת את כתובת המייל באמצעות מייל לאימות סיסמא שנשלח אליך בעת ההרשמה', 'title_page':'התחברות'})
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
        kosher = request.POST.get('kosher')
        agree_mail = request.POST.get('agree_mail')
        type = request.POST.get('type')
        images, urlsexist = [], []
        for k in range(0,6):
            img = request.FILES.get('image'+str(k))
            if img: images.append(img)

        if apr_id == -1:
            
            newApr = Apartment(publisher=request.user, city = city, street=street, rent_price= rent_price, floor = floor, partners= partners, 
                                gender = gender, entry_date = entry_date, details=details, title = title, kosher = kosher, agree_mail = bool(agree_mail), type = type)
            newApr.save()
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
                    apr.kosher = kosher
                    apr.agree_mail = bool(agree_mail)
                    apr.type = type
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
    user = request.user
    if user.is_authenticated: 
        if user.last_name != '1': 
            return render(request, 'login.html', {'log': 'נא לאמת את כתובת המייל באמצעות מייל לאימות סיסמא שנשלח אליך בעת ההרשמה', 'title_page':'Log-in'})
        elif request.method == 'GET':
            if apr_id >0:
                apr = Apartment.objects.filter(pk = apr_id).all()
                if apr: 
                    apr = apr[0]
                    if apr.publisher.id == user.id: return render(request, 'addmanage.html', {'apr': apr, 'rdate':apr.entry_date.strftime('%Y-%m-%d'), 'title_page':f'עריכה: {apr.title}'})
                    else: 
                        return redirect('myads')
            return render(request, 'addmanage.html', {'apr': False, 'date_d': False, 'title_page':'הוספת מודעה'})

def single_page_view(request, apr_id):
    apr = Apartment.objects.filter(pk = apr_id).all()
    if apr: 
        apr = apr[0]
        context = {'apr': apr, 'form': Recaptcha(), 'title_page':apr.title}
        return render(request, 'singlepage.html', context)
    else: return render(request, '404.html')

@login_required
def myads(request):
    user = request.user
    if user: 
        if user.last_name != '1': return render(request, 'login.html', {'log': 'נא לאמת את כתובת המייל באמצעות מייל לאימות סיסמא שנשלח אליך בעת ההרשמה', 'title_page':'Log-in'})
    context = {'apartments': Apartment.objects.filter(publisher = request.user.id).all(), 'title_page':'המודעות שלי'}
    return render(request, 'myads.html', context)

def search(request):
    last_index = int(request.GET.get('last_index',0))
    page = int(request.GET.get('page',1))
    sort_val = request.GET.get('sort_val',0)
    city = request.GET.get('city_choice')
    street = request.GET.get('street_choice')
    rent_price_from = request.GET.get('rent_price_from')
    rent_price_to = request.GET.get('rent_price_to')
    gender = request.GET.get('gender')
    search_key = request.GET.get('search_key')
    entry_month = request.GET.get('entry_month')
    floor = request.GET.get('floor')
    partners = request.GET.get('partners')
    kosher = request.GET.get('kosher')
    type = request.GET.get('type')
    query = Apartment.objects
    if rent_price_from: query = query.filter(rent_price__gte = int(rent_price_from))
    if rent_price_to: query = query.filter(rent_price__lte  = int(rent_price_to))
    if floor: query = query.filter(floor = floor)
    if partners: query = query.filter(partners = partners)
    if gender: 
        if int(gender) != 3: query = query.filter(gender  = int(gender))
    if kosher:
        if int(kosher) != 4: query = query.filter(kosher  = int(kosher))
    if type:
        if int(type) != 3: query = query.filter(type  = int(type))
    if entry_month: query = query.filter(entry_date__month = int(entry_month.split('-')[1])) 
    if city: 
        query = query.filter(city__iexact  = city) 
        if street: 
            query = query.filter(street__iexact = street)
    if search_key:
        query = query.filter(details__icontains = search_key) | query.filter(title__icontains = search_key)
    
    sort_key = 'id'
    sort_val = int(sort_val)
    if sort_val == 2 or sort_val == 3: sort_key = 'rent_price'
    elif sort_val == 4 or sort_val == 5: sort_key = 'partners'
    elif sort_val == 6 or sort_val == 7: sort_key = 'entry_date'
    elif sort_val == 8 or sort_val == 9: sort_key = 'floor'
    if sort_val % 2 == 0: sort_key = '-'+sort_key
    query = query.filter(id__lte = last_index)
    return JsonResponse([k.toJSON() for k in query.order_by(sort_key)[12*(page - 1):12*page]], safe=False)

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        firstname = request.POST.get('firstname')
        email = request.POST.get('email')
        msg = []
        if username:
            if len(username) < 4: msg.append('שם המשתמש צריך להכיל לפחות 4 תווים')
        if User.objects.filter(email = email).all(): msg.append('מייל זה נמצא בשימוש')
        if User.objects.filter(username = username).all(): msg.append('שם משתמש זה נמצא בשימוש')
        elif repassword == password and password and username and email and firstname:
            try:
                options = 'Aa5B1b2C3r4Df5q6E4o7u28F9Q1mRS'
                vaildation = [options[random.randint(0, len(options)-1)] for k in range(16)]
                user = User.objects.create_user(username=username, email=email, first_name = firstname, last_name = ''.join(vaildation), password=password)
                user.save()
            except Exception as e:
                msg.append(e)
            user1 = authenticate(request, username = username, password = password)
            if user1:
                login(request, user1)
                send_vaildation_email(user1.email,user1.first_name, user.id, user1.last_name)
                return render(request, 'login.html', {'reset':'שלחנו לך מייל לאימות כתובת המייל שהזנת, מאחר שתוכל לבחור לקבל מיילים ממתעניינים בדירה נבקש לאשר שזאת כתובת המייל שלך. תודה', 'title_page':'Log-in'})
        elif repassword != password: msg.append('הסיסמאות לא תואמות')
        if not username or not password or not firstname or not firstname or not email:
            msg.append('נא למלא את כל השדות')

        return render(request, 'login.html', {'username2': username, 'email': email, 'firstname':firstname, 'reg': 'reg', 'msg':msg, 'title_page':'Log-in'})

def login_page(request):
    user = request.user
    if user.is_authenticated: 
        if user.last_name != '1': 
            if request.method == 'GET': 
                return render(request, 'login.html', {'title_page':'Log-in'})
            else: 
                return render(request, 'login.html', {'log': 'נא לאמת את כתובת המייל באמצעות מייל לאימות סיסמא שנשלח אליך בעת ההרשמה', 'title_page':'Log-in'})
        else: return redirect('index')
        
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            if user.last_name != '1': return render(request, 'login.html', {'log': 'נא לאמת את כתובת המייל באמצעות מייל לאימות סיסמא שנשלח אליך בעת ההרשמה', 'title_page':'Log-in'})
            else: return redirect('index')
        else:
            messages.error(request, f"log")
        return render(request, 'login.html', {'username1': username, 'log': 'כנראה הזנת שם משתמש או סיסמא לא נכונים', 'title_page':'Log-in'})
    
    next = request.GET.get('next')
    if next:
        mes = ''
        if next== '/rest_password_sent/': mes = 'אם המייל שהזנת רשום, נשלח אליך קישור לאיפוס הסיסמא, נא לבדוק בתיבת המייל או בתיבת הודעות הספאם'
        elif next == 'set': mes = 'סיסמתך שונתה בהצלחה, ניתן להתחבר' 
        return render(request, 'login.html', {'reset': mes , 'title_page':'Log-in'})
    return render(request, 'login.html', {'title_page':'Log-in'})

def logout_page(request):
    logout(request)
    return redirect('index')

def send_email_to_publisher(request, apr_id = 0):
    form = Recaptcha(request.POST)
    mes_content = request.POST.get('mes_content')
    mes_from = request.POST.get('mes_from')
    mes_contact = request.POST.get('mes_contact')
    errmes = 1
    apr = Apartment.objects.filter(pk = apr_id).all()
    if apr and apr_id: 
        apr = apr[0]
    for key, error in list(form.errors.items()):
        if key == 'captcha' and error[0] == 'This field is required.':
            errmes = 3
    if errmes != 3 and request.method == 'POST' and apr:
        if apr.agree_mail:
            user_to = apr.publisher
            mail = f'{user_to.first_name} שלום, \n הושארה לך הודעה בנוגע לדירה שפרסמת באתר \n הדירה: {str(apr)}, {apr.get_url()}\n מאת: {mes_from}\n תוכן ההודעה: {mes_content} \n פרטים ליצירת קשר: {mes_contact} \n \n '
            send_email(user_to.email, f'הודעה חדשה מ{mes_from} בקשר לדירה', mail)
            errmes = 2
    
    context = {'apr': apr, 'errmes': errmes, 'form': Recaptcha(), 'my_name_err': mes_from, 'my_con_err':mes_contact, 'my_mes_err':mes_content, 'title_page':apr.title}
    return render(request, 'singlepage.html', context)

def vaild_account(request, user_id =0, token = None):
    mes = None
    if request.user: 
        if request.user.is_authenticated and request.user.last_name == '1':
            return redirect('index')
    
    if user_id and token:
        user = User.objects.filter(pk = user_id).all()
        if user:
            user = user[0]
            if user.last_name == token:
                user.last_name = '1'
                user.save()
                mes = 'אימות כתובת המייל הושלמה, ניתן להתחבר כעת'
                if request.user.is_authenticated:  return redirect('index')
            elif user.last_name == '1':
                mes = 'נראה שכבר אישרת את כתובת המייל, ניתן להתחבר'
            if mes: 
                return render(request, 'login.html', {'reset': mes, 'title_page':'Log-in'})
    return render(request, 'login.html', {'log': 'שגיאה באימות החשבון', 'title_page':'Log-in'})

# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)