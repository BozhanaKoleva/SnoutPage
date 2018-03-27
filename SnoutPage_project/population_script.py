import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SnoutPage_project.settings')
import django
django.setup()
from SnoutPage.models import Category, Post, Pet

def populate():



    ## testing: marley and max would be two pets, and would have these posts assigned to them
    Marley_post =[
    {"title":"dog","description":"it's a dog","views":5,"category":"dog"},
    {"title":"dog2","description":"it's the same dog","views":10,"category":"dog"}
    ]

    max_post = [
    {"title":"cat", "description":"i'ts a cat","views":10, "category" :"cat"},
    ]
    pets = {"dog":{"posts":Marley_post},
        "cat": {"posts":max_post}}

    for cat, cat_data in pets.items():
        # c = add_cat(cat)
        # Updated the population script to pass through the specific values for views and likes
        print "cat:"+  cat
        c = add_pet(cat)
        for p in cat_data["posts"]:
            add_post(c, p["title"], p["views"],p["description"],p["category"])


def add_post(cat, title, views,description,category):
    print "category:" + category
    p = Post.objects.get_or_create( title=title)[0]
    p.views=views
    p.tile =title
    p.description =description


    #p.category= Category.objects.get_or_create(name = category)


    p.save()
    return p


def add_pet(name):
    c = Pet.objects.get_or_create(name=name)[0]
    c.save()
    return c


if __name__ == '__main__':
    print("Starting SnoutPage population script...")
    populate()
