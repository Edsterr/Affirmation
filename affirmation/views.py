from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from affirmation.models import Category, Page, UserProfile, Data
from affirmation.forms import CategoryForm, UserForm, UserProfileForm, dataForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from chartit import DataPool, Chart

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

@login_required
def data(request):

     user_id = UserProfile.objects.get(user=request.user)

     form = dataForm()
     
     if request.method == 'POST':
          form = dataForm(request.POST)

          if form.is_valid():
               data = form.save(commit=False)
               data.user=user_id
               data.save()
               return HttpResponseRedirect("")
          else:
               print(data_form.errors)
     else:
          data_form = dataForm()
     return render(request,
                   'affirmation/data.html',
                   {'data_form': data_form})

@login_required
def pastData(request):
    print(request.user.is_authenticated())
    s=Data.objects.filter(user=UserProfile.objects.get(user=request.user))
     #Step 1: Create a DataPool with the data we want to retrieve.
    treatmentdata = \
        DataPool(
           series=
            [{'options': {
               'source': s},
              'terms': [
                'date',
                'satisfaction']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = treatmentdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'date': [
                    'satisfaction']
                  }}],
            chart_options =
              {'title': {
                   'text': s[0].treatment},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})

    #Step 3: Send the chart object to the template.
    return render(request, 'affirmation/pastData.html', {'weatherchart': cht})

    #return render(request, 'affirmation/pastData.html', {})

def treatment(request):
     return render(request, 'affirmation/treatment.html', {})

def resources(request):
     return render(request, 'affirmation/resources.html', {})
