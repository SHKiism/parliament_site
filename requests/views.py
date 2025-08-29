# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Request

def request_detail(request, req_id):
    req = get_object_or_404(Request, id=req_id)
    return render(request, "requests/detail.html", {"request_obj": req})

