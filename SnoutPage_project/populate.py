import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SnoutPage_project.settings')

from SnoutPage.models import Category, Page

def populate():
    cats = {"Dogs" : {"pages": dogs}}
    for cat, cat_data in cats.items():
        # c = add_cat(cat)
        # Updated the population script to pass through the specific values for views and likes
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["views"])


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c


if __name__ == '__main__':
    print("Starting SnoutPage population script...")
    populate()
