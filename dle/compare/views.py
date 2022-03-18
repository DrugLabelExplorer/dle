from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def index(request):
    context = {'route': 'compare/index.html'}
    return render(request, 'compare/index.html', context)

def compare_all(request):
    # get the DLs to be compared (add try/catch here)
    druglabel_obj1 = DrugLabel.objects.get(label_id = request.GET['first-label'])
    druglabel_obj2 = DrugLabel.objects.get(label_id = request.GET['second-label'])

    context = { 'dl1': druglabel_obj1, 'dl2': druglabel_obj2, "sections": []}

    # compare each section and build context items
    sections_fields = ['indication_usage', 'dosage', 'contraindication', 'adverse_reaction', 'description']

    for field in sections_fields:
        value1 = getattr(druglabel_obj1, field)
        value2 = getattr(druglabel_obj2, field)
        
        #TODO replace this simple compare
        data = { "sec_name": field, 
                "label1": value1, 
                "label2": value2 }

        if value1 == value2:
            data["is_match"] = "sec-match" 
        else:
            data["is_match"] = "sec-diff" 
        
        context["sections"].append(data)

    return render(request, 'compare/compare_all.html', context)