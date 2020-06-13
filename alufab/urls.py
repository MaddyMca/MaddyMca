from . import views
from django.contrib import admin
from django.urls import path, include, URLPattern,re_path
from django.conf.urls import url
from .views import DetailEmp,CustomerUpdate,EmployeeUpdate,WorkerUpdate
from django.contrib.auth import views as auth_views
#from .views import detailmesure, CustDelete,del_mesurements,update_measurement,del_worker,del_attendance
urlpatterns = [

path("", views.index, name='index'),
path("login_", views.login_, name='login_'),
path("logout_page", views.logout_page, name='logout_page'),
path("home", views.home, name='home'),
path("register", views.register, name='register'),
path("addcust", views.addcust, name='addcust'),
path("calculate_form", views.calculate_form, name='calculate_form'),
path("calculate_", views.calculate_, name='calculate_'),
path("worker_save", views.worker_save, name='worker_save'),
path("Inventory", views.Inventory, name='Inventory'),
path("Worker_attend", views.Worker_attend, name='Worker_attend'),
path("Emp_attend", views.Emp_attend, name='Emp_attend'),
path("Emp_attend_save/<int:id>/", views.Emp_attend_save, name='Emp_attend_save'),
path("Emp_attend_save1/<int:id>/", views.Emp_attend_save1, name='Emp_attend_save1'),
path("otpcust", views.otpcust, name='otpcust'),
path("custpassword/<email>/", views.custpassword, name='custpassword'),
path("changepass/<email>/", views.changepass, name='changepass'),



path("forgotpasscust", views.forgotpasscust, name='forgotpasscust'),







path("filterCustomer", views.filterCustomer, name='filterCustomer'),
path("filterEmppay", views.filterEmppay, name='filterEmppay'),
path("filterWorkerpay", views.filterWorkerpay, name='filterWorkerpay'),
path("filtermes", views.filtermes, name='filtermes'),

path("customer_review/<int:id>/",views.customer_review,name='customer_review'),
path("customer_home_/<int:id>/", views.customer_home_, name='customer_home_'),
path("GeneratePdf/<int:id>/", views.GeneratePdf, name='GeneratePdf'),
path("genratebill/<int:cust>/", views.genratebill, name='genratebill'),

path("customer_login_", views.customer_login_, name='customer_login_'),
path("emppayment", views.emppayment, name='emppayment'),
path("emppayform", views.emppayform, name='emppayform'),

path('complete/<int:pk>/<name>/', views.complete, name='complete'),
path("DetailEmp/<pk>/", DetailEmp.as_view(), name='DetailEmp'),


path("DetailEmps", views.DetailEmps, name='DetailEmps'),
path("DetailCust", views.DetailCust, name='DetailCust'),
path('DetailInv', views.DetailInv,name='DetailInv'),
path('DetailInv0', views.DetailInv0,name='DetailInv0'),
path('DetailInv1', views.DetailInv1,name='DetailInv1'),

path("CustomerUpdate/<pk>/", CustomerUpdate.as_view(), name='CustomerUpdate'),
path("EmployeeUpdate/<pk>/", EmployeeUpdate.as_view(), name='EmployeeUpdate'),
path("WorkerUpdate/<pk>/", WorkerUpdate.as_view(), name='WorkerUpdate'),
path("UpdateInventory/<int:id>/", views.UpdateInventory, name='UpdateInventory'),



path('DetailWorkAttend', views.DetailWorkAttend,name='DetailWorkAttend'),
path('DetailWork', views.DetailWork,name='DetailWork'),
path('DetailAttend', views.DetailAttend,name='DetailAttend'),
path('AttendDate/<date>/', views.AttendDate,name='AttendDate'),
path('AttendEmp', views.AttendEmp,name='AttendEmp'),
path('AttendEmpdetail/<id>/', views.AttendEmpdetail,name='AttendEmpdetail'),
path('Emppay', views.Emppay,name='Emppay'),
path('Emppaycalc/<id>/', views.Emppaycalc,name='Emppaycalc'),
path('Approved/<id>/', views.Approved,name='Approved'),
path('mesdetail/<id>/', views.mesdetail,name='mesdetail'),
path('addcost/<id>/',views.addcost,name='addcost'),
path('password-reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
# url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
# url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
# url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, name='password_reset_confirm'),
# url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),


]
# urlpatterns = [
#     path("logout_page", views.logout_page, name='logout_page'),
#     path("", views.index, name='index'),
#     path("register", views.register, name='register'),
#     path("login", views.login, name='login'),
#     path('addcust', views.addcust,name='addcust'),
#     path('calculate_form', views.calculate_form,name='calculate_form'),
#     path('calculate_', views.calculate_,name='calculate_'),
#     path('home', views.home,name='home'),
#     path('view_customer', views.view_customer,name='view_customer'),
#     path('view_payments_workers', views.view_payments_workers,name='view_payments_workers'),
#     path('updateapyment_save/<int:id>', views.updateapyment_save, name='updateapyment_save'),
#
#
#     path('View_worker', views.View_worker,name='View_worker'),
#     path('detailUser', views.detailUser,name='detailUser'),
#     path('view_customer', views.view_customer,name='view_customer '),
#     path('worker_save', views.worker_save,name='worker_save'),
#     path("detailmesure/<int:pk>",detailmesure.as_view(),name='detailmesure'),
#     path("update_worker/<int:pk>",views.update_worker,name='update_worker'),
#     path('emppayment', views.emppayment,name='emppayment'),
#     path('emppayform', views.emppayform,name='emppayform'),
#
#
#
#     path('update_emp_save/<int:pk>/<un>/', views.update_emp_save,name='update_emp_save'),
#     path('update_customer/<int:pk>/', views.update_customer,name='update_customer'),
#     re_path(r'^update_customer/(<int:pk>[0-9]+)''$',views.view_customer,),
#     path('update_customer_save/<int:pk>/', views.update_customer_save,name='update_customer_save'),
#
#     path('userprofile', views.userprofile,name='userprofile'),
#     path('payment2', views.payment2,name='payment2'),
#
#     path('measure_list', views.measure_list,name='measure_list'),
#     path('contactview', views.contactview,name='contactview'),
#     path('customer_login_', views.customer_login_,name='customer_login_'),
#     #path('user_profile_update/<int:pk>/<un>/', views.user_profile_update, name='user_profile_update'),
#     path('complete/<int:pk>/<name>/', views.complete, name='complete'),
#     path('Detail_user/<int:pk>/', views.Detail_user, name='Detail_user'),
#     path('filterCustomer', views.filterCustomer, name='filterCustomer'),
#
#     path("CustDelete/<int:pk>",CustDelete.as_view(),name='CustDelete'),
#     path("complete_cust/<int:pk>/",views.complete_cust,name='complete_cust'),
#     path("del_mesurements/<int:pk>",del_mesurements.as_view(),name='del_mesurements'),
#     path("update_measurement/<int:pk>",update_measurement.as_view(),name='update_measurement'),
#     path("del_mesurements/<int:pk>",del_mesurements.as_view(),name='del_mesurements'),
#     path("del_worker/<int:pk>",del_worker.as_view(),name='del_worker'),
#     path("del_attendance/<int:pk>",del_attendance.as_view(),name='del_attendance'),
#     path("customer_review/<int:id>/",views.customer_review,name='customer_review'),
#     path("customer_home_/<int:id>/", views.customer_home_, name='customer_home_'),
#     path("GeneratePdf/<int:id>/", views.GeneratePdf, name='GeneratePdf'),
#
#
#
#
#
#
#
#
# ]
