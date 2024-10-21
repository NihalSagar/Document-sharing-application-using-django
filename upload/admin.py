from django.contrib import admin
from .models import Book
from .models import Product,UserProfile

class ModelBook(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'cover', 'pdf')
    search_fields = ('author', 'title')
    list_filter = ('category', 'author')


admin.site.register(Book, ModelBook)


admin.site.register(Product)

admin.site.register(UserProfile)