# myapp/views.py
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def fetch_api_data(request):
    url = "https://example.com/api/data"  # 取得したいAPIのURL
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # 必要なら
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 失敗時に例外発生
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {"error": str(e)}
    
    return render(request, "myapp/api.html", {"data": data})

@csrf_exempt  # 必要に応じて
def send_data_to_api(request):
    if request.method == "POST":
        payload = {
            "name": request.POST.get("name"),
            "age": request.POST.get("age")
        }
        headers = {"Authorization": "Bearer YOUR_API_KEY"}

        try:
            response = requests.post("https://example.com/api/data", json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            result = {"error": str(e)}

        return render(request, "myapp/api_result.html", {"result": result})

    # GETの場合はフォームを表示
    return render(request, "myapp/api_form.html")