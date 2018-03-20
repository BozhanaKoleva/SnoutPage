from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from SnoutPage.forms import UserForm, UserProfileForm, PostForm, PetForm, CommentForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
#from SnoutPage import Friend

def index(request):
    context_dict = {}
    return render(request, 'SnoutPage/index.html', context = context_dict)

def userPage(request):
    context_dict = {}
    return render(request, 'SnoutPage/user.html', context=context_dict)



def register(request):
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            
            profile = profile_form.save(commit=False)
            #profile.user = user # removed as it was causing max recursion error- trying to figure out how to fix

            new_user = authenticate(username = user_form.cleaned_data['username'],password=user_form.cleaned_data['password'],)
            login(request, new_user)
            # If the user provided a profile picture, we need to get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # Now we save the UserProfile model instance.
            profile.save()
            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
            return HttpResponseRedirect('/index/')# change to userPage when userPage completed
        else:
            # Invalid form or forms 
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
    # Render the template depending on the context.
    return render(request,
        'SnoutPage/register.html',
        {'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered})

def user_login(request):
    print ('auda')
    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        print ('username, password' + username + password)
        #email = request.POST.get('email')
##        username = request.POST.get('username')
##        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                print( 'user logged in')
                return HttpResponseRedirect('/index/')

            else:
                return HttpResponse("Your account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    return render(request, {})
        
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/index/')

def show_category(request, category_name_slug):
    # Create a context dictionary that we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
       
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

        context_dict['query'] = category.name
        result_list = []
        if request.method == 'POST':
            query = request.POST['query'].strip()
            if query:
                result_list = run_query(query)
                context_dict['query'] = query
                context_dict['result_list'] = result_list
          
    return render(request, 'SnoutPage/category.html', context_dict)


def add_page(request):
##    try:
##        category = Category.objects.get(slug=category_name_slug)
##    except Category.DoesNotExist:
##        category = None
##
    form = PetForm()
##    if request.method == 'POST':
##        form = PageForm(request.POST)
##        if form.is_valid():
##            if category:
##                page = form.save(commit=False)
##                page.category = category
##                page.views = 0
##                page.save()
##                # probably better to use a redirect here.
##            return show_category(request, category_name_slug)
##        else:
##            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'SnoutPage/add_pet.html', context_dict)

def add_pet(request):
    form = PetForm()
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = self.request.user
            pet.save()
        else:
            print(form.errors)
            
    context_dict = {'form':form}

    return render(request, 'SnoutPage/add_pet.html', context_dict)


def add_post(request, pet_name_slug):
    try:
        pet = Pet.objects.get(slug=pet_name_slug)
    except Pet.DoesNotExist:
        pet = None
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if pet:
                post = form.save(commit=False)
                post.author = self.request.user
                post.likes = 0
                post.category = pet.category
                post.save()
            return show_pet(request, pet_name_slug)    
        else:
            print(form.errors)
            
    context_dict = {'form':form, 'pet': pet}

    return render(request, 'SnoutPage/add_post.html', context_dict)
    

def search(request):

    result_list = []

    return render(request, 'SnoutPage/base.html', {'result_list': result_list})

def user_page(request):

    description =""
    friend_list=[]
    pet_list=[]

    return render(request, 'SnoutPage/user_page.html',{})
def pet(request):
    return render(request, 'SnoutPage/pet.html',{})

def edit_pet(request):
    return render(request,'SnoutPage/edit_pet.html',{})

def category_list(request):
    return render(request, 'SnoutPage/category_list.html',{})

##def add_pet(request):
##    return render(request, 'SnoutPage/add_pet.html',{})

def edit_user(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.POST,instance =request.user)
        if form.is_valid():
            form.save()
            return redirect('user_page')
    else:
        form = EditUserForm(instance = request.user)
        context_dict ={'form':form}
        return render(request, 'SnoutPage/edit_user.html',context_dict)

def change_password(request):
    if request.method=='POST':
        form = PasswordChangeForm(data=request.POST,user =request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('user_page')
        else:
            return redirect('/change-password/')
    else:
        form = PasswordChangeForm(user=request.user)
        context_dict = {'form':form}
    
        return render(request,'SnoutPage/change-password.html',context_dict)
