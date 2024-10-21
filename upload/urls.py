from django.urls import path
from .import views 
from signapp import views as pk



urlpatterns = [
    path('', pk.user_login, name='user_login'),
    path('home/', pk.home_page, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    
    path('add/', views.add_book, name='add_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
    # path('review_page/', views.review_page, name='review_page'),
    path('upload/review_page', views.review_page, name='review_page'),
    path('upload/',views.home,name='upload'),
    path('profile/',pk.user_profile,name='user_profile'),
    path('search/', views.search, name='search'),
    path('add_favorite/<int:book_id>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<int:book_id>/', views.remove_favorite, name='remove_favorite'),
    path('favorite_books/', views.favorite_books, name='favorite_books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('my_books/', views.my_books, name='my_books'),
    path('delete_my_book/<int:pk>/', views.delete_my_book, name='delete_my_book'),
    path('book_list/', views.book_list, name='book_list'),
    
] 
