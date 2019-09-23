from django.shortcuts import render,redirect,reverse, get_object_or_404
from django.contrib.auth import authenticate,login as dj_login
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from django.template import RequestContext
# from django.contrib.auth.forms import CustomUserLoginForm
from .forms import SignUpForm,PasswordForm, LoginForm,UpdateProfile,AddStudentForm,AssignmentForm,AssignmenttForm,AssignmentForm1,ReviewForm,MessageForm
from django.contrib.auth.forms import PasswordChangeForm
# from .templates import  ValidCaptcha
import json
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from core.tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from friendship.models import Friend, Follow, FriendshipRequest, Block
from django.views.generic import View
from django import template
from django.db.models import Count
register = template.Library()
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# # from .serializers import  MessagesSerializer,UserProfileSerializer
from django.db.models import Q



from friendship.exceptions import AlreadyExistsError,AlreadyFriendsError
User = get_user_model()

get_friendship_context_object_name = lambda: getattr(
    settings, "FRIENDSHIP_CONTEXT_OBJECT_NAME", "user"
)
get_friendship_context_object_list_name = lambda: getattr(
    settings, "FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME", "users"
)









def indexx(request):
     return render(request, 'layout.html')     




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # if Captcha.is_valid():
                user= form.save(commit=False)
                user.user_type = form.cleaned_data.get('user_type')
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)) ,
                    'token':account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
            
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
        
    return render(request, 'registration/signup.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        dj_login(request, user)
        return HttpResponseRedirect(reverse('pass', args=(uid,)))
        # return redirect('pass')
    else:
        return HttpResponse('Activation link is invalid!')


# ---------set password after activation of link----------

def password(request,uid):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=uid)
            password= request.POST.get('password')
            password= form.cleaned_data['password']
            user.set_password(password)
            user.save()
            dj_login(request,user)
            return redirect('login1')
    else:
         form = PasswordForm()    
    return render(request, "gen_pas.html", {'form': form})



# ----------same login for both teacher and student----------- 

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'] ,password=request.POST['password'])

        if user is not None:
            if user.is_active:
             dj_login(request, user)
            
            if user.user_type =='student':  
                return redirect('profile') 
            elif user.user_type =='teacher':
                return redirect('profile') 
    else:
        form = PasswordForm()    
        
    return render(request, "registration/login.html", {'form': form})        




# ---------different dashboard after login---------

@login_required
def profile(request):   
        user=request.user
        users = User.objects.all()
        if user.user_type =='teacher':
            return render(request, 'teacher_profile.html', {"users":users})
        elif user.user_type =='student':  
            return render(request, 'student_profile.html', {"users":users})
        else: 
            return redirect('layout.html')


# updation of profile--------------------

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateProfile(request.POST, request.FILES , instance=request.user)
        
        if (user_form.is_valid()):
           
            user_form.save()            
            return HttpResponseRedirect(reverse('profile'))
        
    else:
        user_form = UpdateProfile(instance=request.user)
    if request.user.user_type =='student':    
        return render(request, 'registration/update_profile_student.html', {'user_form': user_form })
    if request.user.user_type =='teacher':  
        return render(request, 'registration/update_profile_teacher.html', {'user_form': user_form})      
    



#--------change password-----------

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            pass
    else:
        form = PasswordChangeForm(request.user)
    if request.user.user_type =='teacher':      
        return render(request, 'change_password.html', {'form': form})
    if request.user.user_type =='student':
        return render(request, 'studentchange_password.html', {'form': form})    


# Teacher can add student----------------------- 

def addstudent(request):
    if request.user.user_type =='teacher':  
        if request.method == 'POST':
            form = AddStudentForm(request.POST)
            if form.is_valid():
                    user= form.save(commit=False)
                    user.user_type = form.cleaned_data.get('user_type')
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your blog account.'
                    message = render_to_string('acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)) ,
                        'token':account_activation_token.make_token(user),
                    })
                    to_email = form.cleaned_data.get('email')
                
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()
                    return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = AddStudentForm()
            
        return render(request, 'registration/add_student.html', {'form': form})   
    else:
        return render(request,'error.html')


 #   list of student in teacher dashboard---------------
def student_list(request): 
    if request.user.user_type =='teacher':    
        dataa=User.objects.filter(user_type = 'student')
        
        context = {
                'dataa':dataa 
        }
        return render(request,'student_list.html',context=context)    
    else:
        return render(request,'error.html')



#-----------list of teacher in student dashboard-----------

def teacher_list(request):   
    if request.user.user_type =='student':  
        dataa=User.objects.filter(user_type = 'teacher')
        
        context = {
                'dataa':dataa 
        }
        return render(request,'teacher_list.html',context=context)    
    else:
        return render(request,'error2.html')



# ---------------student dashboard for making request---------

def friendship_add_friend(request,teacher_id):
    if request.user.user_type =='student':  
        ctx = {"teacher_id": teacher_id}
        if request.method == "POST":
            print("dsad")
            to_user = User.objects.get(pk=teacher_id)
            from_user = request.user
            print(to_user)
            try:
                Friend.objects.add_friend(from_user,to_user)
                print("hghjgj")
            except AlreadyFriendsError as e:
                ctx["errors"] = ["%s" % e]
            else:
                return redirect("student_profile")

        return render(request,"friendship/friend/add.html",ctx)
    else:
        return render(request,'error2.html')



# -----------teacher dashboard for rejecting and accepting request--------------
def friendship_reject(request, friendship_request_id):
    if request.user.user_type =='teacher':
        if request.method == "POST":
            print("dasc")
            f_request = get_object_or_404(request.user.friendship_requests_received, id=friendship_request_id)
            f_request.reject()
            f_request.delete()
            return redirect("teacher_profile")

        return redirect(
            "friendship_requests_detail", friendship_request_id=friendship_request_id)
    else:
        return render(request,'error.html')


def friendship_accept(request, friendship_request_id):
    if request.user.user_type =='teacher':
        if request.method == "POST":
            f_request = get_object_or_404(request.user.friendship_requests_received, id=friendship_request_id)
            f_request.accept()
            return redirect("stu_joined", username=request.user.username)

        return redirect("friendship_requests_detail", friendship_request_id=friendship_request_id) 
    else:
        return render(request,'error.html')



def friendship_request_list(request):
    if request.user.user_type =='teacher':
        friendship_requests = Friend.objects.requests(request.user)
        # This shows all friendship requests in the database
        # friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

        return render(request,"friendship/friend/requests_list.html", {"requests": friendship_requests})  
    else:
        return render(request,'error.html')


def friendship_requests_detail(request, friendship_request_id):
    if request.user.user_type =='teacher':
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

        return render(request, "friendship/friend/request.html", {"friendship_request": f_request})
    else:
        return render(request,'error.html')    


def view_friends(request, username, template_name="friendship/friend/user_list.html"):
    if request.user.user_type =='teacher':
        user = get_object_or_404(User, username=username)
        friends = Friend.objects.friends(user)
        return render(request, template_name, {get_friendship_context_object_name(): user,'friendship_context_object_name': get_friendship_context_object_name(),'friends': friends,})
    else:
        return render(request,'error.html')



# student dashbord---------------------------
def view_friend(request,teacher_id):
    if request.user.user_type =='student':
        user = get_object_or_404(User,id=teacher_id)
        friends = Friend.objects.friends(user)
        return render(request, "friendship/friend/taccepted_list.html", {get_friendship_context_object_name(): user,'friendship_context_object_name': get_friendship_context_object_name(),'friends': friends,})  
    else:
        return render(request,'error2.html')

    
#teacher dashboard----------------------------    
def view_friendss(request,teacher_id):    
    if request.user.user_type =='teacher':
        user = get_object_or_404(User,id=teacher_id)
        friends = Friend.objects.friends(user)
        return render(request, "friendship/friend/saccepted_list.html", {get_friendship_context_object_name(): user,'friendship_context_object_name': get_friendship_context_object_name(),'friends': friends,})  
    else:
        return render(request,'error.html')
    


# request for assignment to teacher--------------------

def ass_request(request,teacher_id):
    if request.user.user_type =='student':
        ctx = {"teacher_id": teacher_id}
        if request.method == "POST":
            form = AssignmenttForm(request.POST,initial={'request':True})

            if form.is_valid():
                user= form.save(commit=False)
                print("dsad")
                user.teacher = User.objects.get(pk=teacher_id)
                user.student = request.user
                user.save()
                return redirect('profile')
        else:
            form = AssignmenttForm       
        return render(request,"friendship/friend/ass_request.html",ctx)
    else:
        return render(request,'error2.html')

# list of student requested for assignment---------------------------

def studentass_list(request):
    if request.user.user_type =='teacher':
        dataa = Assignment_Request.objects.filter(teacher=request.user)
        
        context = {
                'dataa':dataa 
        }
        return render(request,'ass_request2.html',context=context)    
    else:
        return render(request,'error.html')



#   teacher can send assignment------------------ 
def teacher_assignment(request,student_id):  
    if request.user.user_type =='teacher':      
        if request.method == 'POST':
            form = AssignmentForm(request.POST, request.FILES,)
            if form.is_valid():
                a = form.save()
                a.student = User.objects.get(pk = student_id)
                a.teacher = request.user
                a.description = form.cleaned_data['description']
                a.as_file = form.cleaned_data['as_file']
                # a.Submit_date = form.cleaned_data['Submit_date']
                a.save()
                return redirect('profile')
                
        else:
            form = AssignmentForm()
        return render(request, 'teacher_assignment.html', {'form': form}) 
    else:
        return render(request,'error.html')



def student_assignment(request,student_id,ass_id):  
    if request.user.user_type =='student':
        if request.method == 'POST':
            form = AssignmentForm1(request.POST, request.FILES,)
            if form.is_valid():
                c = Assignment.objects.get(id = ass_id)
                d = c . Submit_date
                if d > timezone.now():
                    a = form.save()
                    a.teacher = User.objects.get(pk = student_id)
                    a.student = request.user
                    a.assignment =  Assignment.objects.get(id = ass_id)
                    a.description = form.cleaned_data['description']
                    a.submitted_file = form.cleaned_data['submitted_file']
                    a.save()
                    return redirect('profile')
                else:
                   return render(request,'validationerror.html')
        else:
            form = AssignmentForm1()
        return render(request, 'student_assignment.html', {'form': form})     
    else:
        return render(request,'error2.html')


# list of assignments sent by teachers-------------------------
def submit_ass(request):
    if request.user.user_type =='student':
        dataa = Assignment.objects.filter(student=request.user)
        
        context = {
                'dataa':dataa 
        }
        return render(request,'submit_ass.html',context=context) 
    else:
        return render(request,'error2.html')




def check_ass(request):
    if request.user.user_type =='teacher':
        dataa = Submission.objects.filter(teacher=request.user)
        
        context = {
                'dataa':dataa 
        }
        return render(request,'check_ass.html',context=context)     
    else:
        return render(request,'error.html')


def remark_ass(request,student_id,ass_id):
    if request.user.user_type =='teacher':
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES,)
            if form.is_valid():
                a = form.save()
                a.student = User.objects.get(pk = student_id)
                a.assignment = Submission.objects.get(id = ass_id)
                a.teacher = request.user
                a.rating = form.cleaned_data['rating']
                a.save()
                return redirect('profile')
                
        else:
            form = ReviewForm()
        return render(request, 'reviews.html', {'form': form})
    else:
        return render(request,'error.html')

def check_remarks(request):
    if request.user.user_type =='student':
        dataa = Remark.objects.filter(student=request.user)
        
        context = {
                'dataa':dataa 
        }
        return render(request,'check_remarks.html',context=context)     
    else:
        return render(request,'error2.html')


# student dashboard-----------------------------
def messages(request,teacher_id):
    if request.user.user_type =='teacher':  
        user = get_object_or_404(User,pk=teacher_id)
        friends = Friend.objects.friends(user)
        if friends:
            if request.method == 'POST':
                form =MessageForm(request.POST)
                if form.is_valid():
                    a = form.save()
                    a.receiver = User.objects.get(pk = teacher_id)
                    a.sender = request.user
                    a.msg = form.cleaned_data['msg']
                    a.save()
                    return HttpResponseRedirect(reverse('messages',args=(teacher_id,)))       
            else:
                form = MessageForm()
                query = Q(Q(sender=request.user)&Q(receiver=teacher_id))|Q(Q(sender=teacher_id)&Q(receiver=request.user))
                dataa = Messages.objects.filter(query).order_by('timestamp')  
            return render(request, 'messenger.html', {'form': form,'dataa':dataa})
        else:
            return render(request,'error.html')
    else: 
        return render(request,'error.html')       



def messagess(request,student_id):
    if request.user.user_type =='student':
        user = get_object_or_404(User,pk=student_id)
        friends = Friend.objects.friends(user)
        if friends:
            if request.method == 'POST':
                form =MessageForm(request.POST)
                if form.is_valid():
                    a = form.save()
                    a.receiver = User.objects.get(pk = student_id)
                    a.sender = request.user
                    a.msg = form.cleaned_data['msg']
                    a.save()
                    return HttpResponseRedirect(reverse('messagess',args=(student_id,)))
                    
            else:
                form = MessageForm()
                query = Q(Q(sender=request.user)&Q(receiver=student_id))|Q(Q(sender=student_id)&Q(receiver=request.user))
                dataa = Messages.objects.filter(query).order_by('timestamp')
            return render(request, 'messenger2.html', {'form': form,'dataa':dataa})
        else:
            return render(request,'error2.html')
    else:
            return render(request,'error2.html')











def check_messages(request):
    if request.user.user_type =='teacher': 
        dataa = Messages.objects.filter(receiver=request.user)
        
        context = {
                'dataa':dataa 
        }
        return render(request,'studentmsg.html',context=context)     
    else:
        return render(request,'error.html')


def check_tmessages(request):
    if request.user.user_type =='student': 
        dataa = Messages.objects.filter(receiver=request.user)
        
        context = {
                'dataa':dataa 
        }
        return render(request,'teachermsg.html',context=context)         
    else:
        return render(request,'error2.html')



