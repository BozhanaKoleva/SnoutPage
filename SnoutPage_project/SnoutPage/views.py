from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

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
            profile.user = user
            
            # If the user provided a profile picture, we need to get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # Now we save the UserProfile model instance.
            profile.save()
            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
            return HttpResponseRedirect(reverse('userPage'))
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
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            
        else:
            # Bad login details were provided
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'SnoutPage/login.html', {})


