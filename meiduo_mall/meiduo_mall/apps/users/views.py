import re

from django import http
from django.contrib.auth import login
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic.base import View
from pymysql import DatabaseError

from users.models import User
from users.response_code import RETCODE


class RegisterView(View):

    """用户注册"""

    def get(self,request):
        """用户注册后端逻辑"""


        return render(request,'register.html')


    def post(self,request):
        """
        实现用户注册逻辑
        :param request:
        :return:
        """
        
        #1.接收参数
        username=request.POST.get('username')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        mobile=request.POST.get('mobile')
        # sms_code=request.POST.get('sms_code')
        allow=request.POST.get('allow')
        #2.校验参数
        if not all([username,password,password2,mobile,allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden('请输入5到20位的用户名')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        #3.保存数据
        try:
            user=User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            return render(request,'register.html',{'errmsg':'注册失败'})


        login(request,user)

        #4.响应注册结果（注册结果重定向到首页）
        return redirect(reverse('contents:index'))

class UsernameCountView(View):
    """判断用户名是否重复注册"""
    def get(self,request,username):
        """
        用户名是否重复注册后端逻辑
        :param request:
        :param username:
        :return:
        """
        count=User.objects.filter(username=username).count()

        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'ok',
            'count':count
        })


class UsernameMobileCountView(View):
    """判断手机号是否重复"""
    def get(self,request,mobile):
        """
        判断手机号是否重复后端逻辑
        :param request:
        :param mobile:
        :return:
        """
        count=User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'ok',
            'count':count
        })




