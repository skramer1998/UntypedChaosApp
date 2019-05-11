"""UntypedChaosApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from FSA.views import logviews, registerviews, userviews, courseviews, sectionviews, mycoursesview, labviews,\
    edituserviews, mysectionsview, mylabsview, courseinfoviews

urlpatterns = (
    url('admin/', admin.site.urls),
    url(r'^register/$', registerviews.Register.as_view(), name="register"),
    url(r'^$', logviews.Login.as_view(), name="login"),
    url(r'^user/$', userviews.UserView.as_view(), name="user"),
    url(r'^courses/$', courseviews.Courses.as_view(), name="courses"),
    url(r'^logout/$', logviews.LogoutView.as_view(), name="logout"),
    url(r'^registerloggedin/$', registerviews.RegisterLoggedIn.as_view(), name="registerloggedin"),
    url(r'^courseview/$', courseviews.CourseView.as_view(), name="courseview"),
    url(r'^sectionview/$', sectionviews.SectionView.as_view(), name="sectionview"),
    url(r'^mycourses/$', mycoursesview.MyCourses.as_view(), name="mycoursesview"),
    url(r'^labview/$', labviews.LabView.as_view(), name="labview"),
    url(r'^edituser/$', edituserviews.EditUserView.as_view(), name="edituser"),
    url(r'^mysections/$', mysectionsview.MySectionsView.as_view(), name="mysections"),
    url(r'^mylabs/$', mylabsview.MyLabsView.as_view(), name="mylabs"),
    url(r'^courseinfo/$', courseinfoviews.CourseInfoView.as_view(), name="courseinfo")
)
