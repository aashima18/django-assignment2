from django.urls import path
from django.conf.urls import url
from .import views
from .views import *
# from .views import AuthView, MessengerView, RestAPIView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
    path('',views.indexx,name='indexx'),
    path('pass/<int:uid>',views.password,name='pass'),
    path('login1/',views.user_login,name='login1'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    path('profile/',views.profile,name='profile'),
    path('editprofile/',views.update_profile,name='editprofile'), 
    url(r'^password/$', views.change_password, name='change_password'),

    path('addstudent/',views.addstudent,name='addstudent'),
    path('studentlist/',views.student_list,name='studentlist'),
    path('sendassignment/<int:student_id>/',views.teacher_assignment,name='assignment'),
    path('sendassignments/<int:student_id>/<int:ass_id>/',views.student_assignment,name='s_assignment'),
    path('teacherlist/',views.teacher_list,name='teacherlist'),

    path('trequest/<int:teacher_id>/',views.friendship_add_friend,name='teacher_request'),
    path('request_list/',views.friendship_request_list,name='request_list'),
    path('request_details/<int:friendship_request_id>/',views.friendship_requests_detail,name='requests_detail'),
    path('request_reject/<int:friendship_request_id>/',views.friendship_reject,name='requests_reject'),
    path('request_accept/<int:friendship_request_id>/',views.friendship_accept,name='requests_accept'),
    path('accepted_request/<int:teacher_id>',views.view_friend,name='accepted_request'),
    path('stu_joined/<str:username>',views.view_friends,name='stu_joined'),
    path('accepted_trequest/<int:teacher_id>',views.view_friendss,name='accepted_trequest'),


    path('ass_request/<int:teacher_id>',views.ass_request,name='ass_request'),
    path('studentass_list/',views.studentass_list,name='studentass_list'),
    path('submit_ass/',views.submit_ass,name='submit_ass'),
    path('check_ass/',views.check_ass,name='check_ass'),
    path('remark_ass/<int:student_id>/<int:ass_id>',views.remark_ass,name='remark_ass'),
    path('check_remarks/',views.check_remarks,name='check_remarks'),

    path('messages/<int:teacher_id>',views.messages,name='messages'),
    path('messagess/<int:student_id>',views.messagess,name='messagess'),
    path('messages/',views.check_messages,name='check_messages'),
    path('tmessages/',views.check_tmessages,name='check_tmessages'),
    

]