from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from travelwithme.models import Traveller, Trip
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.utils.dateparse import parse_date

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "travelwithme/searchtrip.html", {"user":request.user})

def users(request):
    return render(request, "travelwithme/alltrips.html")

def search_result(request):
    return render(request, "travelwithme/searchresult.html", {
        'id': 12345, 'list': [
      { "id": 1213, "topic": 'what should we do?', "hobby": 'Swim, soccer', 'email': 're@re.com', 'name': 'Lucy', 'reputation': 8.0 },
      { "id": 123, "topic": 'what should we do?', "hobby": 'Swim, soccer', 'email': 're@re.com', 'name': 'Lucy', 'reputation': 8.0 },
      { "id": 32, "topic": 'what should we do?', "hobby": 'Swim, soccer', 'email': 're@re.com', 'name': 'Lucy', 'reputation': 8.0 },
      { "id": 43, "topic": 'what should we do?', "hobby": 'Swim, soccer', 'email': 're@re.com', 'name': 'Lucy', 'reputation': 8.0 },
      { "id": 54, "topic": 'what should we do?', "hobby": 'Swim, soccer', 'email': 're@re.com', 'name': 'Lucy', 'reputation': 8.0 },
    ],
    })

def login_page(request):
    if request.user.is_authenticated:
         return redirect("travelwithme:index")
    return render(request, "travelwithme/login.html")

def rate_trip(request):
    return render(request, "travelwithme/ratepage.html")

def my_trip(request):
    return render(request, "travelwithme/mytrip.html")

def notification(request):
    return render(request, "travelwithme/notification.html")

def create_trip(request):
    return render(request, "travelwithme/createtrip.html")
    # if request.user.is_authenticated:
    # return redirect("travelwithme:index")


def signup(request):
    if request.user.is_authenticated:
         return redirect("travelwithme:index")
    return render(request, "travelwithme/signup.html")

def log_user_out(request):
    logout(request)
    return redirect("travelwithme:index")

def mytrips(request):
    if request.user.is_authenticated:
        traveller = request.user.traveller
        trips = Trip.objects.filter(creator=traveller)
        return render(request, "travelwithme/mytrips.html",{"trips":trips})
    return render(request, "travelwithme/login.html")

def user_info(request,traveller_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            traveller = get_object_or_404(Traveller,pk=traveller_id)
            return render(request, "travelwithme/user_info.html", {"traveller":traveller})
        else:
            return redirect("travelwithme:login")





#POST handlers


def search_trips(request):
    if request.method == "POST":
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        destination = request.POST["destination"]
        if start_date is not None and end_date is not None and destination is not None:
            if not start_date and not end_date and not destination:
                trips = Trip.objects.all()
                if request.user.is_authenticated:
                    trips = Trip.objects.filter(~Q(creator = request.user.traveller))
            elif not start_date and not end_date:
                trips = Trip.objects.filter(place=destination)
                if request.user.is_authenticated:
                    trips = Trip.objects.filter(~Q(creator = request.user.traveller),place=destination)
            elif not start_date or not end_date:
                return render(request, "travelwithme/searchtrip.html",{"error":"Date must be provided"})
            elif not destination:
                #search by dates
                trips = Trip.objects.filter(start_date__range=(start_date, end_date))
                if request.user.is_authenticated:
                    trips = Trip.objects.filter(~Q(creator = request.user.traveller), start_date__range=(start_date, end_date))
            else:
                #normal search
                trips = Trip.objects.filter(place=destination, start_date__range=(start_date, end_date))
                if request.user.is_authenticated:
                    trips = Trip.objects.filter(~Q(creator = request.user.traveller),place=destination, start_date__range=(start_date, end_date))
        return render(request, "travelwithme/alltrips.html",{"trips":trips})
    else:
        return HttpResponse(status=500)

def create_trip(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            place = request.POST['place']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            if place is not None and start_date is not None and end_date is not None:
                if not place or not start_date or not end_date:
                    return render(request, "travelwithme/searchtrip.html", {"error":"Empty fields"})
                else:
                    date_start_date = parse_date(start_date)
                    date_end_date = parse_date(end_date)
                    if date_end_date < date_start_date:
                        return render(request, "travelwithme/searchtrip.html", {"error":"Dates mismatch"})
                    Trip.objects.create(creator=user.traveller, place=place, start_date=start_date, end_date=end_date)
                    return redirect("travelwithme:mytrips")
                    #redirect to my trips.

        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)


def signup_user(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        nationality = request.POST['nationality']
        birthday = request.POST['birthday']
        gender = request.POST['gender']
        password = request.POST['password']
        hobbies = request.POST['hobbies']
        if first_name is not None and last_name is not None and email is not None and nationality is not None and birthday is not None and password is not None and gender is not None and hobbies is not None:
            if not first_name or not last_name or not email or not nationality or not birthday or not gender or not password:
                return render(request, "travelwithme/signup.html", {"error":"Empty fields"})
            elif User.objects.filter(email=email).exists():
                return render(request, "travelwithme/signup.html", {"error":"User exists"})
            else:
                username = email
                user = User.objects.create_user(username, email=email, first_name=first_name, last_name=last_name, password=password)
                traveller = Traveller.objects.create(user=user, hobbies=hobbies, nationality=nationality, birthday=birthday, gender=gender).save()
                user.save()
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                return redirect("travelwithme:index")


        else:
            return render(request, "travelwithme/signup.html", {"error":"Error in fields"})
    else:
        return render(request, "travelwithme/signup.html")

def log_user_in(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        if email is not None and password is not None:
            if not email or not password:
                return render(request, "travelwithme/login.html", {"error": "Empty input"})

            else:
                username = email
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("travelwithme:index")
                else:
                    return render(request, "travelwithme/login.html", {"error":"Wrong username or password"})

        else:
            return render(request, "travelwithme/login.html", {"error": "Error in fields"})
    else:
        return redirect("travelwithme:login")
