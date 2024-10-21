from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render,HttpResponseRedirect
from .forms import signform
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash

from .models import Book, items, review, user_details
from .forms import BookAddForm

# # Create your views here.
# # @login_required(login_url='login')
# def projectview(request):
#     return render(request,'project/home.html')


# # login__page

# def signview(request):
#     if request.method =="POST":
#         fm=signform(request.POST)
#         if fm.is_valid():
#             messages.success(request,'Account Successfully Created !!')
#             fm.save()
#     else:
#         fm=signform()
#     return render(request,'./project/signup.html',{'form':fm})


# def user_login(request):
#     if not request.user.is_authenticated:
#         if request.method=="POST":
#             fm=AuthenticationForm(request=request,data=request.POST)
#             if fm.is_valid():
#                 uname=fm.cleaned_data['username']
#                 upaas=fm.cleaned_data['password']
#                 user=authenticate(username=uname,password=upaas)
#                 if user is not None:
#                     login(request,user)
#                     return HttpResponseRedirect('/profile/')
#         else:
#             fm=AuthenticationForm()
#         return render(request,'./project/userlogin.html',{'form':fm})
#     else:
#         return HttpResponseRedirect('/profile/')

# def user_profile(request):
#     if request.user.is_authenticated:
#         return render(request,'project/home.html',{'name':request.user})
#     else:
#         return HttpResponseRedirect('/login/')

# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect('/login/')

# def user_changepass(request):
#     if request.user.is_authenticated:
#         if request.method=="POST":
#             fm=PasswordChangeForm(user=request.user,data=request.POST)
#             if fm.is_valid():
#                 fm.save()
#                 update_session_auth_hash(request, fm.user)
#                 messages.success(request,'Password change Successfully')
#                 return HttpResponseRedirect('/profile/')
#         else:     
#             fm = PasswordChangeForm(user=request.user)
#         return render(request,'project/changepass.html',{'form':fm})
#     else:
#         return HttpResponseRedirect('/login/')


# def home(request):
#     books = Book.objects.all()
#     return render(request, 'project/uphome.html', {'books': books})


# def add_book(request):
#     if request.method == 'POST':
#         form = BookAddForm(request.POST, request.FILES)
#         if form.is_valid:
#             form.save()
#             messages.success(request, "Book added successfully")
#             return redirect('home')
#     else:
#         form = BookAddForm()
#     return render(request, 'project/add_book.html', {'form': form})


# def delete_book(request, pk):
#     if request.method == 'POST':
#         book = get_object_or_404(Book, pk=pk)
#         book.delete()
#         messages.success(request, "Book deleted successfully")
#         return redirect('home')
#     else:
#         return redirect('home')



# def review_page(request):

#     id = request.GET.get('id')
#     item_details = items.objects.get(id=int(id))
#     user = request.session['email']
#     user_detail = user_details.objects.get(email=user)
#     if request.method == 'POST':
#         star_rating = request.POST.get('rating')
#         item_review = request.POST.get('item_review')

#         item_reviews = review(user=user_detail, item=item_details, rating=star_rating, review_desp = item_review)
#         item_reviews.save()

#         rating_details = review.objects.filter(item=item_details)
#         context = {'reviews': rating_details}
#         return render(request, 'review_page.html', context)

#     rating_details = review.objects.filter(item=item_details)
#     context = {'reviews': rating_details}
#     return render(request, 'review_page.html', context)


#contact_page
def contactpage(request):
    return render(request,'project/contact.html')
#about_us_page
def aboutus(request):
    return render(request,'project/about.html')

def dashboard_view(request):
    return render(request,'project/dashboard.html')

def uploadpage(request):
    return render(request,'project/upload_base.html')

def adminpage(request):
    return render(request,'project/admin.html')