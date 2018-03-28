import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SnoutPage_project.settings')
import django
django.setup()
from SnoutPage.models import Category, Post, Pet

def populate():



    ## testing: marley and max would be two pets, and would have these posts assigned to them
    Marley_post =[
    {"title":"dog",
     "description":"it's a dog",
     "picture":"post_images/Dog_CTA_Desktop_HeroImage.jpg",
     "Category":"dog",},

    {"title":"do2",
     "description":"it's the same dog",
     "picture":"post_images/download.jpg",
     "Category":"dog",}
    ]

    max_post = [
    {"title":"cat",
     "description":"i'ts a cat",
     "picture":"post_images/ca1.jpg.jpg",
     "Category":"dog",
     },
    ]


    pets = {"dog":{"posts":Marley_post},
        "cat": {"posts":max_post}}

    for cat, cat_data in pets.items():

        c = add_pet(cat)
        for p in cat_data["posts"]:
            add_post(c, p["title"],p["description"], p["picture"], p["Category"])


def add_post(pets, title, description, picture, Category):

    p = Post.objects.get_or_create( title=title, pet=pets)[0]

    p.tile =title
    p.description =description
    p.picture = picture


    p.Category= Category


    p.save()
    return p


def add_pet(name):
    a = Pet.objects.get_or_create(name=name)[0]
    a.save()
    return a


if __name__ == '__main__':
    print("Starting SnoutPage population script...")
    populate()
