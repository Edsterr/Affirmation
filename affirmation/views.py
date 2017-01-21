from django.shortcuts import render
from django.http import HttpResponse
from affirmation.models import Category, Page, UserProfile
from affirmation.forms import CategoryForm, UserForm, UserProfileForm, dataForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def register(request):
     registered = False
     if request.method == 'POST':
          user_form = UserForm(data=request.POST)
          profile_form = UserProfileForm(data=request.POST)

          if user_form.is_valid() and profile_form.is_valid():
               user = user_form.save()
               user.set_password(user.password)
               user.save()

               profile = profile_form.save(commit=False)
               profile.user = user

               if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']

               profile.save()

               registered = True
          else:
               print(user_form.errors, profile_form.errors)
     else:
          user_form = UserForm()
          profile_form = UserProfileForm()

     return render(request,
                   'affirmation/register.html',
                   {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered})

def user_login(request):
     if request.method == 'POST':
          username = request.POST.get('username')
          password = request.POST.get('password')
          user = authenticate(username=username, password=password)
          if user:
               if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('index'))
               else:
                    return HttpResponse("Your account is disabled")
          else:
               print("Invalid login details: {0}, {1}".format(username, password))
               return HttpResponse("Invalid login details supplied")
     else:
          return render(request, 'affirmation/login.html', {})

@login_required
def user_logout(request):
     logout(request)
     return HttpResponseRedirect(reverse('index'))

@login_required
def account(request):
     user_data = UserProfile.objects.get(user=request.user)
     context = {'user_data':user_data}
     return render(request, 'affirmation/account.html',context)

def index(request):
     context_dict = {'boldmessage': "I'm really bad at design. Please someone help"}
     return render(request, 'affirmation/index.html', context_dict)

def data(request):
     if request.method == 'POST':
          data_form = dataForm(request.POST)

          if data_form.is_valid():
               data_form.save()
               return HttpResponseRedirect("")
          else:
               print(data_form.errors)
     else:
          data_form = dataForm()
     return render(request,
                   'affirmation/data.html',
                   {'data_form': data_form})

def pastData(request):
     return render(request, 'affirmation/pastData.html', {})

def treatment(request):
     return render(request, 'affirmation/treatment.html', {})

def resources(request):
     return render(request, 'affirmation/resources.html', {})
