from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from SnoutPage.models import UserProfile, Pet, Post, PostLike, Comment, AdditonalUserData
from SnoutPage.forms import UserForm, UserProfileForm, PostForm, PetForm, CommentForm, EditUserForm, PostLikeForm,EditOtherDetails, AdditonalUserData
from django.template.defaultfilters import slugify
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        #if user_form.is_valid() and profile_form.is_valid
        if profile_form.is_valid() and user_form.is_valid():

            # Save the user's form data to the database.
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            #profile_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user # removed as it was causing max recursion error- trying to figure out how to fix


            # If the user provided a profile picture, we need to get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # Now we save the UserProfile model instance
            username =user_form.cleaned_data['username']
            print ('username' + username)
            #profile.save() #fix!!!
            new_user = authenticate(username =user_form.cleaned_data['username'],password=user_form.cleaned_data['password'],)
            login(request, new_user,backend='django.contrib.auth.backends.ModelBackend')
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

   # print 'soem'


    if request.method == 'POST':

       # print 'soem'

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

def pet(request, pet_name_slug):
    context_dict = {}
    try:
        pet = Pet.objects.get(slug=pet_name_slug)
        posts = Post.objects.filter(pet=pet)
        context_dict['slug'] = pet_name_slug
        context_dict['posts'] = posts
        context_dict['owner'] = pet.owner
        context_dict['name'] = pet.name
        context_dict['category'] = pet.category
        context_dict['picture'] = pet.picture
        context_dict['description'] = pet.description
    except Pet.DoesNotExist:
        context_dict['slug'] = None
        context_dict['posts'] = None
        context_dict['owner'] = None
        context_dict['name'] = None
        context_dict['category'] = None
        context_dict['picture'] = None
        context_dict['description'] = None

    return render(request, 'SnoutPage/pet.html', context_dict)

def post(request, post_name_slug):
    context_dict = {}
    try:
        post = Post.objects.get(slug=post_name_slug)
        liked_by_user = PostLike.objects.filter(post=post, liked = True, user = self.request.user)
        if liked_by_user:
            #context_dict['message'] = "you have liked this post!"
            context_dict['form'] = None
        else:
            form = PostLikeForm(request.POST or None)
            #context_dict['message'] = "like this post if you like it!"
            context_dict['form'] = form
            if form.is_valid():
                postlike = form.save(commit=False)
                postlike.user = request.user
                postLike.post = post
                postLike.save()
            else:
                print(form.errors)

        comments = Comment.objects.filter(post=post)
        likes = PostLike.objects.filter(post=post, liked = True).count()
        context_dict['likes'] = likes
        context_dict['comments'] = comments
        context_dict['category'] = category
        context_dict['title'] = title
        context_dict['description'] = description
        context_dict['tag'] = tag
        context_dict['author'] = author
        context_dict['created_date'] = created_date
    except Post.DoesNotExist:
        context_dict['likes'] = None
        context_dict['comments'] = None
        context_dict['category'] = None
        context_dict['title'] = None
        context_dict['description'] = None
        context_dict['tag'] = None
        context_dict['author'] = None
        context_dict['created_date'] = None


    return render(request, 'SnoutPage/post.html', context_dict)


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
            pet.owner = request.user
            pet.save()
        else:
            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'SnoutPage/add_pet.html', context_dict)


def add_post(request, pet_name_slug=None):
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
                post.category = pet.category
                post.save()
            return pet(request, pet_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'pet': pet}

    return render(request, 'SnoutPage/add_post.html', context_dict)


def search(request):

    result_list = []

    return render(request, 'SnoutPage/base.html', {'result_list': result_list})

#@login_required
def show_user_page(request):
    #picture = user.userprofile.picture
    # userdata = AdditonalUserData.objects.all
    # # descriptions.description.all
    # print (userdata)
    # description =""
    # friend_list=[]
    # user = request.user
    # pets = Pet.objects.filter(owner=user)
    # pet_number = pets.count()
    # context_dict = {}
    # context_dict['pet_number'] = pet_number
    # context_dict['pets'] = pets
    # context_dict['userdata'] = userdata
    # if pk:
    #     users = User.objects.get(pk=pk)
    # else:
    userdata = AdditonalUserData.objects.all
    user = request.user
    try:
        user = User.objects.get(username =user.username)
    except:
        raise Http404
    # users = request.user
    # allusers = User.objects.all()
    # context_dict  ={'user':users, 'allusers':allusers}
    context_dict = {'user':user,'userdata':userdata}
    return render(request, 'SnoutPage/user_page.html',context_dict)

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

def add_info(request):
#def description(self, request):
    context_dict={}
    #if request.method =='POST':
    form= EditOtherDetails(request.POST)
    context_dict ={'form':form}
    if form.is_valid():
        newfile =AdditonalUserData(picture = request.FILES['picture'])
        #newfile.save()

        file = request.FILES['picture']

        info = form.save(commit=False)
        info.user = request.user
        info.save()
        text = form.cleaned_data['description']
        # something similar for picture too
        form = EditOtherDetails()
        context_dict['text'] = text
        context_dict['form']=form

        user = AdditonalUserData.objects.filter(user=request.user)
        user.picture =request.POST.get('picture')
        context_dict['picture']= user.picture

    return render(request,'SnoutPage/add_info.html' ,context_dict)

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
