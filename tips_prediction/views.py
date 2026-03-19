from django.http import HttpResponse
from django.shortcuts import render
import os , pickle
import pandas as pd

def homepage(request):
    return render(request,"index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request , "contact.html")

def skill(request):
    return render(request , "skill.html")


# model load
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)


def tip_prediction(request):

    prediction = None

    if request.method == "POST":

        total_bill = float(request.POST.get("total_bill"))
        size = int(request.POST.get("size"))
        sex = request.POST.get("sex")
        smoker = request.POST.get("smoker")
        day = request.POST.get("day")
        time = request.POST.get("time")

        input_df = pd.DataFrame({
            'total_bill':[total_bill],
            'sex':[sex],
            'smoker':[smoker],
            'day':[day],
            'time':[time],
            'size':[size]
        })

        input_df = pd.get_dummies(input_df)

        if hasattr(model, "feature_names_in_"):
            input_df = input_df.reindex(columns=model.feature_names_in_, fill_value=0)

        prediction = model.predict(input_df)[0] * 10

    return render(request, "tip_prediction.html", {"prediction":prediction})