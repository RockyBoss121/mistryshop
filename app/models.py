
from django.contrib.auth.models import AbstractUser,User,AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE,related_name="client")
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class Surveyor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
 
class UserOTP(models.Model):
	userotp = models.ForeignKey(User, on_delete = models.CASCADE)
	time_st = models.DateTimeField(auto_now = True)
	otp = models.SmallIntegerField()

def upload_profile_to(instance,filename):
	return f'profile_picture/{instance.user.username}/{filename}'

def upload_cover_to(instance,filename):
	return f'coverImage/{instance.user.username}/{filename}'

class CreateSurvey(models.Model):
   survey_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   def __str__(self):
        return self.survey_name

class ProjectName(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True,related_name="user")
    client=models.ForeignKey(Client,on_delete=models.CASCADE, null=True,blank=True,related_name="client")
    surveyor=models.ForeignKey(Surveyor,on_delete=models.CASCADE, null=True,blank=True,related_name="surveyor")
    project_name=models.CharField(max_length=500,null=True,blank=True)
    address=models.TextField(null=True, blank=True)
    city=models.CharField(max_length=200,null=True, blank=True)
    zip_code=models.CharField(max_length=20,null=True, blank=True)
    mobile=models.IntegerField(null=True, blank=True)
    description_req=models.CharField(max_length=20,null=True, blank=True)
    enter_description=models.TextField(null=True, blank=True)
    image_req=models.CharField(max_length=20,null=True, blank=True)
    upload_image_des=models.TextField(null=True, blank=True)
    audio_req=models.CharField(max_length=20,null=True, blank=True)
    upload_video_des=models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(default=False)
    def __str__(self):
        return str(self.project_name)

class ClientQuestion(models.Model):
    project=models.ForeignKey(ProjectName,on_delete=models.CASCADE,related_name="display",null=True,blank=True)
    question=models.CharField(max_length=600,null=True, blank=True)
    option1=models.CharField(max_length=200,null=True, blank=True)
    option2=models.CharField(max_length=200,null=True, blank=True)
    option3=models.CharField(max_length=200,null=True, blank=True)
    option4=models.CharField(max_length=200,null=True, blank=True)
    def __str__(self):
        return str(self.question)
    
class SurveyDescription(models.Model):
    project_des=models.ForeignKey(ProjectName,on_delete=models.CASCADE,related_name="project_des",null=True,blank=True)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.description)
    
class Answer(models.Model):
    ques=models.OneToOneField(ClientQuestion,on_delete = models.CASCADE,related_name="ques",null=True,blank=True)
    answer=models.CharField(max_length=200,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.answer)

class AllImage(models.Model):
    proj_name=models.ForeignKey(ProjectName,on_delete=models.CASCADE,related_name="proj_name",null=True,blank=True)
    image=models.ImageField(upload_to="image/%y", null=True,blank=True)
    def __str__(self):
        return str(self.image)

class ImageDescription(models.Model):
    img_name=models.ForeignKey(ProjectName,on_delete=models.CASCADE,related_name="img_name",null=True, blank=True)
    img=models.OneToOneField(AllImage,on_delete = models.CASCADE,related_name="img",null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.description)
        
class AllVideo(models.Model):
    projec_name=models.ForeignKey(ProjectName,on_delete=models.CASCADE,related_name="projec_name",null=True,blank=True)
    video=models.FileField(upload_to="video/%y",null=True,blank=True)
    def __str__(self):
        return str(self.video)

