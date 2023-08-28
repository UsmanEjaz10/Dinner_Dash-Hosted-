from typing import Any
from django.middleware import *
from django.shortcuts import HttpResponse, redirect, render

class custom_middleware:
    def __init__(self, request) -> None:
        print("custom middleware has been initialized.....")

    def __call__(self, request, *args: Any, **kwds: Any) -> Any:
        print("printing before response")

        response = request.getResponse(request)

        print("View has been called..")

        return render(request, 'about.html')