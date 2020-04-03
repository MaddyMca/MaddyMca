from io import StringIO, BytesIO
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from .models import Employee, customer,measurement,worker,attendance,customer_login
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .forms import  RegisterForm, Calculate_form, Attend_form
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from datetime import datetime
from  django.contrib.auth import logout
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.models import Sum
# Create your views here.
def logout_page(request, next_page=None,
           template_name='registration/logged_out.html',
           current_app=None, extra_context=None):
    logout(request)
    return render(request,'login.html')

def home(request):
    username = request.user.username
    desig = Employee.objects.get(username=username)
    name = Employee.objects.get(username=username)
    cust1 = customer.objects.all().count()
    cust = customer.objects.filter().order_by('-id')[:5]
    mes2 = measurement.objects.values('is_complete','customer_name').order_by('customer_name').annotate(count=Count('is_complete'))
    work1 = worker.objects.all().count()
    mes = measurement.objects.values('customer_name').order_by('customer_name').annotate(count=Count('customer_name'))
    emp1 = Employee.objects.all().count()
    work2 = attendance.objects.filter(Date_of_attendance=datetime.now())

    work = worker.objects.filter().order_by('-id')[:5]
    emp = Employee.objects.filter().order_by('-id')[:5]


    context = {'desig': name, 'cust1': cust1, 'emp1': emp1, 'work1': work1, 'work2': work2,
              'cust': cust, 'work': work, 'emp': emp,'mes':mes,'mes2':mes2}


    #context = {'desig':desig}
    return render(request, 'home.html',context)
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        username = request.POST['u']
        password = request.POST['p']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            username = request.user.username
            desig = Employee.objects.get(username=username)
            name = Employee.objects.get(username=username)
            cust1 = customer.objects.all().count()
            cust = customer.objects.filter().order_by('-id')[:5]
            mes2 = measurement.objects.values('is_complete','customer_name').order_by('customer_name').annotate(count=Count('is_complete'))
            work1 = worker.objects.all().count()
            mes = measurement.objects.values('customer_name').order_by('customer_name').annotate(count=Count('customer_name'))
            emp1 = Employee.objects.all().count()
            work2 = attendance.objects.filter(Date_of_attendance=datetime.now())

            work = worker.objects.filter().order_by('-id')[:5]
            emp = Employee.objects.filter().order_by('-id')[:5]


            context = {'desig': name,'cust1': cust1, 'emp1': emp1, 'work1': work1, 'work2': work2,
                      'cust': cust, 'work': work, 'emp': emp,'mes':mes,'mes2':mes2}
            #context = {'desig':name}
            return render(request, 'home.html',context)
        else:
            messages.error(request, 'invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, "login.html")

def register(request):
    if not request.user.is_authenticated:
        return render(request,'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            un = request.POST['un']
            fn = request.POST['fn']
            ln = request.POST['ln']
            pn = request.POST['pn']
            pa = request.POST['pass']
            ad1 = request.POST['inputAddress']
            ad2 = request.POST['inputAddress2']
            ad3 = request.POST['inputCity']
            de = request.POST['designation']
            em = request.POST['email']
            ad = ad1 + ' Landmark : ' + ad2
            if User.objects.filter(username=un).exists():
                username = request.user.username
                desig = Employee.objects.get(username=username)
                messages.info(request, 'Username is not unique')
                return render(request, 'register.html',{'desig':desig})
            else:
                emp = Employee(username=un,first_name=fn,last_name=ln,password=pa,email=em,address=ad,phono=pn,designation=de,city=ad3)
                emp.save()
                user = User.objects.create_superuser(username=un,password=pa,email=em)
                user.last_name=ln
                user.first_name=fn
                user.save()
                username = request.user.username
                desig = Employee.objects.get(username=username)
                messages.info(request, 'User added successfully')
                return render(request,'register.html',{'desig':desig})
        else:
            username = request.user.username
            desig = Employee.objects.get(username=username)
            return render(request, 'register.html',{'desig':desig})


def addcust(request):
    if not request.user.is_authenticated:
        return render(request,'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            fn = request.POST['fn']
            pn = request.POST['pn']
            ad1 = request.POST['inputAddress']
            ad2 = request.POST['inputAddress2']
            ad3 = request.POST['inputCity']
            em = request.POST['email']
            ad = ad1 + ' Landmark : ' + ad2

            cust = customer(name=fn,email=em, address=ad, phono=pn,city=ad3,cust_date=datetime.now())
            cust.save()

            na = customer.objects.get(name=fn)
            password = request.POST['Password']

            user = customer_login(cust_name=na, cust_password=password)
            user.save()
            # subject = 'Login information for PrideAlu fab'
            # message = 'usename = ' + n + 'password = ' + password
            # email_from = settings.EMAIL_HOST_USER
            # mail = name.email
            # recipient_list = [mail]
            # send_mail(subject, message, email_from, recipient_list)
            username = request.user.username
            desig = Employee.objects.get(username=username)
            return render(request, 'addcust.html', {'desig': desig})

        else:
            print ('error')
            username = request.user.username
            desig = Employee.objects.get(username=username)
            return render(request, 'addcust.html',{'desig':desig})
def calculate_form(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        c_form = Calculate_form()
        username = request.user.username
        desig = Employee.objects.get(username=username)
        return render(request, 'calcu.html', {'form': c_form,'desig':desig})


def calculate_(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            top = float(request.POST['top'])
            bottom = float(request.POST['bottom'])
            left = float(request.POST['left'])
            right = float(request.POST['right'])
            TY = request.POST['type']
            track = request.POST['track']
            color = request.POST['color']
            cust_id = request.POST['customer_name']
            ppsf = float(request.POST['Payment_per_sqft'])
            t = top * 8
            b = bottom * 8
            r = right * 8
            lt = left * 8
            hi = 0
            bb = 0
            g1 = 0
            g2 = 0

            l = []
            l.append(lt)
            l.append(r)
            m = min(l)
            if TY == '18X35' and track == '2T':
                hi = m - 11
                bb = (b - 69) / 2
                g1 = hi - 20
                g2 = bb + 4
            elif TY == '18X35' and track == '3T':
                hi = m - 11
                bb = (b - 51) / 3
                g1 = hi - 20
                g2 = bb + 4
            elif TY == '18X50' and track == '2T':
                hi = m - 11
                bb = (b - 51) / 2
                g1 = hi + 28
                g2 = bb + 5
            elif TY == '18X50' and track == '3T':
                hi = m - 11
                bb = (b - 82) / 3
                g1 = hi + 28
                g2 = bb + 5
            else:
                username = request.user.username
                desig = Employee.objects.get(username=username)
                messages.error(request, 'Invalid input')
                return render(request, "calcu.html",{'desig':desig})

            hi = hi / 8
            bb = bb / 8
            g1 = g1 / 8
            g2 = g2 / 8
            hi = round(hi,2)
            bb= round(bb,2)
            g1 = round(g1,2)
            g2 = round(g2,2)
            area = top * left
            tp=ppsf*area
            print(tp)
            cust = customer.objects.get(id=cust_id)
            user = measurement(customer_name=cust, left=left, right=right, top=top, bottom=bottom, hi=hi, bb=bb, g1=g1,
                               g2=g2, track=track, type=TY, color=color,area=area,Payment_per_sqft=ppsf,total_payment=tp)
            user.save()
            total=measurement.objects.filter(customer_name=cust_id)
            total2=total.aggregate(Sum('total_payment'))
            print(total2)
            ar=total2.get("total_payment__sum", "")
            print("*****************************************************",ar)
            cust = customer.objects.filter(id=cust_id).update(total_payment=ar)
            # user = cust(name=name,address=address,phno=phno)
            # user.save();
            username = request.user.username
            desig = Employee.objects.get(username=username)
            conyext = {'cust': cust, 'top': top, 'bottom': bottom, 'left': left, 'right': right, 'hi': hi, 'bb': bb,
                       'g1': g1, 'g2': g2,'desig':desig,'area':area,'tp':tp,'ppsf':ppsf,}

            messages.info(request, 'Calculattion done')
            return render(request,'calcu2.html',conyext)
        else:
            cust = customer.objects.all()
            username = request.user.username
            desig = Employee.objects.get(username=username)





def worker_save(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            wn = request.POST['wn']
            pn = request.POST['pn']
            ad = request.POST['ad']
            ty = request.POST['type']
            work = worker(worker_name=wn,phone_number=pn,Address=ad,worker_type=ty)
            work.save()
            messages.info(request,'Worker added')
            username = request.user.username
            desig = Employee.objects.get(username=username)
            info = worker.objects.filter().order_by('-id')[:5]
            return render(request, 'workerregister.html', {'desig': desig,'info':info   })
        else:
            username = request.user.username
            desig = Employee.objects.get(username=username)
            info = worker.objects.filter().order_by('-id')[:5]
            return render(request, 'workerregister.html', {'desig': desig,'info':info})

def view_customer(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        form = customer.objects.all()
        username = request.user.username
        desig = Employee.objects.get(username=username)
        context={'form':form,'desig':desig}
        return render(request,'alufab/customer_list.html',context)

def view_payments_workers(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        form = attendance.objects.all()
        username = request.user.username
        desig = Employee.objects.get(username=username)
        context={'form':form,'desig':desig}
        return render(request,'alufab/attendance_list.html',context)

def View_worker(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        form = worker.objects.all()
        username = request.user.username
        desig = Employee.objects.get(username=username)
        context={'form':form,'desig':desig}
        return render(request,'alufab/worker_list.html',context)


def userdet(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        form = Employee.objects.all()
        username = request.user.username
        desig = Employee.objects.get(username=username)
        context={'form':form,'desig':desig}
        return render(request,'alufab/employee_list.html',context)

def update_customer(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:

        cust = get_object_or_404(customer, id= pk)
        username = request.user.username
        desig = Employee.objects.get(username=username)
        return render(request,'updatecust.html',{'i':cust,'desig':desig})

def update_customer_save(request, pk):
    if not request.user.is_authenticated:
        return render(request,'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            fn = request.POST['fn']
            pn = request.POST['pn']
            ad = request.POST['inputAddress']
            ad3 = request.POST['inputCity']
            em = request.POST['email']

            customer.objects.filter(id=pk).update(name=fn,email=em, address=ad, phono=pn,city=ad3 )
            username = request.user.username
            desig = Employee.objects.get(username=username)
            messages.info(request, 'Update successful')
            response = redirect('view_customer')
            return response

        else:
            print ('error')
            return render(request, 'addcust.html')

def update_emp(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:

        cust = get_object_or_404(Employee, id= pk)
        username = request.user.username
        desig = Employee.objects.get(username=username)
        return render(request,'updateemp.html',{'i':cust,'desig':desig})

def update_worker(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:

        cust = get_object_or_404(worker, id= pk)
        username = request.user.username
        desig = Employee.objects.get(username=username)
        return render(request,'update_worker.html',{'i':cust,'desig':desig})


from django.shortcuts import redirect
def update_worker_save(request, pk):
    if not request.user.is_authenticated:
        return render(request,'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            wn = request.POST['wn']
            pn = request.POST['pn']
            ad = request.POST['ad']
            ty = request.POST['type']
            worker.objects.filter(id=pk).update(worker_name=wn, phone_number=pn, Address=ad, worker_type=ty)
            username = request.user.username
            desig = Employee.objects.get(username=username)
            response = redirect('View_worker')
            return response
            #return render(request , "{% url 'View_worker' %}",{'desig':desig})

        else:
            print ('error')
            return render(request, 'addcust.html')

def update_emp_save(request,pk,un):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            fn = request.POST['fn']
            ln = request.POST['ln']
            pn = request.POST['pn']
            ad1 = request.POST['inputAddress']
            ad3 = request.POST['inputCity']
            de = request.POST['designation']
            em = request.POST['email']

            Employee.objects.filter(id=pk).update(first_name=fn, last_name=ln, email=em, address=ad1, phono=pn,
                           designation=de, city=ad3)

            User.objects.filter(username=un).update(email=em,last_name = ln,first_name = fn)
            response = redirect('userdet')
            return response



class detailmesure(DetailView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'notloggedin.html')
        elif request.user.is_authenticated:
            try:
                obj = measurement.objects.filter(customer_name=kwargs['pk'])
            except measurement.DoesNotExist:
                raise Http404("No records")
            username = request.user.username
            desig = Employee.objects.get(username=username)
            cust = customer.objects.get(id=kwargs['pk'])
            context = {'obj': obj,'desig':desig,'cust':cust}
            return render(request, 'mesuredetail.html', context)



from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def contactview(request):
    # name = request.GET['fn']
    # phoneno = request.GET['pn']
    # req = request.GET['rq']
    # email= request.GET['email']
    # comment=request.GET['address']
    #
    # comment = name + " with the email, " + email + "Phone number" + phoneno + ", sent the following message:\n\n"+req
    #
    # #send_mail("For Quote", comment, 'mandarphadke1434@gmail.com', [email])
    # send_mail("Quote",comment, 'mandarphadke1434@gmail.com',["mandarphadke1434@gmail.com"],fail_silently=False)
    # return render(request, 'index.html')
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['mandarphadke1434@gmail.com', ]
    send_mail(subject, message, email_from, recipient_list)
    return render(request, 'index.html')

def userprofile(request):
    username = request.user.username
    desig = Employee.objects.get(username=username)
    return render(request,'userprofile.html',{'desig':desig})



# def user_profile_update(request,pk,un):
#     if not request.user.is_authenticated:
#         return render(request, 'notloggedin.html')
#     elif request.user.is_authenticated:
#         if request.method == 'POST':
#             fn = request.POST['fn']
#             ln = request.POST['ln']
#             pn = request.POST['pn']
#             ad1 = request.POST['inputAddress']
#             ad3 = request.POST['inputCity']
#             de = request.POST['designation']
#             em = request.POST['email']
#
#             Employee.objects.filter(id=pk).update(first_name=fn, last_name=ln, email=em, address=ad1, phono=pn,
#                                                   designation=de, city=ad3)
#
#             User.objects.filter(username=un).update(email=em, last_name=ln, first_name=fn)
#             response = redirect('userprofile')
#             return response
#     response = redirect('userprofile')
#     return response

def complete(request,pk,name):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        obj = measurement.objects.get(id=pk)
        print(obj.is_complete)
        na = customer.objects.get(name=name)
        name=na.id
        if not obj.is_complete:
            obj.is_complete=True
            obj.completion_date=datetime.now()
            obj.save()
        else:
            obj.is_complete=False
            obj.completion_date=datetime.now()
            obj.save()
        resopnce = redirect('detailmesure',name)
        return resopnce
def complete_cust(request,pk):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        obj = customer.objects.get(id=pk)
        if not obj.is_complete:
            obj.is_complete=True
            obj.completion_date=datetime.now()
            obj.save()
        else:
            obj.is_complete=False
            obj.save()

        resopnce = redirect('view_customer')
        return resopnce


def delete_user(request,pk):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        obj = get_object_or_404(User,id=pk)
        obj.delete()
        obj = get_object_or_404(Employee, id=pk)
        obj.delete()
        response = redirect('userdet')
        return response

class CustDelete(DeleteView):
        model = customer
        success_url = reverse_lazy('view_customer')


def measure_list(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        form = measurement.objects.all()
        username = request.user.username
        desig = Employee.objects.get(username=username)
        context={'form':form,'desig':desig}
        return render(request,'alufab/measurement_list.html',context)



class del_mesurements(DeleteView):
    model = measurement
    success_url = reverse_lazy('view_customer')
class del_worker(DeleteView):
    model = worker
    success_url = reverse_lazy('View_worker')
class del_attendance(DeleteView):
    model = attendance
    success_url = reverse_lazy('view_payments_workers')
class update_measurement(UpdateView):
    model = measurement
    fields = ['top','bottom','left','right','type','track','color']
    success_url = reverse_lazy('measure_list')
def payment2(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            site = request.POST['site']
            wiqf = float(request.POST['wiqf'])
            rpsf = float(request.POST['rpsf'])
            d = request.POST['d']
            total = wiqf*rpsf
            cust = customer.objects.get(id=site)
            work_name = worker.objects.get(id=name)
            user = attendance(worker_name=work_name,customer_name=cust,work_in_square_foot=wiqf,payment_per_square_ft=rpsf,total_payment=total,Date_of_attendance=d)
            user.save()
            response = redirect('attend_list')
            return response

        else:
            cust = customer.objects.all()
            work = worker.objects.all()
            context = {'cust':cust,'work':work}
            return render(request,'payment.html',context)


def updateapyment_save(request,id):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            form=attendance.objects.filter(id=id).get()
            name = request.POST['name']
            site = request.POST['site']
            wiqf = float(request.POST['wiqf'])
            rpsf = float(request.POST['rpsf'])
            d = request.POST['d']
            total = wiqf*rpsf
            cust = customer.objects.get(id=site)
            work_name = worker.objects.get(id=name)
            user = attendance.objects.filter(id=id).update(worker_name=work_name,customer_name=cust,work_in_square_foot=wiqf,payment_per_square_ft=rpsf,total_payment=total,Date_of_attendance=d)
            user.save()
            response = redirect('attend_list')
            return response
        else:
            cust = customer.objects.all()
            work = worker.objects.all()
            form=attendance.objects.filter(id=id).get()
            context = {'cust':cust,'work':work,'form':form}

            return render(request,'workpaymentupdate.html',context)
def filterCustomer(request):
        frm = request.GET['from']
        to = request.GET['to']
        if(frm=='' or to==''):
            frm = datetime.now()
            to=datetime.now()
        form=customer.objects.filter(cust_date__range=[frm,to])
        return render(request,'alufab/customer_list.html',{'form':form})

def filterEmppay(request):
    frm = request.GET['from']
    to = request.GET['to']
    if (frm == '' or to == ''):
        frm = datetime.now()
        to = datetime.now()
    form = employeePayment.objects.filter(day_of_payment__range=[frm, to])
    return render(request, 'alufab/employeepayment_list.html', {'form': form})

def filterWorkerpay(request):
    frm = request.GET['from']
    to = request.GET['to']
    if (frm == '' or to == ''):
        frm = datetime.now()
        to = datetime.now()
    form = attendance.objects.filter(Date_of_attendance__range=[frm, to])
    return render(request, 'alufab/attendance_list.html', {'form': form})

def filtermes(request):
    frm = request.GET['from']
    to = request.GET['to']
    if (frm == '' or to == ''):
        frm = datetime.now()
        to = datetime.now()
    form = measurement.objects.filter(mesure_date_time__range=[frm, to])
    return render(request, 'mesuredetail.html', {'form': form})



def customer_login_(request):
    if request.method == 'POST':
        un = request.POST['username']
        password = request.POST['pass']

        try:
            usename =customer.objects.get(name=un)
            try:
                cust = customer_login.objects.get(cust_name=usename.id, cust_password=password)

            except customer_login.DoesNotExist:
                raise  Http404("Invalid username or password")
        except customer.DoesNotExist:
            raise Http404("invalid username or password")
        if cust is not None:
            c = get_object_or_404(customer,name=usename)
            m = measurement.objects.filter(customer_name=c)
            context = {'cust':c,'mes':m,'id':usename.id}
            return render(request, 'customer_home.html',context)
        else:
            print('error')
            return render(request, 'customer_login.html')

    return render(request,'customer_login.html')

def customer_home_(request,id):
    usename = customer.objects.get(id=id)
    c = get_object_or_404(customer, name=usename)
    m = measurement.objects.filter(customer_name=c)
    context = {'cust': c, 'mes': m,'id':usename.id}
    return render(request, 'customer_home.html', context)

def customer_review(request, id ):
    cmt = request.GET['cmt']
    rate = request.GET['rating']
    cust = customer_login.objects.get(cust_name=id)
    customer_login.objects.filter(cust_name=cust).update(cust_review=cmt,star=rate)
    responce=redirect('customer_home_', id=id)
    return responce;
def emppayment(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            dp = float(request.POST['dp'])
            rpsf = float(request.POST['ppd'])
            d=request.POST['d']
            tp = rpsf*dp
            empid=Employee.objects.get(id=name)
            user = employeePayment(emp_id=empid,payment_per_day=rpsf,days_present=dp,payment=tp,day_of_payment=d)
            user.save()
            responce = redirect('emppayform')
            return responce;
def emppayform(request):
            emp=Employee.objects.all()
            context={'emp':emp}
            return render(request,'empattend.html',context)

def GeneratePdf(request,id):
    cust=customer.objects.get(id=id)
    mes = measurement.objects.filter(customer_name=id)
    data = {'obj':cust,'obj2':mes}
    return render(request, 'pdf/invoice.html', data)

