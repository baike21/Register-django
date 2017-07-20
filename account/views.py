# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from account.models import User


# Create your views here.
# def index(request):
#    return render(request, 'ceshi.html')


# 注册表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput())
    phone = forms.IntegerField(label='手机号码')
    email = forms.EmailField(label='邮箱地址')


# 登录表单
class LoginUserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


# 修改密码表单
class ChangePasswordForm(forms.Form):
    username = forms.CharField(required=True, label='用户名', max_length=32)
    oldpassword = forms.CharField(required=True, label='旧密码', widget=forms.PasswordInput())
    newpassword = forms.CharField(required=True, label='新密码', widget=forms.PasswordInput())
    newpassword2 = forms.CharField(required=True, label='确认新密码', widget=forms.PasswordInput())


# 注册
def register(request):
    # 如果是POST请求
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            password2 = uf.cleaned_data['password2']
            phone = uf.cleaned_data['phone']
            email = uf.cleaned_data['email']
            # 如果没有重名，添加到数据库
            if not User.objects.filter(username=username):
                if password == password2:
                    User.objects.create(username=username, password=password, phone=phone, email=email)
                    return HttpResponse('注册成功')
                else:
                    uf = UserForm()
                    return render_to_response('register.html', {'uf': uf})
            else:
                uf = UserForm()
                return render_to_response('register.html', {'uf': uf})
        else:
            return render_to_response('register.html', {'uf': uf})
    # 不是POST请求，仍显示注册页面
    else:
        uf = UserForm()
        return render_to_response('register.html', {'uf': uf})


# 登录
def login(request):
    if request.method == 'POST':
        uf = LoginUserForm(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                # 比较成功跳转index已登录页面
                response = HttpResponseRedirect('/login/index')
                # 设置一个cookie有效期1小时
                response.set_cookie('username', username, 3600)
                return response
                # return render_to_response('success.html', {'username': username})
            else:
                # 比较失败跳转回到login
                return HttpResponseRedirect('/login/login')
        else:
            return HttpResponseRedirect('/login/login')
    else:
        uf = LoginUserForm()
        return render_to_response('login.html', {'uf': uf})


# 登录成功跳转至普通登录后页面
def index(request):
    username = request.COOKIES.get('username', '')
    return render_to_response('index.html', {'username': username})


# 修改密码
def changepasswd(request):
    if request.method == 'POST':
        uf = ChangePasswordForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            oldpassword = uf.cleaned_data['oldpassword']
            newpassword = uf.cleaned_data['newpassword']
            newpassword2 = uf.cleaned_data['newpassword2']
            user = User.objects.filter(username__exact=username, password__exact=oldpassword)
            if user:
                # 是原来的旧账号密码
                if newpassword == newpassword2:
                    # 两次输入新密码一致，修改之
                    user.update(password=newpassword)
                    return render_to_response('changepasswd.html', {'form': uf, 'changepwd_success': True})
                else:
                    # 两次密码不一致提醒重新输入
                    uf = ChangePasswordForm()
                    return render_to_response('changepasswd.html', {'form': uf, 'newpwd_is_wrong': True})
            else:
                # 旧账号或密码不对
                uf = ChangePasswordForm()
                return render_to_response('changepasswd.html', {'form': uf, 'oldpwd_is_wrong': True})
        else:
            return HttpResponseRedirect('/login/changepasswd')
    else:
        uf = ChangePasswordForm()
        return render_to_response('changepasswd.html', {'form': uf})


# 退出
def logout(request):
    response = HttpResponse('logout !!')
    response.delete_cookie('username')
    return response

