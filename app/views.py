from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
import random
from .models import *
from .forms import LoginForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import forms
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.forms.utils import ErrorList
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm


def home_view(request): 
    return render(request,'quiz/index.html')

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'quiz/index.html')


#for showing signup/login button for client
def clientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'quiz/index.html')


#for showing signup/login button for surveyor
def surveyorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'quiz/index.html')


def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('/adminlogin/')
    return render(request,'accounts/register.html')

def client_register(request):
    userForm=forms.ClientUserForm()
    clientForm=forms.ClientForm()
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST)
        clientForm=forms.ClientForm(request.POST)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            client=clientForm.save(commit=False)
            client.user=user
            client.save()
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
        return HttpResponseRedirect('/clientlogin/')
    return render(request,'client/register.html',context=mydict)

def surveyor_register(request):
    userForm=forms.SurveyorUserForm()
    surveyorForm=forms.SurveyorForm()
    mydict={'userForm':userForm,'surveyorForm':surveyorForm}
    if request.method=='POST':
        userForm=forms.SurveyorUserForm(request.POST)
        surveyorForm=forms.SurveyorForm(request.POST)
        if userForm.is_valid() and surveyorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            surveyor=surveyorForm.save(commit=False)
            surveyor.user=user
            surveyor.save()
            my_surveyor_group = Group.objects.get_or_create(name='SURVEYOR')
            my_surveyor_group[0].user_set.add(user)
        return HttpResponseRedirect('/surveyorlogin/')
    return render(request,'surveyor/register.html',context=mydict)

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_client(user):
    return user.groups.filter(name='CLIENT').exists()

def is_surveyor(user):
    return user.groups.filter(name='SURVEYOR').exists()
    
def afterlogin_view(request):
    if is_surveyor(request.user):      
        return redirect('surveyor')          
    elif is_client(request.user):
            return redirect('client')   
    else:
        return redirect('home')

@login_required(login_url='adminlogin')
def home(request):
	clist=Client.objects.all()
	return render(request, 'admin/admin.html',{'clist':clist})


@login_required(login_url="adminlogin")  
def createprofile(request,project_id):
	releted_data=ProjectName.objects.get(id=project_id)	
	surveyor_list=Surveyor.objects.all()
	clients = Client.objects.filter(user_id=request.user.id)
	# print(request.user.id)
	if request.method=="POST":
		surveyor_id = request.POST.get('surveyor_name')
		releted_data.surveyor_id = surveyor_id
		for i in clients:
			releted_data.client_id = i.id
		releted_data.save()
	return render(request, 'admin/createsurvey.html',{'display':releted_data,'surveyor_list':surveyor_list})

@login_required(login_url='adminlogin')   
def editprofile(request):
    return render(request, 'admin/edit-profile.html')

@login_required(login_url="adminlogin")	
def listprofile(request):
	project_list= ProjectName.objects.filter(display__ques__isnull=False).distinct()
	return render(request, 'admin/list-products.html', {'project_list': project_list})


@login_required(login_url="adminlogin")   
def task(request):
    return render(request, 'admin/task.html')

@login_required(login_url='adminlogin')
def completesyrvey(request):
	clt=Client.objects.all()
	return render(request,'admin/Completesurvey.html',{'clt':clt})

@login_required(login_url='adminlogin')
def comsur(request):
	clt=ProjectName.objects.all()
	return render(request,'admin/Requestservey.html',{'clt':clt})

@login_required(login_url='adminlogin')
def complete_survey_view(request,project_id):
	project = ProjectName.objects.filter(id=project_id)
	return render(request,'admin/user-profile.html',{'project':project})

################################### client views ####################################################################

@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client(request):
    return render(request, 'client/client.html')

@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def ccreate(request):
	current_user=request.user.client.id
	if request.method == 'POST':
		project_name=request.POST['project_name']
		address=request.POST['address']
		city=request.POST['city']
		zip_code=request.POST['zip_code']
		mobile=request.POST['mobile']
		description_req=request.POST['check1']
		image_req=request.POST['check2']
		audio_req=request.POST['check3']
		
		newpost=ProjectName(client_id=current_user,project_name=project_name,address=address,city=city,zip_code=zip_code,mobile=mobile,description_req=description_req,
		image_req=image_req,audio_req=audio_req)
		newpost.save()
		a=ProjectName.objects.all().last()
		b=ProjectName.objects.get(id=a.id)
		ques=request.POST.getlist('question1')
		opt1=request.POST.getlist('opt1')
		opt2=request.POST.getlist('opt2')
		j=0
		for i in ques:
			a=ClientQuestion(project=b,question=i,option1=opt1[j],option2=opt2[j])
			a.save()
			j +=1	
		question=request.POST.getlist('question')
		option1=request.POST.getlist('option1')
		option2=request.POST.getlist('option2')
		option3=request.POST.getlist('option3')
		option4=request.POST.getlist('option4')
		j=0
		for i in question:
			newpost=ClientQuestion(project=b,question=i,option1=option1[j],option2=option2[j],option3=option3[j],option4=option4[j])
			newpost.save()
			j +=1	
	return render(request,'client/projectcreate.html')

@login_required(login_url='clientlogin')
@user_passes_test(is_client)   
def cedit(request):
    return render(request, 'client/edit-profile.html')

@login_required(login_url='clientlogin')
@user_passes_test(is_client)	
def clist(request):
	user_id = request.user.id
	project    = ProjectName.objects.filter(client__user_id=user_id,is_send=True)
	return render(request, 'client/list-products.html',{'project':project})

# @login_required(login_url='clientlogin')
# @user_passes_test(is_client)  
def clientallocate(request,id):
	ProjectName.objects.filter(id=id).update(is_send=True)
	return HttpResponseRedirect("/list/")

@login_required(login_url='clientlogin')
@user_passes_test(is_client)	
def ctask(request):
    return render(request, 'client/task.html')

@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def userprofile(request):
	return render(request, 'client/user-profile.html')

@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def userabc(request,project_id):
	project = ProjectName.objects.filter(id=project_id)
	return render(request,'client/user-profile.html',{'project':project})

########################## surveyor views ##############################################################

@login_required(login_url='surveyorlogin')
@user_passes_test(is_surveyor)
def surveyor(request):
	return render(request, 'surveyor/survy.html',{'clist':clist})

@login_required(login_url='surveyorlogin')
@user_passes_test(is_surveyor)
def listq(request,project_id):
	# project_list = ProjectName.objects.filter(surveyor_id__in=surveyor_ids)
	releted_data=ProjectName.objects.get(id=project_id)
	q = ClientQuestion.objects.filter(project_id=project_id)
	
	if request.method == 'POST':
		# print(request.POST)
		# import pdb
		# pdb.set_trace()

		releted_data=ClientQuestion.objects.filter(project_id=project_id)

		answer_list=[]
		description=request.POST.get("description")
		a=SurveyDescription.objects.create(project_des_id=project_id,description=description)
		for i in releted_data:
			# print(i.project_id)
			# que=exec(f'ques_{i.id}')
			ans=request.POST.get(f'{i.id}')
			# answer_list.append(Answer(ques_id=i.id,answer=ans))
			Answer.objects.update_or_create(ques_id=i.id,defaults={'answer':ans})
		# Answer.objects.bulk_create(answer_list)
		releted_data=ProjectName.objects.get(id=project_id)
		abc=releted_data.id
	    
		img_uplod=request.FILES.getlist("image")
		for i in img_uplod:
			a=AllImage(image=i,proj_name_id=abc)
			a.save()
			
		image_description=request.POST.getlist("image_description")
		for i in image_description:
			a=ImageDescription(description=i)
			a.save()
		video=request.FILES.getlist("Videos")
		for i in video:
			a=AllVideo(video=i,projec_name_id=abc)
			a.save()
		
	return render(request,'surveyor/projectcreate.html',{'display':releted_data})

@login_required(login_url='surveyorlogin')
@user_passes_test(is_surveyor)
def allsurvey(request):
	user_id = request.user.id
	project_list= ProjectName.objects.filter(display__ques__isnull=False, surveyor__user_id =user_id).distinct()
	return render(request,'surveyor/list-products.html',{'project_list':project_list})

@login_required(login_url='surveyorlogin')
@user_passes_test(is_surveyor)
def surveylist(request):
	# import pdb
	# pdb.set_trace()
	user_id = request.user.id
	# surveyors = Surveyor.objects.all()
	# surveyor_ids = [i.id for i in surveyors]
	project_list = ProjectName.objects.filter(surveyor__user_id =user_id)
	context = {'project_list': project_list}
	return render(request,'surveyor/Requestsarvey.html',context)

@login_required(login_url='surveyorlogin')
@user_passes_test(is_surveyor)
def complete_view(request,project_id):
	project = ProjectName.objects.filter(id=project_id)
	return render(request,'surveyor/user-profile.html',{'project':project})

def quiz(request):
	return render(request,'surveyor/quiz.html')



def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("afterlogin")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

# def register_user(request):
# 	if request.method == 'POST':
# 		get_otp = request.POST.get('otp') #213243 #None

# 		if get_otp:
# 			get_usr = request.POST.get('usr')
# 			usr = User.objects.get(username=get_usr)
# 			if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
# 				usr.is_active = True
# 				usr.save()
# 				messages.success(request, f'Account is Created For {usr.username}')
# 				return redirect('login')
# 			else:
# 				messages.warning(request, f'You Entered a Wrong OTP')
# 				return render(request, 'accounts/register.html', {'otp': True, 'usr': usr})

# 		form = SignUpForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data.get('username')
# 			name = form.cleaned_data.get('name').split(' ')

# 			usr = User.objects.get(username=username)
# 			usr.email = username
# 			usr.first_name = name[0]
# 			if len(name) > 1:
# 				usr.last_name = name[1]
# 			usr.is_active = False
# 			usr.save()
# 			usr_otp = random.randint(100000, 999999)
# 			UserOTP.objects.create(user = usr, otp = usr_otp)

# 			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

# 			send_mail(
# 				"Welcome to USURVEY - Verify Your Email",
# 				mess,
# 				settings.EMAIL_HOST_USER,
# 				[usr.email],
# 				fail_silently = False
# 				)

# 			return render(request, 'accounts/register.html', {'otp': True, 'usr': usr})

		
# 	else:
# 		form = SignUpForm()

# 	return render(request, 'accounts/register.html', {'form':form})

def logoutUser(request):
	logout(request)
	return redirect('/')
def forget_user(request):
    return render(request, 'accounts/forget-password.html')

def resend_otp(request):
	if request.method == "GET":
		get_usr = request.GET['usr']
		if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
			usr = User.objects.get(username=get_usr)
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)
			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to USERVEY - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)
			return HttpResponse("Resend")

	return HttpResponse("Can't Send ")

# User Profile View
# def profile(request, username):
# 	user = User.objects.filter(username=username)
# 	if not user:
# 		raise Http404()
# 	if request.user == user.first():
# 		if request.method == 'POST':
# 			passChangeForm = PasswordChangeForm(request.user, request.POST)
# 			if passChangeForm.is_valid():
# 				passChangeForm.save()
# 				messages.success(request, f'Password had been changed successfully')
# 		else:
# 			passChangeForm = PasswordChangeForm(request.user)
# 		parms = {
# 			'passChangeForm' : passChangeForm,
# 			'useritself': True,
# 			'user': request.user
# 			}
# 		# return render(request, 'user/profile.html', parms)
# 	else:
# 		parms = {
# 			'useritself': False,
# 			'user': user.first(),
# 		}

# 	posts = Post.objects.filter(user = user.first()).order_by('-created_at')

# 	all_post = Paginator(posts,10)
# 	page = request.GET.get('page')
# 	try:
# 		posts = all_post.page(page)
# 	except PageNotAnInteger:
# 		posts = all_post.page(1)
# 	except EmptyPage:
# 		posts = all_post.page(all_post.num_pages)

# 	parms['posts'] = posts
# 	return render(request, 'user/profile.html', parms)

# This view is used to change profile pic, cover image, about, dob and more user details
# @login_required
# def ChangeIntoProfile(request, fieldname):
# 	prof = request.user.profile

# 	#Change Profile Picture
# 	if fieldname == 'profile_pic':
# 		img = request.FILES.get('profile_pic')
# 		if img:
# 			prof.profile_pic = img
# 			prof.save()
# 		return redirect(f"/user/{request.user}")
# 	# Change Cover Image
# 	elif fieldname == 'cover_image':
# 		img = request.FILES.get('cover_image')
# 		if img:
# 			prof.cover_image = img
# 			prof.save()
# 		return redirect(f"/user/{request.user}")


# 	value = request.GET.get('value')
# 	if not value:
# 		raise Http404()
# 	# print(value, fieldname)

# 	# Change Name
# 	if fieldname == 'name':
# 		name = value.split(' ')
# 		request.user.first_name = name[0]
# 		if len(name) > 1:
# 			request.user.last_name = name[1]
# 		request.user.save()
# 	# Change About Me
# 	elif fieldname == 'aboutme':
# 		prof.about_me = value
# 		prof.save()
# 	#Change Date of Birth
# 	elif fieldname == 'dob':
# 		prof.birthday = value
# 		prof.save()
# 	#Change Gender
# 	elif fieldname == 'gender':
# 		if value == "Male":
# 			prof.gender = "Male"
# 			prof.save()
# 		elif value == "Female":
# 			prof.gender = 'Female'
# 			prof.save()
# 		elif value == "Other":
# 			prof.gender = "Other"
# 			prof.save()
# 	else:
# 		raise Http404()
# 	return HttpResponse(value)

# @login_required
# @csrf_exempt
# def following(request):
# 	if request.method == 'POST' and request.user.is_authenticated:
# 		data = {}
# 		for usr in request.user.profile.following.all():
# 			data[usr.id] = {
# 			 'first_name' : usr.first_name,
# 			 'last_name': usr.last_name,
# 			 'username' : usr.username,
# 			 'pic' : usr.profile.profile_pic.url
# 			 }
		
# 		return JsonResponse(data)
# 	raise Http404()

# @login_required
# @csrf_exempt
# def followers(request):
# 	if request.method == 'POST' and request.user.is_authenticated:
# 		data = {}
# 		for usr in request.user.profile.followers.all():
# 			data[usr.id] = {
# 			 'first_name' : usr.first_name,
# 			 'last_name': usr.last_name,
# 			 'username' : usr.username,
# 			 'pic' : usr.profile.profile_pic.url,
# 			 'followed_back': usr in request.user.profile.following.all()
# 			 }
		
# 		return JsonResponse(data)
# 	raise Http404()
# @login_required
# def notifications(request):
# 	noti = Notification.objects.filter(user=request.user, seen = False)
# 	noti = serializers.serialize('json', noti)
# 	return JsonResponse({'data':noti})

# @login_required
# def notifications_seen(request):
# 	Notification.objects.filter(user=request.user, seen = False).update(seen = True)
# 	return HttpResponse(True)

# @csrf_exempt
# @login_required
# def clear_notifications(request):
# 	if request.method == "POST":
# 		Notification.objects.filter(user=request.user).delete()
# 		return HttpResponse(True)
# 	return HttpResponse(False)

# def islogin(request):
# 	return JsonResponse({'is_login':request.user.is_authenticated})

def addquestion(request):
	ques=Question.objects.all()
	return render(request, 'add.html', {'ques':ques})

def usercreate(request):
	
	return render(request, 'usercreate.html', {'ques':ques})
def survecreate(request):
	
	return render(request, 'survcreate.html', {'ques':ques})
def clientquestion(request):
	
	return render(request, 'clientquestion.html', {'ques':ques})




