from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import CustomUser,Book, IssuedBook
from .forms import CustomUserForm , BookForm, Filter_Form, IssuedBookForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login as log_user, logout as lgout
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.utils.dateparse import parse_datetime
# import django.utils.timezone.now






# def Register(request):  

#     if request.method == "POST":       
#         data = request.POST
#         print('====dd======',data['email'])

#         fm = CustomUserForm(request.POST)  
        
#         if fm.is_valid():  
#             # user = data['email']
#             # user.set_password('password')

#             fm.save()

 
#     else:  
#         fm = CustomUserForm()  
#         # data = CustomUser.objects.all()
#     return render(request,'home.html',{'fm':fm})  

# from django.http import HttpResponse, HttpResponseNotFound
def Register(request):
    
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        address = request.POST["address"]

        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        
        if password1 == password2:
           
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, "Email already registered")
                return redirect("register")
            
            else:
                
                user = CustomUser.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    address=address,
                    password=password1
                )

                user.set_password(password1)
                user.save()

                from django.core.mail import EmailMultiAlternatives

                subject, from_email, to = 'Library Account Registaration Sucessful', 'akp181097@gmail.com', 'akashkedariya007@gmail.com'
                text_content = 'This is an important message.'
                html_content = '<body><h2>User registration to Library,<h2><br> Now you can take Book from Library </body>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # subject = 'User registration to Library'
                # message =  HttpResponseNotFound("<h1>Page not found</h1>")
                # # message = f'<html lang="en"><head><meta charset="utf-8"><title>Am I HTML already?</title></head><body>Yes,<br>I am!</body></html>'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [email, ]
                # send_mail( subject, message, email_from, recipient_list )
               
                return redirect("login")
        else:
           
            messages.info(request, "Password not matches")
            return redirect("register")
    else:
        
        return render(request, "home.html")



def login(request):
   
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            log_user(request, user)
           
            return redirect("show_book")
        else:
    
            messages.info(request, "Invalid Credential")
            return redirect("login")
    else:
        
        return render(request, "login.html")
    
def logout(request):
    # Logout user and redirect to home page
    lgout(request)
    return redirect("login")    



def add_book(request):  

    if request.method == "POST":  
        data = request.POST
        # print('============data=============',data)
        fm = BookForm(request.POST)  

        if fm.is_valid():

            book_name = fm.cleaned_data['book_name']
            author_name = fm.cleaned_data['author_name']
            quantity = fm.cleaned_data['quantity']
            subject = fm.cleaned_data['subject']
            print('============book_name=============',book_name)

            Book.objects.create(book_name = book_name, author_name = author_name, quantity =quantity, subject = subject )
            
            return redirect("show_book")
 
    else:  
        fm = BookForm()  
    
    return render(request,'add_book.html',{'fm':fm})


@login_required(login_url="login")
def book_update(request,pk=None):
   
    if request.method == 'POST':
        print('=======request.user=======',request.user)
        pi = Book.objects.get(id=pk)
        form = BookForm(request.POST,instance=pi)  
        if form.is_valid():
            form.save()
            return redirect("show_book")
            
    else:
        
        pi = Book.objects.get(id=pk)
        form = BookForm() 

    return render(request,'update_book.html',{'form':form})  


@login_required(login_url="login")
def show_book(request) :
    if request.method == 'GET' :
        superusers = CustomUser.objects.get(is_superuser=True)
        print('[============superusers==============]',superusers)
        book_data = Book.objects.all()
    
    return render(request,"show_book.html",{'book_data' : book_data ,'superusers': superusers})   


def get_username(self):
    all_users = CustomUser.objects.all()
    for usr in all_users:
        if self == usr:
            data = usr.username
    return data

def get_bookname(self):
    all_book = Book.objects.all()
    for usr in all_book:
        # print('=======usr====',usr)
        if self == usr:
            data = usr.book_name
    return data


# @login_required(login_url="login")
# def issues_book_histry(request) :
#     if request.method == 'GET' :
#         history_list = []
#         book_data = IssuedBook.objects.all()
#         for bk_user in book_data:
    
#             # print('========bk_user== =====',bk_user.user_id) 
#             get_data = get_username(bk_user.user_id)
#             get_book = get_bookname(bk_user.book_id)
#             print(bk_user.user_id,'========',get_data)
#             print(bk_user.user_id,'========',get_book)

#             history = {
#                 'user_id':get_data,
#                 'book_id':get_book,
#                 'issue_date':bk_user.issue_date,
#                 'return_date':bk_user.return_date,

#             }
#             history_list.append(history)
#         # print('========history_list=====',history_list)    

#     return render(request,"issue_book_histry.html",{'book_data' : history_list })  


@login_required(login_url="login")
def issues_book_histry(request) :
    if request.method == 'GET' :

        book_data = IssuedBook.objects.all()

    return render(request,"issue_book_histry.html",{'book_data' : book_data }) 


def issue_books(request,pk=None) :
    
    if request.method == 'POST':       
        book = Book.objects.get(id=pk)

        if book.quantity == 0 :
            messages.add_message(request, messages.INFO, '<h4>No book found </h4>')

        else :
            value = book.quantity - 1
            Book.objects.filter(id = pk).update(quantity = value)
                         
        book_data = Book.objects.all()
        
    return render(request,"show_book.html",{'book_data' : book_data})    
        


@login_required(login_url="login")
def filter_book(request):
    if request.method == 'POST':
        data = request.POST

        if data['book_name'] :
            book_data = Book.objects.filter(book_name = data['book_name'])

        elif data['index'] :
            book_data = Book.objects.filter(id = data['index'])  
    else :
        book_data = Book.objects.all()
        
    return render(request,"book_filter.html",{'book_data' : book_data})


def delete_book(request, pk=None) :

    if request.method == 'POST':
        data = Book.objects.get(id=pk)
        data.delete()
        return redirect('show_book')


def issue_bk(request):
    if request.method == 'POST':
        data = request.POST
        form = IssuedBookForm(request.POST)
       
        if form.is_valid():
            form.save()

            qun = Book.objects.get(id=data['book_id'])
            count = qun.quantity - 1        
            Book.objects.filter(id=data['book_id']).update(quantity=count)

            subject = 'Issues Books to reader'
            message = f'Hello,  This book is your... Please read the book and give to the library before end date '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user, ]
            send_mail( subject, message, email_from, recipient_list )

            form = IssuedBookForm()

    else:
        form = IssuedBookForm()                                     
            
        return render(request, "issue_book.html",{'form':form})


def return_book(request):
    if request.method == 'POST' :
        book_id = request.POST['book_id']

        demo = IssuedBook.objects.get(id=book_id)
        print('============demo=======',demo)

        data = Book.objects.all()    
        match_book = [x.quantity for x in data if str(x) == book_id]
    
        if match_book:
            data = Book.objects.get(id=book_id)
            count = data.quantity + 1
           
            Book.objects.filter(id = book_id).update(quantity=count)
            return redirect('show_book')
                        
        else:
            
            messages.info(request, "This book code is not available in Library ")
            return render(request, "return_book.html")

    else:

        return render(request, "return_book.html")    



# def issue_bk(request):
#     if request.method == 'POST':
        
#         user_id = request.POST["user_id"]
#         # user_id = request.user
#         book_id = request.POST["book_id"]
#         issue_date = request.POST["issue_date"]
#         return_date = request.POST["return_date"]
#         print('=======user_id============',user_id,book_id,issue_date,return_date)

#         # today_time = datetime.datetime.now()      
#         # print("========= today time=====",today_time)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
#         # print("======current_time======",current_time.time())

#         # posted = timezone.now()
#         # checkinTime = time.localtime()

#         # parser_date = dateutil.parser.parse(str(today_time))
#         # print("======parser_date======",parser_date,type(parser_date))

#         # formatted_datetime = parse_datetime(str(today_time)).strftime('%Y-%m-%d %H:%M:%S')
#         # print("=======formated time======",formatted_datetime)

#         IssuedBook.objects.create(user_id=user_id,book_id=book_id,issue_date=issue_date,return_date=return_date)

#     else:
#         return render(request, "issue_book.html")