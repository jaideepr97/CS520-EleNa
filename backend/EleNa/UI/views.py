# Create your views here.
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
import requests
# from .forms import InputForm
# from flask import render_tempate

def get_input_form(request):
	# if this is a POST request we need to process the form data
	# if request.method == 'POST':
	# 	# create a form instance and populate it with data from the request:
	# 	form = InputForm(request.POST)

	# 	# check whether it's valid:
	# 	if form.is_valid():
	# 		post_data = {'lat': form.cleaned_data['latitude']}
	# 		response = requests.post('http://localhost:8000/find_route/', data=post_data)
	# 		# content = response.content
	# 		# process the data in form.cleaned_data as required
	# 		# ...
	# 		# redirect to a new URL:
	# 		# return HttpResponseRedirect('/thanks/')

	# if a GET (or any other method) we'll create a blank form
	# else:
	# 	form = InputForm()

	if request.method == 'GET':
		# data = dict()
		context = {
			'MAP_API_KEY': settings.MAP_API_KEY
		}
		# data['MAP_API_KEY'] = settings.MAP_API_KEY
		return render(request, "UI/index.mako", context)
	# return render(request, 'UI/inputForm.html', {'form': form})