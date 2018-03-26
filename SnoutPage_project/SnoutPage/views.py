from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from SnoutPage.models import UserProfile, Pet, Post, PostLike, Comment, AdditonalUserData,ImageTest
from SnoutPage.forms import UserForm, UserProfileForm, PostForm, PetForm, CommentForm, EditUserForm, PostLikeForm,EditOtherDetails, AdditonalUserData,ImageForm, FollowForm
from django.template.defaultfilters import slugify
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#from SnoutPage import Friend

def index(request):
    context_dict = {}
    posts = Post.objects.all()
    context_dict['posts'] = posts
    return render(request, 'SnoutPage/index.html', context_dict)

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
        post_number=posts.count()
        comment_number=0
        like_number=0
        owner = pet.owner
        user = request.user
        if user.username==owner.username:
            context_dict['authenticated'] = True
        else:
            context_dict['authenticated'] = False
        for post in posts:
            comSum = Comment.objects.filter(post=post).count()
            likeSum = PostLike.objects.filter(post=post, liked=True).count()
            comment_number += comSum
            like_number += likeSum
        context_dict['post_number'] = post_number
        context_dict['comment_number'] = comment_number
        context_dict['like_number'] = like_number
        context_dict['slug'] = pet_name_slug
        context_dict['posts'] = posts
        context_dict['owner'] = owner
        context_dict['name'] = pet.name
        context_dict['category'] = pet.category
        context_dict['picture'] = pet.picture
        context_dict['description'] = pet.description
    except Pet.DoesNotExist:
        context_dict['post_number'] = None
        context_dict['comment_number'] = None
        context_dict['like_number'] = None
        context_dict['slug'] = None
        context_dict['posts'] = None
        context_dict['owner'] = None
        context_dict['name'] = None
        context_dict['category'] = None
        context_dict['picture'] = None
        context_dict['description'] = None

    return render(request, 'SnoutPage/pet.html', context_dict)

def post_category (request, category):
    context_dict = {}
    posts = Post.objects.filter(category=category)
    context_dict ['posts'] = posts
    return render(request, 'SnoutPage/post_category.html', context_dict)


def post(request, post_title_slug):
    context_dict = {}
    form = PostLikeForm()
    context_dict['form'] = form
    try:
        post = Post.objects.get(slug=post_title_slug)
        user = request.user
        if user.id != None:
            context_dict['user'] = user
            liked_by_user = PostLike.objects.filter(post=post, liked = True, user = user)
            if liked_by_user:
                context_dict['not_liked_by_user'] = False
            else:
                context_dict['not_liked_by_user'] = True

            if request.method=='POST' and 'like' in request.POST:
                postlike = form.save(commit=False)
                postlike.user = user
                postlike.post = post
                postlike.liked = True
                postlike.save()
            else:
                print(form.errors)
        else:
            context_dict['user'] = None


        comments = Comment.objects.filter(post=post)
        likes = PostLike.objects.filter(post=post, liked = True).count()
        context_dict['likes'] = likes
        context_dict['slug'] = post.slug
        context_dict['pet'] = post.pet
        context_dict['comments'] = comments
        context_dict['category'] = post.category
        context_dict['title'] = post.title
        context_dict['description'] = post.description
        context_dict['tag'] = post.tag
        context_dict['author'] = post.author
        context_dict['created_date'] = post.created_date
        context_dict['image']=post.image
    except Post.DoesNotExist:
        context_dict['pet'] = None
        context_dict['slug'] = None
        context_dict['likes'] = None
        context_dict['comments'] = None
        context_dict['category'] = None
        context_dict['title'] = None
        context_dict['description'] = None
        context_dict['tag'] = None
        context_dict['author'] = None
        context_dict['created_date'] = None
        context_dict['image']=None


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
        form = PetForm(request.POST,request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
        else:
            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'SnoutPage/add_pet.html', context_dict)

def add_comment(request, post_title_slug):
    context_dict={}
    try:
        post = Post.objects.get(slug=post_title_slug)
    except Post.DoesNotExist:
        post = None
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if post:
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
            return render(request, 'SnoutPage/post.html', context_dict)
        else:
            print(form.errors)
    context_dict = {'form':form, 'post': post}
    return render(request, 'SnoutPage/add_comment.html', context_dict)


def add_post(request, pet_name_slug):
    context_dict={}
    try:
        pet = Pet.objects.get(slug=pet_name_slug)
    except Pet.DoesNotExist:
        pet = None
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            if pet:
                post = form.save(commit=False)
                post.pet = pet
                post.author = request.user
                post.category = pet.category
                post.save()
                context_dict['slug']=pet_name_slug
            return render(request, 'SnoutPage/pet.html', context_dict)
        else:
            print(form.errors)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
    context_dict = {'form':form, 'pet': pet}

    return render(request, 'SnoutPage/add_post.html', context_dict)


def search(request):

    result_list = []

    return render(request, 'SnoutPage/base.html', {'result_list': result_list})

#@login_required
def user_page(request, username):
    context_dict = {}
    userdata = AdditonalUserData.objects.all
    owner = User.objects.get(username = username)
    context_dict['owner']=owner
    try:
        user = request.user

        if owner.username == user.username:
            context_dict['authenticated'] = True
        else:
            context_dict['authenticated'] = False

        pets = Pet.objects.filter(owner=owner)
        pet_number = pets.count()
        context_dict['pet_number'] = pet_number
        context_dict['pets'] = pets
        context_dict['userdata'] = userdata
        context_dict['user']=user
        form= FollowForm()
        context_dict['form'] = form
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user = owner
            follow.follower = user
            follow.save
            #return render(request, 'SnoutPage/user_page.html',context_dict)
        else:
            print(form.errors)

    except:
        print ('didnt work')


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

def add_image(request): ## view saves image to database (see in admin panel)
    form = ImageForm(request.POST or None, request.FILES or None)
    # imagedata = ImageTest.objects.all
    if form.is_valid():
        instance = form.save(commit =False)
        instance.save()
    else:
        print ('not valid form')

    # imagedata = ImageTest.objects.all
    imagedata = ImageTest.objects.filter(description ='this is a description5')
    user = request.user

    c ={}
    c['imagedata'] =imagedata
    print ("image data ")
    print (imagedata)
    c["form"]=form
    c['user']=user



    return render(request, "SnoutPage/add_image.html",c)
