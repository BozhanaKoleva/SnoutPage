from django.test import TestCase

class ModelTests(TestCase):

    def setUp(self):
        try:
            from populate import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')
			
def get_category(self, name):
        
        from SnoutPage.models import Category
        try:                  
            cat = Category.objects.get(name=name)
        except Category.DoesNotExist:    
            cat = None
        return cat
        