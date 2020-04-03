from . import views
from django.contrib import admin
from django.urls import path, include, URLPattern,re_path
from django.conf.urls import url
from .views import detailmesure, CustDelete,del_mesurements,update_measurement,del_worker,del_attendance

urlpatterns = [
    path("logout_page", views.logout_page, name='logout_page'),
    path("", views.index, name='index'),
    path("register", views.register, name='register'),
    path("login", views.login, name='login'),
    path('addcust', views.addcust,name='addcust'),
    path('calculate_form', views.calculate_form,name='calculate_form'),
    path('calculate_', views.calculate_,name='calculate_'),
    path('home', views.home,name='home'),
    path('view_customer', views.view_customer,name='view_customer'),
    path('view_payments_workers', views.view_payments_workers,name='view_payments_workers'),
    path('updateapyment_save/<int:id>', views.updateapyment_save, name='updateapyment_save'),


    path('View_worker', views.View_worker,name='View_worker'),
    path('userdet', views.userdet,name='userdet'),
    path('view_customer', views.view_customer,name='view_customer '),
    path('worker_save', views.worker_save,name='worker_save'),
    path("detailmesure/<int:pk>",detailmesure.as_view(),name='detailmesure'),
    path("update_worker/<int:pk>",views.update_worker,name='update_worker'),
    path('emppayment', views.emppayment,name='emppayment'),
    path('emppayform', views.emppayform,name='emppayform'),



    path('update_emp_save/<int:pk>/<un>/', views.update_emp_save,name='update_emp_save'),
    path('update_customer/<int:pk>/', views.update_customer,name='update_customer'),
    re_path(r'^update_customer/(<int:pk>[0-9]+)''$',views.view_customer,),
    path('update_customer_save/<int:pk>/', views.update_customer_save,name='update_customer_save'),
    path('updateemp/<int:pk>/', views.update_emp,name='updateemp'),

    path('userprofile', views.userprofile,name='userprofile'),
    path('payment2', views.payment2,name='payment2'),

    path('measure_list', views.measure_list,name='measure_list'),
    path('contactview', views.contactview,name='contactview'),
    path('customer_login_', views.customer_login_,name='customer_login_'),
    #path('user_profile_update/<int:pk>/<un>/', views.user_profile_update, name='user_profile_update'),
    path('complete/<int:pk>/<name>/', views.complete, name='complete'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('filterCustomer', views.filterCustomer, name='filterCustomer'),

    path("CustDelete/<int:pk>",CustDelete.as_view(),name='CustDelete'),
    path("complete_cust/<int:pk>/",views.complete_cust,name='complete_cust'),
    path("del_mesurements/<int:pk>",del_mesurements.as_view(),name='del_mesurements'),
    path("update_measurement/<int:pk>",update_measurement.as_view(),name='update_measurement'),
    path("del_mesurements/<int:pk>",del_mesurements.as_view(),name='del_mesurements'),
    path("del_worker/<int:pk>",del_worker.as_view(),name='del_worker'),
    path("del_attendance/<int:pk>",del_attendance.as_view(),name='del_attendance'),
    path("customer_review/<int:id>/",views.customer_review,name='customer_review'),
    path("customer_home_/<int:id>/", views.customer_home_, name='customer_home_'),
    path("GeneratePdf/<int:id>/", views.GeneratePdf, name='GeneratePdf'),








]
