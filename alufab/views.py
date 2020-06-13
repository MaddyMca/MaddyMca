from io import StringIO, BytesIO
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.views import View

from .models import Employee,emp_pay, customer,measurement,worker,attendance,customer_login,material_inventory,Empattendance,Used_material,bill
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .forms import  Calculate_form
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from datetime import datetime
from  django.contrib.auth import logout
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.models import Sum
def index(request):

    return render(request,'index.html')
def login_(request):
    if request.method == "POST":
        username = request.POST['u']
        password = request.POST['p']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            cust1 = customer.objects.all().count()
            cust = customer.objects.filter().order_by('-id')[:5]
            emp1 = User.objects.all().count()
            mes2 = measurement.objects.values('is_complete','customer_name').order_by('customer_name').annotate(count=Count('is_complete'))
            work1 = worker.objects.all().count()
            mes = measurement.objects.values('customer_name').order_by('customer_name').annotate(count=Count('customer_name'))

            work2 = attendance.objects.filter(Date_of_attendance=datetime.now())

            work = worker.objects.filter().order_by('-id')[:5]



            context = {'desig': desig,'cust1': cust1, 'emp1': emp1, 'work1': work1, 'work2': work2,
                      'cust': cust, 'work': work,'mes':mes,'mes2':mes2}

            return render(request, 'home.html',context)
        else:
            messages.error(request, 'invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, "login.html")


def logout_page(request, next_page=None,
           template_name='registration/logged_out.html',
           current_app=None, extra_context=None):
    logout(request)
    return render(request,'login.html')

def home(request):
    id = request.user.id
    desig = Employee.objects.get(Emp_id=id)
    name = Employee.objects.get(Emp_id=id)
    cust1 = customer.objects.all().count()
    cust = customer.objects.filter().order_by('-id')[:5]
    mes2 = measurement.objects.values('is_complete','customer_name').order_by('customer_name').annotate(count=Count('is_complete'))
    work1 = worker.objects.all().count()
    mes = measurement.objects.values('customer_name').order_by('customer_name').annotate(count=Count('customer_name'))
    emp1 = User.objects.all().count()
    work2 = attendance.objects.filter(Date_of_attendance=datetime.now())
    work = worker.objects.filter().order_by('-id')[:5]
    context = {'cust1': cust1, 'emp1': emp1, 'work1': work1, 'work2': work2,'cust': cust, 'work': work,'mes':mes,'mes2':mes2,'desig':desig}
    return render(request, 'home.html',context)


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
            ad = request.POST['inputAddress']
            ad3 = request.POST['inputCity']
            de = request.POST['designation']
            em = request.POST['email']
            ppd = float(request.POST['ppd'])
            print(User.objects.filter(username=un))
            if User.objects.filter(username=un).exists():
                empid = request.user.id
                desig = Employee.objects.get(Emp_id=empid)
                messages.info(request, 'Username is not unique')
                return render(request, 'register.html',{'desig':desig})
            else:

                user = User.objects.create_superuser(username=un,password=pa,email=em)
                user.last_name=ln
                user.first_name=fn
                user.date_joined=datetime.now()
                user.email=em
                user.save()
                obj = User.objects.get(last_name=ln,first_name=fn,email=em)
                emp = Employee(Emp_id=obj, Address=ad,phono=pn,designation=de,city=ad3,Paymentperday=ppd)
                emp.save()
                empid = request.user.id
                desig = Employee.objects.get(Emp_id=empid)
                messages.info(request, 'User added successfully')
                return render(request,'register.html',{'desig':desig})
        else:
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
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
            empid = request.user.id
            emp = Employee.objects.get(id=empid)
            cust = customer(Emp_id=emp,name=fn,email=em, address=ad, phono=pn,city=ad3,cust_date=datetime.now())
            cust.save()

            na = customer.objects.get(name=fn)
            password = request.POST['pass']

            user = customer_login(cust_name=na, cust_password=password,cust_email=em)
            user.save()
            # subject = 'Login information for PrideAlu fab'
            # message = 'usename = ' + n + 'password = ' + password
            # email_from = settings.EMAIL_HOST_USER
            # mail = name.email
            # recipient_list = [mail]
            # send_mail(subject, message, email_from, recipient_list)
            desig = Employee.objects.get(Emp_id=empid)
            return render(request, 'addcust.html', {'desig': desig})

        else:
            print ('error')
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            return render(request, 'addcust.html',{'desig':desig})


def calculate_form(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        c_form = Calculate_form()
        empid = request.user.id
        desig = Employee.objects.get(Emp_id=empid)
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
                empid = request.user.id
                desig = Employee.objects.get(Emp_id=empid)
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
            empid = request.user.id
            emp = Employee.objects.get(id=empid)
            user = measurement(Emp_id=emp,customer_name=cust, left=left, right=right, top=top, bottom=bottom, hi=hi, bb=bb, g1=g1,g2=g2, track=track, type=TY, color=color,area=area,Payment_per_sqft=ppsf,total_payment=tp)
            user.save()
            total=measurement.objects.filter(customer_name=cust_id)
            total2=total.aggregate(Sum('total_payment'))
            ar=total2.get("total_payment__sum", "")
            cust = customer.objects.filter(id=cust_id).update(total_payment=ar)
            # user = cust(name=name,address=address,phno=phno)
            # user.save();
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            conyext = {'cust': cust, 'top': top, 'bottom': bottom, 'left': left, 'right': right, 'hi': hi, 'bb': bb,'g1': g1, 'g2': g2,'desig':desig,'area':area,'tp':tp,'ppsf':ppsf,}

            messages.info(request, 'Calculattion done')
            return render(request,'calcu2.html',conyext)
        else:
            c_form = Calculate_form()
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            return render(request, 'calcu.html', {'form': c_form,'desig':desig})


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
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            info = worker.objects.filter().order_by('-id')[:5]
            return render(request, 'workerregister.html', {'desig': desig,'info':info   })
        else:
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            info = worker.objects.filter().order_by('-id')[:5]
            return render(request, 'workerregister.html', {'desig': desig,'info':info})

def Inventory(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            mn = request.POST['mn']
            md = request.POST['md']
            p = float(request.POST['p'])
            quan = float(request.POST['quan'])
            tot = p*quan
            c_form = User.objects.all()
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            user = material_inventory(Emp_id=desig,material_name=mn,matrial_description=md,quantity=quan,price=p,total_amt=tot)
            user.save()
            return render(request, 'Inventory.html', {'form': c_form,'desig':desig})
        else:

            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            return render(request, 'Inventory.html', {'desig':desig})

def Worker_attend(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            wn = request.POST['Work']
            cust = request.POST['cust']
            wisf = float(request.POST['wisf'])
            rpsf = float(request.POST['rpsf'])
            date = request.POST['date']
            tot = wisf*rpsf
            c_form = User.objects.all()
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            work = worker.objects.get(id=wn)
            cuto = customer.objects.get(id=cust)
            user = attendance(Emp_id=desig,customer_name=cuto,worker_name=work,work_in_square_foot=wisf,total_payment=tot,payment_per_square_ft=rpsf,Date_of_attendance=date)
            user.save()
            form1 = customer.objects.all()
            form = worker.objects.all()
            return render(request, 'worker_attend.html', {'desig':desig,'form':form,'form1':form1})

        else:
            form1 = customer.objects.all()
            form = worker.objects.all()
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            return render(request, 'worker_attend.html', {'desig':desig,'form':form,'form1':form1})

def Emp_attend(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        obj = Employee.objects.all()
        total = Employee.objects.all().count()
        empid = request.user.id
        desig = Employee.objects.get(Emp_id=empid)
        return render(request,'EmpAttend.html',{'desig':desig,'obj':obj,'total':total})

def Emp_attend_save(request,id):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        empid = Employee.objects.get(id=id)
        #attend = Empattendance.objects.filter(Emp_id=id,date=datetime.today())
        attend = Empattendance.objects.filter(Emp_id=id,date=datetime.today())
        try:
            attend[0]
            messages.error(request,'Attendance already marked')
            obj = Employee.objects.all()
            total = Employee.objects.all().count()
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            return render(request,'EmpAttend.html',{'desig':desig,'obj':obj,'total':total})
        except IndexError:
            #user = Empattendance(Emp_id=empid,date=datetime.now(),Attend=True)
            user = Empattendance(Emp_id=empid,date=datetime.today(),Attend=True)
            user.save()
            obj = Employee.objects.all()
            total = Employee.objects.all().count()
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            return render(request,'EmpAttend.html',{'desig':desig,'obj':obj,'total':total})

def Emp_attend_save1(request,id):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        empid = Employee.objects.get(id=id)
        attend = Empattendance.objects.filter(Emp_id=id,date=datetime.today())
        print(attend)
        try:
            attend[0]
            messages.error(request,'Attendance already marked')
            obj = Employee.objects.all()
            total = Employee.objects.all().count()
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            return render(request,'EmpAttend.html',{'desig':desig,'obj':obj,'total':total})
        except IndexError:
            #user = Empattendance(Emp_id=empid,date=datetime.now(),Attend=False)
            user = Empattendance(Emp_id=empid,date=datetime.today(),Attend=False)
            user.save()
            obj = Employee.objects.all()
            total = Employee.objects.all().count()
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            return render(request,'EmpAttend.html',{'desig':desig,'obj':obj,'total':total})




def complete(request,pk,name):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        obj = measurement.objects.get(id=pk)
        print(obj.is_complete)
        na = customer.objects.get(name=name)
        name=na.id
        if obj.is_approved:
            if not obj.is_complete:
                obj.is_complete=True
                obj.completion_date=datetime.now()
                obj.save()
                mes = measurement.objects.filter(customer_name=na.id,is_complete=False)
                try:
                    mes[0]
                    na.is_complete=False
                    na.save()
                except IndexError :
                    na.is_complete=True
                    na.completion_date=datetime.today()
                    na.save()
                return render(request,'Addcost.html',{'obj':obj})
            else:
                obj.is_complete=False
                obj.completion_date=datetime.now()
                obj.save()
                na.is_complete=False
                na.save()

                resopnce = redirect('mesdetail',name)
                return resopnce
        else:
            messages.error(request,'Not approved by customer')
            resopnce = redirect('mesdetail',name)
            return resopnce

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
            usename =customer.objects.get(email=un)
            try:
                cust = customer_login.objects.get(cust_name=usename.id, cust_password=password)

            except customer_login.DoesNotExist:
                messages.error(request,'invalid username or password')
                return render(request, 'customer_login.html')

        except customer.DoesNotExist:
            messages.error(request,'invalid username or password')
            return render(request, 'customer_login.html')
        if cust is not None:
            c = get_object_or_404(customer,name=usename)
            m = measurement.objects.filter(customer_name=c)
            com = measurement.objects.filter(is_complete=True,customer_name=c.id).count()
            all = measurement.objects.filter(customer_name=c.id).count()
            per = int((com*100)/all)
            context = {'cust':c,'mes':m,'id':usename.id,'per':per}
            return render(request, 'customer_home.html',context)
        else:
            print('error')
            return render(request, 'customer_login.html')

    return render(request,'customer_login.html')

def customer_home_(request,id):
    usename = measurement.objects.get(id=id)
    c = get_object_or_404(customer, name=usename.customer_name)
    m = measurement.objects.filter(customer_name=c)
    com = measurement.objects.filter(is_complete=True).count()
    all = measurement.objects.all().count()
    per = (com*100)/all
    context = {'cust': c, 'mes': m,'id':usename.id,'per':per}
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
def genratebill(request,cust):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            c = customer.objects.get(id=cust)
            if(c.is_complete==True):
                empid = request.user.id
                desig = Employee.objects.get(Emp_id=empid)
                paid = float(request.POST['paid'])
                user = bill(Emp_id=desig,customer_name=c,completion_date=c.completion_date,total_payment=c.total_payment,paid_payment=paid,payment_date=datetime.today())
                user.save()
                if(c.total_payment == paid):
                    c.is_active=False
                resopnce = redirect('GeneratePdf', c.id)
                return resopnce
            else:
                messages.error(request,'Order is not complete')
                resopnce = redirect('DetailCust')
                return resopnce
        else:
            c = customer.objects.get(id=cust)
            b = bill.objects.filter(customer_name=c.id)
            print(b)
            try:
                b[0]
                resopnce = redirect('GeneratePdf', c.id)
                return resopnce
            except IndexError:
                if(c.is_complete==False):
                    messages.error(request,'Order is not complete')
                    resopnce = redirect('DetailCust')
                    return resopnce
                empid = request.user.id
                desig = Employee.objects.get(Emp_id=empid)
                return render(request,'pdf/bill.html',{'c':c,'desig':desig})




def GeneratePdf(request,id):
    cust=customer.objects.get(id=id)
    mes = measurement.objects.filter(customer_name=id)
    b = bill.objects.get(customer_name=id)
    pay = cust.total_payment-b.paid_payment
    data = {'obj':cust,'obj2':mes,'b':b,'pay':pay}

    return render(request, 'pdf/invoice.html', data)

def DetailEmps(request):
    obj = Employee.objects.all()
    empid = request.user.id
    desig = Employee.objects.get(Emp_id=empid)
    data={'obj':obj,'desig':desig}
    return render(request, 'alufab/employee_list.html', data)



def DetailCust(request):
    obj=customer.objects.all()
    empid = request.user.id
    desig = Employee.objects.get(Emp_id=empid)
    data={'obj':obj,'desig':desig}
    return render(request, 'alufab/customer_list.html', data)


def DetailInv(request):
    obj=material_inventory.objects.filter(is_user=False)
    empid = request.user.id
    desig = Employee.objects.get(Emp_id=empid)
    data={'obj':obj,'desig':desig}
    return render(request, 'alufab/material_inventory_list.html', data)

def DetailInv0(request):
    obj=material_inventory.objects.all()
    empid = request.user.id
    desig = Employee.objects.get(Emp_id=empid)
    data={'obj':obj,'desig':desig}
    return render(request, 'alufab/material_inventory_list.html', data)

def DetailInv1(request):
    obj=material_inventory.objects.filter(is_user=True)
    empid = request.user.id
    desig = Employee.objects.get(Emp_id=empid)
    data={'obj':obj,'desig':desig}
    return render(request, 'alufab/material_inventory_list.html', data)

def DetailWorkAttend(request):
    obj=attendance.objects.all()
    empid = request.user.id
    desig = Employee.objects.get(Emp_id=empid)
    data={'obj':obj,'desig':desig}
    return render(request, 'alufab/attendance_list.html', data)

def DetailWork(request):
    obj=worker.objects.all()
    empid = request.user.id
    desig = Employee.objects.get(Emp_id=empid)
    data={'obj':obj,'desig':desig}
    return render(request, 'alufab/worker_list.html', data)

class DetailEmp(DetailView):

    # specify the model for list view
    queryset = Employee.objects.all()

def DetailAttend(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        emp1=Empattendance.objects.filter(Attend=True).values('date').annotate(total=Count('date')).all()
        empid = request.user.id
        desig = Employee.objects.get(Emp_id=empid)
        emp = Employee.objects.all().count()
        data={'emp1':emp1,'desig':desig,'emp':emp}
        return render(request, 'alufab/Empattendance_list.html', data)
def AttendDate(request,date):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        emp1=Empattendance.objects.filter(date=date)
        empid = request.user.id
        desig = Employee.objects.get(Emp_id=empid)
        emp = Employee.objects.all().count()
        data={'emp1':emp1,'desig':desig,'emp':emp}
        return render(request, 'alufab/empattendance_list.html', data)

def AttendEmp(request):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        empid = request.user.id
        desig = Employee.objects.get(Emp_id=empid)
        emp = Employee.objects.all()
        data={'desig':desig,'emp':emp}
        return render(request, 'alufab/empattend_list1.html', data)

def AttendEmpdetail(request,id):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        emp=Empattendance.objects.filter(Emp_id=id)
        empid = request.user.id
        desig = Employee.objects.get(Emp_id=empid)
        data={'desig':desig,'emp':emp}
        return render(request, 'alufab/empattend_list2.html', data)

def mesdetail(request,id):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        emp=measurement.objects.filter(customer_name=id)
        empid = request.user.id
        desig = Employee.objects.get(Emp_id=empid)
        cust = customer.objects.get(id=id)
        com = measurement.objects.filter(is_complete=True,customer_name=id).count()
        all = measurement.objects.filter(customer_name=id).count()
        per = int((com*100)/all)
        data={'desig':desig,'emp':emp,'cust':cust,'per':per}
        return render(request, 'alufab/detailmesure.html', data)


def Emppay(request):
        if not request.user.is_authenticated:
            return render(request, 'notloggedin.html')
        elif request.user.is_authenticated:
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            emp = Employee.objects.all()
            data={'desig':desig,'emp':emp}
            return render(request, 'alufab/emppay_list.html', data)
def Emppaycalc(request,id):
        if not request.user.is_authenticated:
            return render(request, 'notloggedin.html')
        elif request.user.is_authenticated:
            current_month = datetime.now().month
            emp = Empattendance.objects.filter(date__month=current_month,Attend=True).count()
            ppd = Employee.objects.get(Emp_id=id)
            payment=ppd.Paymentperday*emp
            user = emp_pay(Emp_id=ppd,date=datetime.today(),attent=emp,Payment=payment)
            user.save()
            emp1=emp_pay.objects.filter(Emp_id=ppd.id)
            empid = request.user.id
            desig = Employee.objects.get(Emp_id=empid)
            data={'desig':desig,'emp':emp,'emp1':emp1}
            return render(request, 'alufab/emppay_list0.html', data)
from django.shortcuts import redirect
def Approved(request,id):
    obj = measurement.objects.get(id=id)
    print(obj.is_approved)
    obj.is_approved=True
    obj.save()
    resopnce = redirect('customer_home_',id)
    return resopnce


#update records

class CustomerUpdate(UpdateView):
    model = customer
    fields = ['name','email','address','city','phono']
    success_url = reverse_lazy('DetailCust')

class EmployeeUpdate(UpdateView):
    model = Employee
    fields = ['name','email','address','city','phono']
    success_url = reverse_lazy('DetailCust')

class CustomerUpdate(UpdateView):
    model = customer
    fields = ['name','email','address','city','phono']
    success_url = reverse_lazy('DetailCust')

class CustomerUpdate(UpdateView):
    model = customer
    fields = ['name','email','address','city','phono']
    success_url = reverse_lazy('DetailCust')

class CustomerUpdate(UpdateView):
    model = customer
    fields = ['name','email','address','city','phono']
    success_url = reverse_lazy('DetailCust')

class EmployeeUpdate(UpdateView):
    model = Employee
    fields = ['phono','Address','city','designation','Paymentperday','is_working' ]
    success_url = reverse_lazy('DetailEmps')

class WorkerUpdate(UpdateView):
    model = worker
    fields = ['worker_name','phone_number','Address','worker_type']
    success_url = reverse_lazy('DetailWork')

def UpdateInventory(request,id):
    empid = request.user.id
    desig = Employee.objects.get(Emp_id=empid)
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            used = float(request.POST['used'])
            cust = request.POST['cust']
            mat = material_inventory.objects.get(id=id)
            if(mat.quantity < used):
                messages.error(request,"You can't use more than you have")
                resopnce = redirect('DetailInv')
                return resopnce
            else:
                cust1 = customer.objects.get(id=cust)
                user = Used_material(Emp_id=desig,used=used,cust_name=cust1)
                user.save()

                used=mat.quantity - used
                if (used==0):
                    mat.is_user=True
                    mat.save()
                mat = material_inventory.objects.filter(id=id).update(quantity=used)
                resopnce = redirect('DetailInv')
                return resopnce
        else:
            mat = material_inventory.objects.get(id=id)
            cust=customer.objects.all()
            return render(request,'alufab/Updateinv.html',{'mat':mat,'cust':cust,'desig':desig})


def custpassword(request,email):
    otp = request.POST['otp']
    try:
        usename =customer.objects.get(email=email)
        try:
            cust = customer_login.objects.get(cust_email=email, otp=otp)

        except  customer_login.DoesNotExist:
            messages.error(request,'Invalid username or otp')

    except customer.DoesNotExist:
            messages.error(request,'Invalid username or otp')
    if cust is not None:
        return render(request, 'updatepasswordcust.html',{'email':email})
    else:
        return render(request, 'customer_login_.html')



from random import randint

def otpcust(request):
    email = request.POST['email']
    cust = customer_login.objects.get(cust_email=email)
    if cust.cust_email==email:
        otp = 0
        for i in range (0,4):
            a = randint(0, 10)
            otp = otp*10+a
        print(otp)
        customer_login.objects.filter(cust_email=email).update(otp=otp)

        return render(request,'Enterotp.html',{'email':email})
    else:
        messages.error(request, "Invalid email")
        responce = redirect('forgotpasscust')
        return responce;
def forgotpasscust(request):
    return render(request,'Custpass.html')

def changepass(request,email):
    pass1 = request.POST['pass']
    customer_login.objects.filter(cust_email=email).update(cust_password=pass1)
    messages.info(request,'Password updates successfully')
    return render(request,'customer_login.html')

def addcost(request,id):
    if not request.user.is_authenticated:
        return render(request, 'notloggedin.html')
    elif request.user.is_authenticated:
        r = request.POST['r']
        measurement.objects.filter(id=id).update(cost=r)
        obj=measurement.objects.get(id=id)
        cust = customer.objects.get(id=obj.customer_name.id)
        resopnce = redirect('mesdetail', cust.id)
        return resopnce
