from .models import CustomUser, Book, IssuedBook
from django import forms 
# from django.forms import ModelForm
  
# creating a form 
class CustomUserForm(forms.ModelForm): 
    class Meta:
        model = CustomUser
        fields = [ 'username','first_name','last_name','address','email','password' ]  


class BookForm(forms.ModelForm): 
    class Meta:
        model = Book
        fields = [ 'id','book_name','author_name','quantity','subject' ] 


class IssuedBookForm(forms.ModelForm): 
    class Meta:
        model = IssuedBook
        fields = [ 'user_id','book_id','issue_date','return_date' ]         


class Filter_Form(forms.Form):
    book_name = forms.CharField(max_length=100)  
    # book_name = forms.CharField(max_length=100)             

