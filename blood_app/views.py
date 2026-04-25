from django.shortcuts import render
from .models import Donor
from .models import Hospital, BloodRequest
from .predict import predict_demand
from .models import BloodStock
import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO

def home(request):
    return render(request, 'home.html')
def donor_register(request):

    if request.method == "POST":
        name = request.POST.get("name")
        blood_group = request.POST.get("blood_group")
        phone = request.POST.get("phone")
        city = request.POST.get("city")

        Donor.objects.create(
            name=name,
            blood_group=blood_group,
            phone=phone,
            city=city
        )

    return render(request, "donor_register.html")
def hospital_request(request):

    if request.method == "POST":
        hospital_name = request.POST.get("hospital_name")
        blood_group = request.POST.get("blood_group")
        units_required = request.POST.get("units_required")
        request_date = request.POST.get("request_date")

        hospital = Hospital.objects.create(
            hospital_name=hospital_name
        )

        BloodRequest.objects.create(
    hospital_name=hospital_name,
    blood_group=blood_group,
    units_needed=units_required
)

    return render(request, "hospital_request.html")
def predict_page(request):
    result = None
    status = ""

    if request.method == "POST":
        try:
            # ✅ get safely
            month = request.POST.get('month')
            blood_group = request.POST.get('blood_group')
            collected = request.POST.get('collected')
            supplied = request.POST.get('supplied')

            # ✅ check empty values (VERY IMPORTANT)
            if not month or not blood_group or not collected or not supplied:
                return render(request, 'predict.html', {
                    'error': '⚠ Please select month & blood group properly (auto data not loaded)'
                })

            # ✅ convert safely
            month = int(month)
            blood_group = int(blood_group)
            collected = int(collected)
            supplied = int(supplied)

            # ✅ prediction
            result = predict_demand(month, blood_group, collected, supplied)

            if result > supplied:
                status = "⚠ Shortage Expected"
            else:
                status = "✅ Supply Sufficient"

        except Exception as e:
            return render(request, 'predict.html', {
                'error': f"Error: {str(e)}"
            })

    return render(request, 'predict.html', {
        'result': result,
        'status': status
    })
def shortage_check(request):
    requests = BloodRequest.objects.all()
    stocks = BloodStock.objects.all()

    shortage_list = []

    for req in requests:
        for stock in stocks:
            if req.blood_group == stock.blood_group:
                if req.units_needed > stock.units_available:
                    shortage_list.append({
                        "blood_group": req.blood_group,
                        "needed": req.units_needed,
                        "available": stock.units_available,
                        "shortage": req.units_needed - stock.units_available
                    })

    return render(request, "shortage.html", {
        "shortages": shortage_list
    })
def demand_graph(request):
    requests = BloodRequest.objects.all()

    blood_groups = []
    units_needed = []

    for req in requests:
        blood_groups.append(req.blood_group)
        units_needed.append(req.units_needed)

    plt.figure(figsize=(8, 5))
    plt.bar(blood_groups, units_needed)

    plt.title("Live Blood Demand by Blood Group")
    plt.xlabel("Blood Group")
    plt.ylabel("Units Needed")
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")
def dashboard(request):
    total_donors = Donor.objects.count()
    total_requests = BloodRequest.objects.count()

    data = pd.read_csv("dataset/dataset_bloods.csv")

    shortage = data[data["Units_Requested"] > data["Units_Supplied"]].copy()

    shortage["Shortage_Units"] = (
        shortage["Units_Requested"] - shortage["Units_Supplied"]
    )

    context = {
        "donors": total_donors,
        "requests": total_requests,
        "shortage": shortage.head(5).to_dict('records')
    }

    return render(request, "dashboard.html", context)
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from .models import UserProfile

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:

            login(request,user)

            
            profile = UserProfile.objects.filter(user=user).first()

            if not profile:
                return render(request, "login.html", {"error": "Profile not found"})

            if profile.role == "admin":
                return redirect('/dashboard/')

            elif profile.role == "donor":
                return redirect('/donor_dashboard/')

            elif profile.role == "hospital":
                return redirect('/hospital_dashboard/')


    return render(request,"login.html")
def donor_dashboard(request):
    donors = Donor.objects.all()

    context = {
        "message": "Welcome Donor",
        "total_donors": donors.count(),
        "donors_list": donors
    }

    return render(request, "donor_dashboard.html", context)


def hospital_dashboard(request):
    requests = BloodRequest.objects.all()

    context = {
        "message": "Welcome Hospital",
        "total_requests": requests.count(),
        "request_list": requests
    }

    return render(request, "hospital_dashboard.html", context)
# views.py
from django.shortcuts import redirect, get_object_or_404

def complete_request(request, id):
    req = get_object_or_404(BloodRequest, id=id)
    req.status = 'Completed'
    req.save()
    return redirect('admin_dashboard')


import pandas as pd
from django.http import JsonResponse

def get_data(request):
    try:
        month = request.GET.get('month')
        blood = request.GET.get('blood')

        if not month or blood is None:
            return JsonResponse({'collected': 0, 'supplied': 0})

        month = int(month)

        # ✅ map dropdown → dataset values
        blood_map = {
            "0": "O+",
            "1": "A+",
            "2": "B+",
            "3": "AB+",
            "4": "O-",
            "5": "A-",
            "6": "B-",
            "7": "AB-",
        }

        blood_value = blood_map.get(blood)

        # ✅ load dataset
        df = pd.read_csv("dataset/dataset_bloods.csv")

        # ✅ filter data
        row = df[
            (df["Month"] == month) &
            (df["Blood_Group"] == blood_value)
        ]

        if row.empty:
            return JsonResponse({'collected': 0, 'supplied': 0})

        collected = int(row["Units_Collected"].values[0])
        supplied = int(row["Units_Supplied"].values[0])

        return JsonResponse({
            'collected': collected,
            'supplied': supplied
        })

    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'collected': 0, 'supplied': 0})
