from django.contrib import admin
from core.models import *  


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name','email','user_type')

admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Assignment_Request)
admin.site.register( Remark)
# admin.site.register(Chat)
admin.site.register(Messages)