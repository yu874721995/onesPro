"""twostr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import re_path
from oneGo import views as indexviews
from oneGo.api.user_CreateTestCase import user_testCase as SaveCase
from oneGo.api.updateUser import update_Users as user
from oneGo.api.userList import user_list as users
from oneGo.api.req_Debug import req_debug as req
from oneGo.api.login import Login as login
from oneGo.api.CaseChoice import caseChoice as case
from oneGo.api import wechat as wechatview
from xcx.api.loginAndRegite import login_and_reg as xcx_login
from oneGo.api import uploadimg
from oneGo.api import tapd

urlpatterns = [
    # re_path('',oneviews.login),
    re_path(r'^$', indexviews.login),
    re_path('session_test', users().session_test),
    re_path('index', indexviews.index),
    re_path('login', indexviews.login),
    re_path('diary_index', indexviews.diary_index),
    re_path('diary_login', indexviews.diary_login),
    re_path('Loginup', login().Loginup),
    re_path('goRegister', indexviews.goRegister),
    re_path('register', indexviews.register),
    re_path('reqJson', req().reqJson),
    re_path('username', users().getuser),
    re_path('UserHistory', users().userHistory),
    re_path(r'^accounts/login/$', indexviews.login),
    re_path('SaveTestCase', SaveCase().saveTestCase),
    re_path('deleteHistory', indexviews.deleteHistory),
    re_path('userList', users().userList),
    re_path('updateUserStatus', user().updateUserStatus),
    re_path('addUser', users().add_User),
    re_path('user_delete', user().user_delete),
    re_path('userDelList', users().userDelList),
    re_path('recoverCustomer', users().recoverCustomer),
    re_path('addChoice', case().addChoice),
    re_path('queryForProduct', case().queryForProduct),
    re_path('queryForOur', case().queryForOur),
    re_path('caseList', case().caseList),
    re_path('shenheList', case().shenheList),
    re_path('zhenrenList', case().zhenrenlist),
    re_path('removezhenren', case().removezhenren),
    re_path('zhaohu',case().zhaohu),
    re_path('shijishenhe',case().shijishenhe),
    re_path('batchExecution', case().batchExecution),
    # re_path('sendMsg', wechatview.sendMsg),
    re_path('getUserInfo', xcx_login().getUserInfo),
    re_path('uploadImage', uploadimg.uploadImage),
    re_path('update', indexviews.update),
    re_path('commit', indexviews.commit),
    re_path('hlshengji', indexviews.hlshengji),
    re_path('user_id_phone', indexviews.user_id_phone),
    re_path('charge_vip', indexviews.charge_vip),
    re_path('flower', indexviews.flower_update),
    re_path('gaidengji', indexviews.gaidengji),
    re_path('sign', indexviews.sign),
    re_path('zhuboshenhe', indexviews.zhuboshenhe),
    re_path('guizu', indexviews.guizu),
    re_path('tapd',tapd.main),
    re_path('look',indexviews.look),
    re_path('checkApp',indexviews.checkApp),
    re_path('information_gifts',indexviews.information_gifts),
    re_path('Project',tapd.get_project),
    re_path('auto_registration',indexviews.auto_registration),
    re_path('income_calculator',indexviews.income_calculator),
    re_path('auth_msg',indexviews.auth_msg),
    re_path('Getagent',indexviews.get_agent),
    re_path('shenhe',indexviews.returnshenhe),
    re_path('zhenren',indexviews.zhenren),
    # re_path('get_houtai_cookie',indexviews.get_houtai_cookie),




]
