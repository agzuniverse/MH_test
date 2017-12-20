from __future__ import unicode_literals
from django.shortcuts import render,redirect
from mhsite.forms import RegistrationForm,ApplicationForm,ExpenseForm,ReportForm,MessCutForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from mhsite.models import Application,Expense,MessCut, Profile
from django.views import View
from django.views.generic.edit import FormView
from django.db import IntegrityError
from django.utils.dateformat import format
from datetime import date, timedelta, datetime
import json, os


def home(request):
    args = {'name': url_lock('home')}
    return render(request, 'mhsite/index.html', args)

def gallery(request):
    args = {'name': url_lock('gallery')}
    return render(request, 'mhsite/gallery.html', args)

def mess(request):
    args = {'name': url_lock('mess')}
    return render(request, 'mhsite/messlogout.html', args)


def allocation(request):
    if request.method == 'POST':
        pwd = os.path.dirname(__file__)
        file = open(pwd + '/students.csv')
        data = file.readlines()
        file.close()
        students = []
        Profile.objects.filter().delete()
        for row in data:
            a = row.split(',')
            students.append(a)
        students.pop(0)
        for x in students:
            p = Profile(admission_number=x[0], name=x[1], email=x[2][:-1])
            p.save()

        return redirect('/')

    else:
        pwd = os.path.dirname(__file__)
        file = open(pwd + '/students.csv')
        data = file.readlines()
        file.close()
        students = []
        for row in data:
            a = row.split(',')
            students.append(a)
        students.pop(0)
        args = {'name': url_lock('alloc'), 'data':students}
        return render(request, 'mhsite/allocation.html', args)


def loginf(request):
    form = AuthenticationForm
    args = {'form': form, 'name': url_lock('log')}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
        else:
            args = {'form': form, 'error': True}
            return render(request, 'mhsite/login.html', args)


    return render(request, 'mhsite/login.html', args)


def logoutf(request):
    args = {'name': url_lock('log')}
    logout(request)
    return render(request, 'mhsite/logout.html')


def application(request):

    form = ApplicationForm()
    args = {'form': form, 'name': url_lock('application')}
    if request.method == 'POST':
        form = ApplicationForm(request.POST)


        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
            args = {'form': form, 'name': url_lock('application')}
            return render(request, 'mhsite/application.html', args)
    else:
        return render(request, 'mhsite/application.html', args)

#error for registration pending
def registration(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():
            if Profile.objects.filter(admission_number=form.cleaned_data.get('admission_number')).exists():
                form.save()
                return redirect('/')
            else:
                args = {'forms':form,'admission_error':True}
                return render(request, 'mhsite/registration.html', args)

        else:
            print ('error')
            args = {'forms':form}
            return render(request, 'mhsite/registration.html', args)

    else:
        form = RegistrationForm()
        args = {'forms': form, 'name': url_lock('reg')}
        return render(request, 'mhsite/registration.html', args)

def url_lock(page):
    index = [''  for x in range(9)]
    pages = ['home','gallery','student','mess','contact','log', 'alloc', 'application','reg']
    if page in pages:
        i = pages.index(page)
        index[i] = 'active'
        return index
    return index

#mess cut data generation function
def date_gen(lst,start_date,end_date,obj):
    delta = end_date - start_date
    for i in range(delta.days+1):
        lst['processing'].append(str(start_date + timedelta(days=i)))

    seen = set()
    seen_add = seen.add
    lst['processing'] = [x for x in lst['processing'] if not (x in seen or seen_add(x))]

    return lst

def mess_cut(request):
    if request.method=='POST':
        form=MessCutForm(request.POST)

        if form.is_valid():
            email= request.user.email
            start_date=form.cleaned_data['start_date']
            end_date=form.cleaned_data['end_date']
            try:

                obj = MessCut.objects.get(email=email)
                date_list = json.loads(obj.mess_cut_dates)

                date_list=(date_gen(date_list,start_date,end_date,obj))

                date_list = (json.dumps(date_list))

                obj.mess_cut_dates=date_list
                obj.applied_date =  datetime.now().timestamp()

                obj.save()
            except:

                date_list = (date_gen({'processing':[]},start_date,end_date,obj))
                date_list = json.dumps(date_list)
                obj = MessCut(email=email, mess_cut_dates=date_list, applied_date =  datetime.now().timestamp())
                obj.save()


            return redirect('/')
        else:
            args={'form':form}
            return render(request,'mhsite/mess_cut.html',args)
    else:
        form = MessCutForm()
        args={'form':form}
        return render(request,'mhsite/mess_cut.html',args)

def processing(request):
    rows = MessCut.objects.all()
    res = []
    for row in rows:
        profile = Profile.objects.get(email=row.email)
        name = profile.name
        mid = MessCut.objects.get(email=row.email).id
        room_number = profile.room_number #Complete after finishing profile

        data = json.loads(row.mess_cut_dates)
        timestamp = float(MessCut.objects.get(email=row.email).applied_date)
        applied_date = datetime.fromtimestamp(timestamp).strftime("%A, %d-%m-%Y")

        if len(data['processing']) > 0:
            res.append([name,room_number,applied_date,mid])

    args = {'data':res}
    return render(request,'mhsite/mess_cut_processing.html', args)

def approval(request,mess_id):
    mess = MessCut.objects.get(id=mess_id)
    mess_data = json.loads(mess.mess_cut_dates)
    dates = mess_data['processing']

    profile_data = Profile.objects.get(email=mess.email)
    profile = {'name':profile_data.name, 'room_number':profile_data.room_number, 'mobile':profile_data.phone}

    args = {'dates':dates, 'profile':profile}
    return render(request,'mhsite/verify.html', args)

#Final processing of mess data
def final(request, mess_id):
    mess = MessCut.objects.get(id=mess_id)
    mess_data = json.loads(mess.mess_cut_dates)
    dates = mess_data['processing']
    approved_dates = []
    rejected_dates = []

    for date in dates:
        try:

            choice = request.POST[date]
            if choice == '1':
                approved_dates.append(date)
            elif choice == '0':
                rejected_dates.append(date)
        except:
            pass

    mess_data['processing'] = [date for date in dates if (date not in approved_dates) and (date not in rejected_dates)]

    def date_data(x_date,dates):
        for date in dates:
            dateobject = datetime.strptime(date, '%Y-%m-%d')

            if str(dateobject.year) not in x_date:
                x_date[str(dateobject.year)] = {}

            if str(dateobject.month) not in x_date[str(dateobject.year)]:
                x_date[str(dateobject.year)][str(dateobject.month)] = []

            x_date[str(dateobject.year)][str(dateobject.month)].append(date)

        return x_date


    dic_approved_dates = (date_data(json.loads(mess.approved_dates),approved_dates))
    dic_rejected_dates = (date_data(json.loads(mess.rejected_dates),rejected_dates))


    mess.mess_cut_dates = json.dumps(mess_data)
    mess.approved_dates = json.dumps(dic_approved_dates)
    mess.rejected_dates = json.dumps(dic_rejected_dates)
    mess.process_date = datetime.now().timestamp()

    mess.save()

    #print ('approved', approved_dates, 'rejected', rejected_dates)
    return redirect('/')


def expense(request,year,month,day):
    date=(year+'-'+month+'-'+day)
    if request.method=='POST':
        try:
            expense=Expense.objects.get(date=date)
            form=ExpenseForm(request.POST,instance=expense)

        except Expense.DoesNotExist:
            form=ExpenseForm(request.POST)

        if form.is_valid():

            try:
                form.save()
                return redirect('/report'+'/'+date)

            except IntegrityError as e:

                return render(request, 'mhsite/expense_tracker.html', args)
        else:
            args={'form':form}
            return render(request, 'mhsite/expense_tracker.html', args)

#edit/create expense
    else:
        #edit expense for a month
        try:
            expense=Expense.objects.get(date=date)
            form=ExpenseForm(instance=expense)
            args = {'form': form}
            return render(request, 'mhsite/expense_tracker.html', args)
        #create expense for a month
        except Expense.DoesNotExist:
            form=ExpenseForm(initial={'date':date})
            args = {'form': form}
            return render(request, 'mhsite/expense_tracker.html',args)


class Report(FormView):
    template_name = 'mhsite/report.html'
    form_class = ReportForm

    def form_valid(self, form):
        date = form.cleaned_data.get('date')
        year = date.year
        month = format(date, 'm')
        day = '01'
        return redirect('report_details', year, month, day)

class ReportDetails(View):
    def get(self, request, year, month, day):
        date=(year+'-'+month+'-'+day)
        #display expense of a month if it exist
        try:
            expense=Expense.objects.get(date=date)
            return render(request, 'mhsite/report_details.html', {'data': expense,'link':date})

        except Expense.DoesNotExist:
            return redirect('expense',year,month,day)
