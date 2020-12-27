import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import models as django_models
from django.contrib.auth.models import User
from django.views import generic, View
from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from events.models import Event
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from events.forms import EventListForm,LoginForm,SignUpForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def home(request):
    return render(request, 'home.html',{'home':home})
def contactus(request):
    return render(request, 'contactus.html',{'home':home})

class ManagerRequiredMixin(AccessMixin):
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated or not hasattr(self.request.user, 'userprofile') or not self.request.user.userprofile.is_manager:
			return self.handle_no_permission()
		return super().dispatch(request, *args, **kwargs)

class Login(View):
	def get(self, request):
		form = LoginForm()
		return render(request, 'login.html', {'form': form})
	
	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = django_models.User.objects.filter(username=username).first()
			if user:
				if user.check_password(password):
					login(request, user)
					return redirect('/Eventlist')
				else:
					return render(request, 'login.html', {'form': form, 'error': 'Invalid Credentials'})
			else:
				return render(request, 'login.html', {'form': form, 'error': 'User not found'})
		else:
			return render(request, 'login.html', {'form': form})


class EventListView(generic.ListView):
	template_name = 'Eventlist.html'
	context_object_name = 'events'
	queryset = Event.objects.filter()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['now'] = datetime.datetime.now()
		return context
def event_detail(request,event_id):
	event = Event.objects.filter(id=event_id).first()
	return render(request, 'event_detail.html', {'event': event})

class AddEventCreateView(LoginRequiredMixin, generic.CreateView):
	login_url = '/login'
	success_url = '/Eventlist'
	template_name = 'add_event.html'
	form_class = EventListForm
	
	def get_success_url(self):
		if self.request.user.is_authenticated:
			self.object.created_by = self.request.user
			self.object.save()
		return super().get_success_url()
	
class UpdateEventView(generic.UpdateView):
	success_url = '/Eventlist'
	template_name = 'add_event.html'
	form_class = EventListForm
	model = Event

	

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Youre now registered'))
			return redirect('/home')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'register.html', context)

def logout_user(request):
	logout(request)
	messages.success(request,('Youre now logged out'))
	return redirect('/home')

#class UserProfileView(LoginRequiredMixin, generic.DetailView):
#	login_url = '/login'
#	model = User
#	template_name = 'user_detail.html'
#	context_object_name = 'user'

#	def get_object(self):
#		return self.request.user

#	def get_context_data(self, **kwargs):
#		context = super().get_context_data(**kwargs)
#		context['blogs'] = Post.objects.filter(created_by=self.get_object())
#		return context



