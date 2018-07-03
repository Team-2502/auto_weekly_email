import os

from django.shortcuts import render


# Create your views here.
import sys
print(__file__)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "weeklyemailgenerator/"))
import weeklyemailgenerator

def index(request):
    return render(request, "autoweeklyemail/index.html", {"stuff": weeklyemailgenerator.utils.generate_email()})
