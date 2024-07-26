from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager 
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.utils import timezone


class Usermanager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):  
 
        if not email:  
            raise ValueError(('The Email must be Required'))  
        email = self.normalize_email(email)  
          
        user = self.model(email=email, **extra_fields)  
        user.set_password(password)  
        user.save(using=self._db)
        return user 
                                              
    
    def create_superuser(self, email, password, **extra_fields): 
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True)  
        extra_fields.setdefault('is_active', True) 

        if extra_fields.get('is_staff') is not True:  
            raise ValueError(('Superuser must have is_staff=True.'))
        
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50) 
    address = models.CharField(max_length = 200)
    email = models.EmailField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = Usermanager()    


class Book(models.Model):
    book_name = models.CharField(max_length=150)
    author_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    subject = models.CharField(max_length=200,blank = True)    

    # def __str__(self):
    #     return self.id
    #    return str(self.id) + " " + str(self.book_name)


class IssuedBook(models.Model):  
    
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=date.today(), blank=False)
    # issue_date = models.DateTimeField(default=timezone.now())
    return_date = models.DateField(blank=True, null=True)
    # return_date = models.DateTimeField(default=timezone.now())
    # models.DateTimeField(default=timezone.now)   use

    # def __str__(self) :
    #     return str(self.book_id)




