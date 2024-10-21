from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Book, items, review, user_details, BookRating, Product,FavoriteBook,UserProfile
from .forms import BookAddForm,BookRatingForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render





@login_required
def home(request):
    # Annotate each book with its average rating
        # Check if the user has uploaded a book
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    has_uploaded_book = user_profile.has_uploaded_book

    # Annotate each book with its average rating
    books = Book.objects.annotate(average_rating=Avg('bookrating__rating')).order_by('id')

    # Paginate the annotated queryset
    paginator = Paginator(books, 5)  # Show 5 books per page

    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'uphome.html', {'books': books, 'has_uploaded_book': has_uploaded_book})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookAddForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)  # Do not save to the database yet
            book.uploaded_by = request.user  # Assign the currently logged-in user
            book.save()  # Now save the instance to the database
            # Update user profile to indicate book upload
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.has_uploaded_book = True
            user_profile.save()
            messages.success(request, "Book added successfully")
            return redirect('upload')
    else:
        form = BookAddForm()
    return render(request, 'add_book.html', {'form': form})
@login_required
def delete_book(request, pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        messages.success(request, "Book deleted successfully")
        return redirect('home')
    else:
        return redirect('home')

@login_required
def review_page(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        rating = request.POST.get('rating')
        
        # Handle saving the rating to the database here
        # BookRating.objects.create(book_id=book_id, rating=rating)
        
        return redirect('upload')  # Redirect to a success URL

    return render(request, 'review_page.html')

def projectview(request):
    return render(request, 'home.html')
   

@login_required
def book_list(request):
    category = request.GET.get('category')  # Get the selected category from query parameters
    books = Book.objects.all()

    if category:
        books = books.filter(category=category)

    for book in books:
        average_rating = BookRating.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
        book.average_rating = average_rating if average_rating else 0  # Default to 0 if no ratings

    context = {
        'books': books,
        'selected_category': category,  # Pass selected category to template for highlighting
    }
    return render(request, 'uphome.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    ratings = BookRating.objects.filter(book=book)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        form = BookRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.book = book
            rating.save()
            messages.success(request, "Your rating has been submitted!")
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookRatingForm()

    context = {
        'book': book,
        'ratings': ratings,
        'average_rating': round(average_rating,2) if average_rating else 0,  # Default to 0 if no ratings
        'form': form,
    }
    return render(request, 'book_detail.html', context)


@login_required
def search(request):
    query = request.GET.get('q')
    if query:
        results = Book.objects.filter(title__icontains=query)
    else:
        results = Book.objects.all()
    
    paginator = Paginator(results, 5)  # Paginate the results if needed
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    
    return render(request, 'uphome.html', {'books': results, 'query': query})



@login_required
def add_favorite(request, book_id):
    if not request.user.userprofile.has_uploaded_book:
        messages.error(request, "You must upload at least one book to save favorites.")
        return redirect('home')
    
    book = get_object_or_404(Book, pk=book_id)
    FavoriteBook.objects.get_or_create(user=request.user, book=book)
    return redirect('favorite_books')

@login_required
def download_book(request, book_id):
    if not request.user.userprofile.has_uploaded_book:
        messages.error(request, "You must upload at least one book to download.")
        return redirect('home')

    book = get_object_or_404(Book, pk=book_id)
    # Add your logic to handle book download
    return redirect(book.pdf.url)

@login_required
def remove_favorite(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    favorite = FavoriteBook.objects.filter(user=request.user, book=book)
    if favorite.exists():
        favorite.delete()
    return redirect('favorite_books')

@login_required
def favorite_books(request):
    favorite_books = FavoriteBook.objects.filter(user=request.user)
    return render(request, 'favorite_books.html', {'favorite_books': favorite_books})

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request, 'about.html')

@login_required
def my_books(request):
    books = Book.objects.filter(uploaded_by=request.user)
    return render(request, 'my_books.html', {'books': books})

@login_required
def delete_my_book(request, pk):
    book = get_object_or_404(Book, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully")
        return redirect('my_books')
    return render(request, 'delete_my_book.html', {'book': book})