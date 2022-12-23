from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login as enter
from django.contrib.auth import logout as exit
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from medapp.models import Patient, Diagnosis, Reception, Doctor, PurposeOfVisit

DIAGNOSIS_TMP = "home/diagnosis.html"
DETAIL_DIAGNOSIS = "home/detail_diagnosis.html"


SEARCH_PACIENTS = "home/pacients.html"
ADD_PACIENT = "home/add_pacient.html"
EDIT_PACIENT = "home/edit_pacient.html"
DETAIL_PACIENT = "home/detail_pacient.html"

RECEPTIONS_TMP = "home/receptions.html"
ADD_RECEPTION = "home/add_receptions.html"
EDIT_RECEPTION= "home/edit_reception.html"
DETAIL_RECEPTION = "home/detail_reception.html"


LOGIN_TMP = "home/login.html"
HOME_TMP = "home/index.html"

def phone_formatter(data):
    return data.replace("(","").replace(")","").replace(" ","").replace("-","").replace("+7","8")


@login_required(login_url='/login')
def diagnosis(request):
    per_page = 15
    current_page = 1
    if request.GET.get("per_page"):
        per_page = request.GET.get("per_page")
    if request.GET.get("current_page"):
        current_page = request.GET.get("current_page")
    objects = Diagnosis.objects.all()
    if request.GET.get("q"):
        objects = objects.filter(name__icontains=request.GET.get("q"))

    paginator = Paginator(objects, per_page=per_page)
    page = paginator.page(current_page)
    return render(request,DIAGNOSIS_TMP,{
        "q":request.GET.get("q"),
        "page":{
            "current_page": current_page,
            "all_items": paginator.count,
            "all_pages": paginator.num_pages,
            "items": page.object_list
        }})

@login_required(login_url='/login')
def detail_diagnosis(request,pk):
    return render(request,DETAIL_DIAGNOSIS,{"diagnosis":Diagnosis.objects.get(pk=pk)})

@login_required(login_url='/login')
def add_pacient(request):
    context = {}
    if request.method == "POST":

        surname = request.POST.get("surname")
        name = request.POST.get("name")
        patronymic = request.POST.get("patronymic")
        date_of_birth = request.POST.get("date_of_birth")
        passport_ID = request.POST.get("passport_ID")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")

        context['surname'] = surname
        context['name'] = name
        context['patronymic'] = patronymic
        context['date_of_birth'] = date_of_birth
        context['passport_ID'] = passport_ID
        context['address'] = address
        context['phone_number'] = phone_number

        p = Patient(
            surname=surname,
            name=name,
            patronymic=patronymic,
            date_of_birth=date_of_birth,
            passport_ID=passport_ID.replace(" ",""),
            address=address,
            phone_number=phone_formatter(phone_number)
        )
        try:
            p.save()
            return redirect(reverse("home:detail_pacient",kwargs={"pk":p.pk}))
        except BaseException as e:
            messages.error(request, str(e))

    return render(request,ADD_PACIENT,context)

@login_required(login_url='/login')
def edit_pacient(request,pk):
    context = {}
    obj = Patient.objects.get(pk=pk)
    if request.method == "POST":

        surname = request.POST.get("surname")
        name = request.POST.get("name")
        patronymic = request.POST.get("patronymic")
        date_of_birth = datetime.strptime(request.POST.get("date_of_birth"), '%Y-%m-%d')
        passport_ID = request.POST.get("passport_ID").replace(" ","")
        address = request.POST.get("address")
        phone_number = phone_formatter(request.POST.get("phone_number"))

        try:
            obj.surname = surname
            obj.name = name
            obj.patronymic = patronymic
            obj.date_of_birth = date_of_birth
            obj.passport_ID = passport_ID
            obj.address = address
            obj.phone_number = phone_number
            obj.save()

            messages.success(request, 'Данные сохранены')
        except BaseException as e:
            messages.error(request, str(e))
    context["obj"] = obj
    return render(request, EDIT_PACIENT, context)

@login_required(login_url='/login')
def detail_pacient(request,pk):
    return render(request,DETAIL_PACIENT,{"pacient":Patient.objects.get(pk=pk)})

@login_required(login_url='/login')
def pacients(request):
    per_page = 15
    current_page = 1
    if request.GET.get("per_page"):
        per_page = request.GET.get("per_page")
    if request.GET.get("current_page"):
        current_page = request.GET.get("current_page")
    patients = Patient.objects.all()
    if request.GET.get("q"):
        patients = patients.filter(
            Q(pk__icontains=request.GET.get("q")) |
            Q(surname__icontains=request.GET.get("q"))|
            Q(name__icontains=request.GET.get("q"))|
            Q(patronymic__icontains=request.GET.get("q"))|
            Q(passport_ID__icontains=request.GET.get("q")) |
            Q(phone_number__icontains=request.GET.get("q"))
        )
    paginator = Paginator(patients,per_page=per_page)
    page = paginator.page(current_page)
    return render(request, SEARCH_PACIENTS,{
        #"tmp_path":request.path,
        "q": request.GET.get("q"),
        "page": {
            "current_page": current_page,
            "all_items": paginator.count,
            "all_pages": paginator.num_pages,
            "items": page.object_list
        }})

@login_required(login_url='/login')
def receptions(request):
    per_page = 15
    current_page = 1
    if request.GET.get("per_page"):
        per_page = request.GET.get("per_page")
    if request.GET.get("current_page"):
        current_page = request.GET.get("current_page")
    objects = Reception.objects.all()
    if request.GET.get("q"):
        objects = objects.filter(
            Q(patient__passport_ID__icontains=request.GET.get("q"))|
            Q(patient__surname__icontains=request.GET.get("q"))|
            Q(patient__name__icontains=request.GET.get("q"))|
            Q(patient__pk__icontains=request.GET.get("q"))|
            Q(diagnosis__name__icontains=request.GET.get("q"))
        )

    paginator = Paginator(objects, per_page=per_page)
    page = paginator.page(current_page)
    return render(request,RECEPTIONS_TMP,{
        "q": request.GET.get("q"),
        "page":{
            "current_page": current_page,
            "all_items": paginator.count,
            "all_pages": paginator.num_pages,
            "items": page.object_list
        }})

@login_required(login_url='/login')
def add_receptions(request):
    context = {
        'purpose_of_visits':PurposeOfVisit.objects.all(),
        "pacients":Patient.objects.all(),
        "diagnosis":Diagnosis.objects.all(),
        "doctors":Doctor.objects.all(),
    }
    if request.method == "POST":
        purpose_of_visit = request.POST.get("purpose_of_visit")
        patient = request.POST.get("patient")
        doctor = request.POST.get("doctor")
        diagnosis = request.POST.get("diagnosis")
        clinical_guid = request.POST.get("clinical_guid")


        context['purpose_of_visit'] = purpose_of_visit
        context['patient'] = patient
        context['doctor'] = doctor
        context['diagnosis'] = diagnosis
        context['clinical_guid'] = clinical_guid

        try:
            p = Reception(
                purpose_of_visit=PurposeOfVisit.objects.get(pk=purpose_of_visit),
                patient=Patient.objects.get(pk=patient),
                doctor=Doctor.objects.get(pk=doctor),
                diagnosis=Diagnosis.objects.get(pk=diagnosis),
                clinical_guid=clinical_guid

            )

            p.save()
            return redirect(reverse("home:detail_reception",kwargs={"pk":p.pk}))
        except BaseException as e:
            messages.error(request, str(e))

    return render(request,ADD_RECEPTION,context)

@login_required(login_url='/login')
def edit_receptions(request,pk):
    context = {
        'purpose_of_visits': PurposeOfVisit.objects.all(),
        "pacients": Patient.objects.all(),
        "diagnosis": Diagnosis.objects.all(),
        "doctors": Doctor.objects.all(),
    }
    obj = Reception.objects.get(pk=pk)
    context["obj"]=obj

    if request.method == "POST":
        purpose_of_visit = request.POST.get("purpose_of_visit")
        patient = request.POST.get("patient")
        doctor = request.POST.get("doctor")
        diagnosis = request.POST.get("diagnosis")
        clinical_guid = request.POST.get("clinical_guid")

        try:
            obj.purpose_of_visit = PurposeOfVisit.objects.get(pk=purpose_of_visit),
            obj.patient = Patient.objects.get(pk=patient)
            obj.doctor = Doctor.objects.get(pk=doctor)
            obj.diagnosis = Diagnosis.objects.get(pk=diagnosis)
            obj.clinical_guid = clinical_guid
            obj.save()
            messages.success(request,'Данные сохранены')
        except BaseException as e:
            messages.error(request, str(e))

    return render(request, EDIT_RECEPTION, context)

@login_required(login_url='/login')
def remove_receptions(request,pk):
    Reception.objects.get(pk=pk).delete()
    return redirect(reverse("home:receptions"))

@login_required(login_url='/login')
def remove_pacient(request,pk):
    Patient.objects.get(pk=pk).delete()
    return redirect(reverse("home:pacients"))



@login_required(login_url='/login')
def detail_receptions(request,pk):
    return render(request,DETAIL_RECEPTION,{"reception":Reception.objects.get(pk=pk)})

def login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']
        context['login'] = username
        context['password'] = username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            enter(request, user)
            return redirect(reverse("home:index"))
        else:
            messages.error(request, "неверный пароль или имя пользователя")

    return render(request,LOGIN_TMP,context)

@login_required(login_url='/login')
def logout(request):
    exit(request)
    return redirect(reverse("home:login"))

@login_required(login_url='/login')
def index(request):
    return render(request,HOME_TMP)
