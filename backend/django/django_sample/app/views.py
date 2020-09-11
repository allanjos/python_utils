from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    data = {
        "result": 0,
        "message": "home"
    }

    return JsonResponse(data)

def handler404(request, exception):
    data = {
        "result": -1,
        "message": "not-found"
    }

    return JsonResponse(data)