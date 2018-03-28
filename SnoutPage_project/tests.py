from django.contrib.auth.models import User
from django.test import TestCase

from SnoutPage.models import UserProfile, Pet
from SnoutPage.forms import PetForm
import SnoutPage.views
class ModelTests(TestCase):

    def setUp(self):
        try:
            from population_script import populate
            populate()
        except ImportError:
            print('The module does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function')


    def test_create_profile(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        self.user.save()
        self.assertEqual(self.user.username == 'testuser', True)

    def test_add_pet(self):

        self.Pet = Pet.objects.create(name='Testanimal', description='Testdescription', category='DOG', picture=None)
        self.Pet.save()
        self.assertEqual(self.Pet.name=='Testanimal', self.Pet.description=='Testdescription',self.Pet.category=='DOG', True)
