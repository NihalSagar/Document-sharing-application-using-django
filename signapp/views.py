from django.shortcuts import render,HttpResponseRedirect
from .forms import signform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from upload.models import UserProfile
# Create your views here.

def signview(request):
    if request.method =="POST":
        fm=signform(request.POST)
        if fm.is_valid():
            messages.success(request,'Account Successfully Created !!')
            fm.save()
    else:
        fm=signform()
    return render(request,'signup.html',{'form':fm})


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
#                     return HttpResponseRedirect('/home/')
#         else:
#             fm=AuthenticationForm()
#         return render(request,'userlogin.html',{'form':fm})
#     else:
#         return HttpResponseRedirect('/home/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upaas = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upaas)
                if user is not None:
                    login(request, user)
                    # Reset the has_uploaded_book flag to False
                    user_profile, created = UserProfile.objects.get_or_create(user=user)
                    user_profile.has_uploaded_book = False
                    user_profile.save()
                    return HttpResponseRedirect('/home/')
        else:
            fm = AuthenticationForm()
        return render(request, 'userlogin.html', {'form': fm})
    else:
        return HttpResponseRedirect('/home/')
    
def home_page(request):
    return render(request, 'home.html')

def user_profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html',{'name':request.user})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def user_changepass(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request,'Password change Successfully')
                return HttpResponseRedirect('/profile/')
        else:     
            fm = PasswordChangeForm(user=request.user)
        return render(request,'changepass.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')