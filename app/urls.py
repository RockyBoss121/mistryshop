# from app import views
from django.urls import path,include
from app import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login',views.login_view,name='login'),
    path('',views.home_view,name='index'),
    path('about_us',views.aboutus,name='about_us'),
    path('contact_us',views.contactus,name='contact_us'),

    ############ Admin Related Urls  ###################################################
    path('home/' ,views.home , name="home"),
    path('edit/' , views.editprofile , name="edit"),
    path('list/' , views.listprofile , name="list"),
    path('create/<int:project_id>' , views.createprofile , name="create"),
    path('task/' , views.task , name="task"),
    path('requestservey/',views.comsur,name="requestservey"),
    path('complete_survey_view/<int:project_id>',views.complete_survey_view,name="complete_survey_view"),
    path('completesurvey/',views.completesyrvey,name="completesurvey"),
    
    ########## Client Related Urls ######################################################
    path('client/' , views.client , name="client"), 
    path('ccreate/' , views.ccreate , name="ccreate"),
    path('clist/' , views.clist , name="clist"),
    path('cedit/' , views.cedit , name="cedit"),
    path('ctask/' , views.ctask , name="ctask"),
    path('userprofile/' , views.userprofile , name="userprofile"),
    path('userabc/<int:project_id>',views.userabc, name="userabc"),
    path('clientallocate/<int:id>',views.clientallocate,name="clientallocate"),

    path('adminclick', views.adminclick_view),
    path('clientclick', views.clientclick_view),
    path('surveyorclick', views.surveyorclick_view),

    path('register/', views.admin_signup_view, name="adminsignup"),
    path('client_register/',views.client_register, name='client_register'),
    path('surveyor_register/',views.surveyor_register, name='surveyor_register'),
    path('afterlogin/', views.afterlogin_view,name='afterlogin'),

    # path('adminlogin/', views.login_view,name='adminlogin'),###when we provide only one url then this 3 line is commennted
    # path('clientlogin/', views.login_view,name='clientlogin'),
    # path('surveyorlogin/', views.login_view,name='surveyorlogin'),

    ############# Surveyor Related Urls #################################################
    path('surveyor/' , views.surveyor , name="surveyor"),
    path('listq/<int:project_id>',views.listq,name='listq'),
    path('surveylist/',views.surveylist,name="surveylist"),
    path('allsurvey/',views.allsurvey,name="allsurvey"),
    path('complete_view/<int:project_id>',views.complete_view, name="complete_view"),

   
    path('forget/', views.forget_user, name="forget"),      
    path('logout/', views.logoutUser, name="logout"),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_complete"),

    path('resendOTP/',views.resend_otp),
    path('contactus/',views.contactus),
    path('create-pdf/<int:project_id>', views.pdf_report_create, name='create-pdf'),

   
]
