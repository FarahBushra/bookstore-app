import imp
from django.shortcuts import render
from django.http import JsonResponse
from .books import books

# Create your views here.

def getRoutes(request):
    routes = [

        "/api/books/",
        "/api/books/create",

        "/api/books/upload/",

        "/api/books/<id>/reviews",

        "/api/books/top/",
        "/api/books/<id>/",

        "/api/books/delete/<id>",
       "/api/books/<update>/<id>/",
   
    ]


    return JsonResponse(routes, safe=False)



# def getBooks(request):
#      return JsonResponse(books, safe=False)