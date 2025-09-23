from django.contrib import messages
# Create your views here.
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import Group,User
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from datetime  import datetime
# Create your views here.

from django.contrib.auth.decorators import login_required

def login_page(request):
    logout(request)
    return render(request,"index.html")


def loginpost(request):
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        print("hhh")
        if user.groups.filter(name="Admin").exists():
            print("jajaja")
            login(request, user)
            return redirect('/myapp/admin_home/')
        if user.groups.filter(name="Service").exists():
            print("jajaja")
            ob=Service_Table.objects.get(LOGIN__id=user.id)
            if ob.status=='service':
                login(request, user)
                return redirect('/myapp/service_home/')
        if user.groups.filter(name="User").exists():
            print("jajaja")
            login(request, user)
            return redirect('/myapp/user_home/')
    else:
        messages.warning(request, "Invalid username or password")
        return redirect('/myapp/')
    messages.warning(request, "Invalid username or password")
    return redirect('/myapp/')






def logouta(request):
    logout(request)
    return redirect('/myapp/')

@login_required(login_url='/myapp/')
def admin_home(request):
    return render(request,"adminindex.html")


@login_required(login_url='/myapp/')
def aview_complaints(request):
    complaints = Complaint_Table.objects.all()
    return render(request, "admin/complaint.html", {"complaints": complaints})

@login_required(login_url='/myapp/')
def reply_complaint(request, id):
    comp = get_object_or_404(Complaint_Table, id=id)
    if request.method == "POST":
        comp.reply = request.POST.get("reply")
        comp.save()
        return redirect("/myapp/aview_complaints/")


@login_required(login_url='/myapp/')
def view_user(request):
    ob=User_Table.objects.all()
    return render(request,"admin/view_user.html",{"users":ob})

@login_required(login_url='/myapp/')
def view_service(request):
    ob=Service_Table.objects.filter(status='service')
    return render(request,"admin/view_service.html",{"services":ob})

@login_required(login_url='/myapp/')
def verify_service(request):
    ob=Service_Table.objects.filter(status='pending')
    return render(request,"admin/verify_service.html",{"services":ob})

@login_required(login_url='/myapp/')
def accept_service(request,id):
    ob=Service_Table.objects.get(id=id)
    ob.status='service'
    ob.save()
    return redirect("/myapp/verify_service/#about")

@login_required(login_url='/myapp/')
def reject_service(request,id):
    ob = Service_Table.objects.get(id=id)
    ob.status = 'reject'
    ob.save()
    return redirect("/myapp/verify_service/#about")


from django.shortcuts import render, redirect, get_object_or_404

@login_required(login_url='/myapp/')
def view_complaints(request):
    complaints = Complaint_Table.objects.all()
    return render(request, "admin/view_complaints.html", {"complaints": complaints})

@login_required(login_url='/myapp/')
def send_reply(request, complaint_id):
    complaint = get_object_or_404(Complaint_Table, id=complaint_id)
    if request.method == "POST":
        reply_text = request.POST["reply"]
        complaint.reply = reply_text
        complaint.save()
    return redirect("/myapp/view_complaints/")


def registration_service(request):
    if request.method == "POST":
        name = request.POST["name"]
        phoneno = request.POST["phoneno"]
        place = request.POST["place"]
        post = request.POST["post"]
        pin = request.POST["pin"]
        email = request.POST["email"]
        password = request.POST["password"]
        username=request.POST['uname']
        photo = request.FILES["photo"]
        user = User.objects.create(username=username, password=make_password(password), email=email, first_name=name)
        user.save()
        user.groups.add(Group.objects.get(name="Service"))
        Service_Table.objects.create(
            LOGIN=user,
            name=name,
            phoneno=phoneno,
            place=place,
            post=post,
            pin=pin,
            email=email,
            photo=photo,
        )
        messages.success(request,"Success")
        return redirect("/myapp/")


    return render(request,"registration_service.html")



@login_required(login_url='/myapp/')
def service_home(request):
    return render(request,"serviceindex.html")

@login_required(login_url='/myapp/')
def view_profile(request):
    profile=Service_Table.objects.get(LOGIN__id=request.user.id)
    return render(request,"service/profile.html",{"profile":profile})


@login_required(login_url='/myapp/')
def update_profile(request):
    profile=Service_Table.objects.get(LOGIN__id=request.user.id)
    if request.method == "POST":

        profile.name = request.POST["name"]
        profile.phoneno = request.POST["phoneno"]
        profile.place = request.POST["place"]
        profile.post = request.POST["post"]
        profile.pin = request.POST["pin"]
        profile.email = request.POST["email"]


        if "photo" in request.FILES:
            profile.photo = request.FILES["photo"]


        profile.save()


        return redirect("/myapp/view_profile/#about")
    return render(request,"service/update_profile.html",{"profile":profile})






@login_required(login_url='/myapp/')
def view_complaints1(request):
    complaints = Complaint_Table.objects.filter(LOGIN=request.user)
    return render(request, "service/complaint.html", {"complaints": complaints})

@login_required(login_url='/myapp/')
def add_complaint1(request):
    if request.method == "POST":
        text = request.POST.get("complaint")
        Complaint_Table.objects.create(
            LOGIN=request.user,
            complaint=text,
            date=datetime.today(),
            reply="pending"
        )
        messages.success(request, "Complaint submitted successfully!")
    return redirect("/myapp/view_complaints1#about")

@login_required(login_url='/myapp/')
def delete_complaint1(request, comp_id):
    complaint = get_object_or_404(Complaint_Table, id=comp_id, LOGIN=request.user)
    complaint.delete()
    messages.warning(request, "Complaint deleted.")
    return redirect("/myapp/view_complaints1#about")









@login_required(login_url='/myapp/')
def view_works(request):

    works = Work_Table.objects.filter(SERVICE__LOGIN__id=request.user.id)
    return render(request, "service/mywork.html", {"works": works})


@login_required(login_url='/myapp/')
def add_work(request):
    service = Service_Table.objects.get(LOGIN=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        photo = request.FILES.get("photo")

        work = Work_Table.objects.create(
            SERVICE=service,
            title=title,
            description=description,
            price=price,
            photo=photo,
            date=datetime.today()
        )
        return redirect("/myapp/view_works/#about")

    return render(request, "service/addwork.html")


@login_required(login_url='/myapp/')
def update_work(request, work_id):
    request.session['wid']=work_id
    return redirect("/myapp/update_work1")

@login_required(login_url='/myapp/')
def update_work1(request):
    work = Work_Table.objects.get(id=request.session['wid'])

    if request.method == "POST":
        work.title = request.POST.get("title")
        work.description = request.POST.get("description")
        work.price = request.POST.get("price")

        if "photo" in request.FILES:
            work.photo = request.FILES["photo"]

        work.save()
        return redirect("/myapp/view_works/#about")

    return render(request, "service/update_work.html", {"work": work})


@login_required(login_url='/myapp/')
def delete_work(request, work_id):
    work = Work_Table.objects.get( id=work_id)
    work.delete()
    return redirect("/myapp/view_works/#about")


@login_required(login_url='/myapp/')
def service_view_works_request(request):

    works = Request_Table.objects.filter(WORK__SERVICE__LOGIN__id=request.user.id)

    return render(request, "service/view_work_request.html", {"requests": works})



@login_required(login_url='/myapp/')
def approve_request(request):
    if request.method == "POST":
        req_id = request.POST.get("request_id")
        price = request.POST.get("price")

        req = get_object_or_404(Request_Table, id=req_id)
        req.price = price
        req.status = "Approved"
        req.save()

        messages.success(request, "Request approved successfully!")
        return redirect("/myapp/service_view_works_request/#about")  # change to your request list page

@login_required(login_url='/myapp/')
def reject_request(request, req_id):
    req = get_object_or_404(Request_Table, id=req_id)
    req.status = "Rejected"
    req.save()
    messages.warning(request, "Request rejected.")
    return redirect("/myapp/service_view_works_request/#about")











def user_register(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]


        name = request.POST["name"]
        phoneno = request.POST["phoneno"]
        place = request.POST["place"]
        post = request.POST["post"]
        pin = request.POST["pin"]
        email = request.POST["email"]
        photo = request.FILES["photo"]


        user = User.objects.create(username=username, password=make_password(password), email=email, first_name=name)
        user.save()
        user.groups.add(Group.objects.get(name="User"))


        # Create user profile
        User_Table.objects.create(
            LOGIN=user,
            name=name,
            phoneno=phoneno,
            place=place,
            post=post,
            pin=pin,
            email=email,
            photo=photo,
            status="user"
        )
        messages.success(request, "Success")

        return redirect("/myapp/")  # after registration redirect to login page

    return render(request, "user_reg.html")



@login_required(login_url='/myapp/')

def user_home(request):
    return render(request,"userindex.html")

@login_required(login_url='/myapp/')
def user_view_works(request):

    works = Work_Table.objects.all()
    return render(request, "user/view_work.html", {"works": works})


@login_required(login_url='/myapp/')
def user_view_works_request(request):

    works = Request_Table.objects.filter(USER__LOGIN__id=request.user.id)
    return render(request, "user/view_work_request.html", {"request": works})





@login_required(login_url='/myapp/')
def view_complaints(request):
    complaints = Complaint_Table.objects.filter(LOGIN=request.user)
    return render(request, "user/complaint.html", {"complaints": complaints})

@login_required(login_url='/myapp/')
def add_complaint(request):
    if request.method == "POST":
        text = request.POST.get("complaint")
        Complaint_Table.objects.create(
            LOGIN=request.user,
            complaint=text,
            date=datetime.today(),
            reply="pending"
        )
        messages.success(request, "Complaint submitted successfully!")
    return redirect("view_complaints")

@login_required(login_url='/myapp/')
def delete_complaint(request, comp_id):
    complaint = get_object_or_404(Complaint_Table, id=comp_id, LOGIN=request.user)
    complaint.delete()
    messages.warning(request, "Complaint deleted.")
    return redirect("view_complaints")




@login_required(login_url='/myapp/')
def request_work(request):
    if request.method == "POST":
        work_id = request.POST.get("work_id")
        details = request.POST.get("details")
        preferred_date = request.POST.get("preferred_date")

        work = Work_Table.objects.get(id=work_id)
        # Assuming you have a RequestWork model
        ob=Request_Table()
        ob.WORK= work
        ob.USER= User_Table.objects.get(LOGIN__id=request.user.id)
        ob.details= details
        ob.date= datetime.today()
        ob.due_date= preferred_date
        ob.price=0
        ob.status='pending'
        ob.save()
        messages.success(request, "Your booking request has been submitted!")
        return redirect("/myapp/user_view_works/#about")



# Chat Service



@login_required(login_url='/myapp/')

def chat_view_service(request,id):
    try:
        request.session["userid"] = id
        qry=User_Table.objects.get(LOGIN__id=id)
        request.session["new"] = id
        return render(request, "Chat.html",{'photo': qry.photo.url, 'name': qry.name, 'toid': id})
    except:
        request.session["userid"] = id
        qry=Service_Table.objects.get(LOGIN__id=id)
        request.session["new"] = id
        return render(request, "Chat.html",{'photo': qry.photo.url, 'name': qry.name, 'toid': id})



@login_required(login_url='/myapp/')
def chat_view(request):
    fromid = request.user.id
    toid = request.session["userid"]
    try:
        qry = User_Table.objects.get(LOGIN=request.session["userid"])
    except:
        qry = Service_Table.objects.get(LOGIN=request.session["userid"])
    from django.db.models import Q

    res = Chat_Table.objects.filter(Q(FROM__id=fromid,TO__id=toid) | Q(FROM__id=toid, TO__id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TO_id, "date": i.date, "from": i.FROM_id})

    return JsonResponse({'photo':qry.photo.url, "data": l, 'name': qry.name, 'toid': request.session["userid"]})

@login_required(login_url='/myapp/')
def chat_send(request, msg):
    lid = request.user.id
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat_Table()
    chatobt.message = message
    chatobt.TO_id = toid
    chatobt.FROM_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})












