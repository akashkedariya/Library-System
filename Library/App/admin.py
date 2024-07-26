from django.contrib import admin
from.models import CustomUser , Book, IssuedBook
# Register your models here.




@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','address','is_active','is_superuser','email','password']


@admin.register(Book)
class register_employeeAdmin(admin.ModelAdmin):
    list_display = [ 'id','book_name','author_name','quantity','subject' ]

@admin.register(IssuedBook)
class IssuedItemAdmin(admin.ModelAdmin):
    list_display = [ 'id','user_id','book_id','issue_date','return_date' ]


# @admin.register(Assign_task)
# class Assign_taskAdmin(admin.ModelAdmin):
#     list_display = [ 'id','project_name','discription','assign_by','assign_to','department','task_priority','task_assign_date','task_finish_date','task_status' ]
    
