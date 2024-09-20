from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import Registeruser,EditForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache


# Create your views here.
#@user_passes_test(lambda u:u.is_superuser)


def admin_view(request):
    qs =request.GET.get('qs')
    if qs:
        users=User.objects.filter(username__icontains=qs)
    else:
        users=User.objects.all()
        
    
    return render(request,'admin.html',{'users':users})

@user_passes_test(lambda u: u.is_superuser,login_url="error")
@never_cache
def user_detail_page(request,id):
    user=User.objects.get(id=id)
    return render(request,'detail.html',{'user':user})

@user_passes_test(lambda u:u.is_superuser,login_url="error")
@never_cache   
def delete_user(request,id):
    user=User.objects.get(id=id)
    user.delete()
    
    return redirect('adminview')
@user_passes_test(lambda u:u.is_superuser,login_url="error")
def edit_user(request,id):
    user=User.objects.get(id=id)
    form=EditForm(instance=user)
    if request.method=='POST':
        form=EditForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'user edited succesfully')
            return redirect('adminview')
        else:
            messages.error(request,form.errors) 
            form=EditForm(instance=user)
            return render(request,'edit.html',{'form':form})
  
    return render(request,'edit.html',{'form':form})

def user_creation(request):
    form=Registeruser()
    
    if request.method=='POST':
        form=Registeruser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'user create sucsessfuly')
            return redirect('login')
        else:
            messages.error(request,form.errors)
            return redirect('register')
    return render(request,'register.html',{'form':form})

def login_view(request):
    if request.user.is_authenticated:
        
        return redirect('adminview')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f'hello {username}')
            return redirect('adminview')
        else:
            messages.error(request,'invalied credential')
            return redirect('login')
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


def error_view(request):
    messages.error(request,'only superuser are autherised this fungtion')
    return redirect('adminview')