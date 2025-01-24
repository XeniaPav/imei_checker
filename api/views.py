from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests


@csrf_exempt
def check_imei(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            imei = data.get("imei")
            token = data.get("token")

            if not imei or not token:
                return JsonResponse({"error": "IMEI и токен обязательны."}, status=400)
            response = requests.post(
                "https://imeicheck.net/api/v1/check",
                data={"imei": imei, "token": token},
            )

            if response.status_code == 200:
                return JsonResponse(response.json(), safe=False)
            else:
                return JsonResponse(
                    {"error": "Ошибка при проверке IMEI."}, status=response.status_code
                )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверный формат JSON."}, status=400)
    return JsonResponse({"error": "Метод не разрешен."}, status=405)
