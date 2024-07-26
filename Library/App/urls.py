from django.urls import path
from .views import *
from App import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('',views.Register,name = 'register'),
    path('login/',views.login, name = 'login'),
    path('logout/',views.logout, name = 'logout'),
    path('add-book/',views.add_book,name = 'add-book'),
    path('update/<int:pk>/',views.book_update,name = 'book_update'),
    path('show_book/',views.show_book,name = 'show_book'),
    path('issue_books/<int:pk>/',views.issue_books,name = 'issue_books'),
    path('filter_book/',views.filter_book,name = 'filter_book'),
    path('delete_book/<int:pk>/',views.delete_book,name = 'delete_book'),
    path('issue_bk/',views.issue_bk,name = 'issue_bk'),
    path('issues_book_histry/',views.issues_book_histry,name = 'issues_book_histry'),
    path('return_book/',views.return_book,name = 'return_book'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

