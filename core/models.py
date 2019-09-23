from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from .validators import validate_file_extension,validate_file1_extension
from .signals import *
from datetime import datetime,timedelta
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def validate_image(image):     
    file_size = image.file.size
    limit_mb = 2
    if file_size >limit_mb * 1024 * 1024:
       raise ValidationError("Max size of file is %s MB" % limit_mb)

ROLE = (
      ('student','student'),
      ('teacher','teacher'),
  )


class User(AbstractUser):
    
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=254,unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    user_type = models.CharField(choices=ROLE,max_length=15)
    Image = models.ImageField(upload_to='images/',validators=[validate_file_extension,validate_image])
   

class Assignment_Request(models.Model):
    teacher = models.ForeignKey( User,on_delete=models.CASCADE,null=True,related_name='teacherr')
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name='studentt')
    request = models.BooleanField(default=True)



def get_deadline():
    return datetime.today()+timedelta(days=10)


class Assignment(models.Model):
   
    teacher = models.ForeignKey( User,on_delete=models.CASCADE,null=True,related_name='teacher')
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name='student')
    description = models.CharField(max_length=255, blank=True)
    as_file = models.FileField(upload_to='documents/', validators=[validate_file1_extension])
    Submit_date = models.DateTimeField(default=get_deadline,blank=True)
    uploaded = models.DateTimeField(default=datetime.now,blank=True)







class Submission(models.Model):
   
    teacher = models.ForeignKey( User,on_delete=models.CASCADE,null=True,related_name='teachers')
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name='students')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True,related_name='assignment')
    submitted_file = models.FileField(upload_to='documents/', validators=[validate_file1_extension])
    description = models.CharField(max_length=255, blank=True)
    Submitted_date = models.DateTimeField(default=datetime.now,blank=True)



STAR = (
      ('1star','1star'),
      ('2star','2star'),
      ('3star','3star'),
      ('4star','4star'),
      ('5star','5star'),
      
  )







class Remark(models.Model):
    teacher = models.ForeignKey( User,on_delete=models.CASCADE,null=True,related_name='teacherss')
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name='studentss') 
    assignment = models.ForeignKey(Submission, on_delete=models.CASCADE, null=True,related_name='assignments')
    rating = models.CharField(choices=STAR,max_length=25, null=True, blank=True)
    

   

class Messages(models.Model):

    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE, null=True)
    msg = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(default=datetime.now,blank=True)
    
    class Meta:
        verbose_name_plural = "Messages"
    
    def __str__(self):
        return str(self.id) + ": from " + str(self.sender) + " to " + str(self.receiver)

  

    

