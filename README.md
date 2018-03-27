# SnoutPage

<H3> Django allauth/ facebook login setup </h3>
<ol>
	<li> Install django allauth by using: pip install django-allauth</li>
	<li> Create a superuser account for the django admin site by using 'python manage.py createsuperuser' and log in</li>
	<li> Click on the sites tab and click on the first site</li>
	<li> Change domain name to 'localhost:8000' and save</li>
	<li> Click on social applications and select facebook as the provider from the drop down menu</li>
	<li> Enter details for the client id and secret key - both of these are stored as variables in settings.py</li>
	<li> Select localhost:8000 in the available sits tab and choose it so that it appears in the chosen sites tab, and save</li>
	<li> Django allauth should now be set up</li>
</ol>
