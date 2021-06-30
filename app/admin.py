from django.contrib import admin
from .models import *
from .models import User, Client, Surveyor

# admin.site.register(User)
admin.site.register(Client)
  
admin.site.register(Surveyor)

admin.site.register(UserOTP)
class AnswerAdmin(admin.ModelAdmin):
    list_display=['id','answer']
admin.site.register(Answer,AnswerAdmin)

admin.site.register(CreateSurvey)

class ProjectNameAdmin(admin.ModelAdmin):
    list_display=['id','project_name','address','city','zip_code','mobile','description_req','image_req','audio_req']
admin.site.register(ProjectName,ProjectNameAdmin)

class ClientQuestionAdmin(admin.ModelAdmin):
    list_display=['id','project','question','option1','option2','option3','option4']
admin.site.register(ClientQuestion,ClientQuestionAdmin)

admin.site.register(SurveyDescription)
admin.site.register(AllImage)
admin.site.register(ImageDescription)
admin.site.register(AllVideo)




