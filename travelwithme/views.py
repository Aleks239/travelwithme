from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "travelwithme/searchtrip.html")
def users(request):
    return render(request, "travelwithme/alltrips.html")
def login(request):
    return render(request, "travelwithme/login.html")
def signup(request):
    return render(request, "travelwithme/signup.html")
