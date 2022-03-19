from django.shortcuts import render
from django.http import HttpResponse

from .models import *


def index(request):
    context = {'route': 'compare/index.html'}
    return render(request, 'compare/index.html', context)


def compare_all(request):
    # get the DLs to be compared (TODO add try/catch here)
    druglabel_obj1 = DrugLabel.objects.get(label_id = request.GET['first-label'])
    druglabel_obj2 = DrugLabel.objects.get(label_id = request.GET['second-label'])
    context = { 'dl1': druglabel_obj1, 'dl2': druglabel_obj2, "sections": []}

    # compare each section and insert data in context.sections
    for field in SEC_DISPLAY_NAMES.keys():
        value1 = getattr(druglabel_obj1, field)
        value2 = getattr(druglabel_obj2, field)
        data = { "sec_name": SEC_DISPLAY_NAMES[field], 
                "label1": value1, 
                "label2": value2 }

        # compare if sections are exact match (TODO replace this with a diff algo)
        if value1 == value2:
            data["is_match"] = "sec-match" 
        else:
            data["is_match"] = "sec-diff" 
        
        context["sections"].append(data)

    return render(request, 'compare/compare_all.html', context)


def compare_diff(request):
    #TODO
    context = {'route': 'not implemented'}
    return render(request, 'compare/index.html', context)


def compare_match(request):
    #TODO
    context = {'route': 'not implemented'}
    return render(request, 'compare/index.html', context)
