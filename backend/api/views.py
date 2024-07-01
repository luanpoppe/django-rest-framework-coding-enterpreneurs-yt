import json
from django.http import JsonResponse

def api_home(request, *args):
    body = request.body

    data = {}
    try:
        data = json.loads(body)
    except:
        pass

    # print(data)
    print(request.GET)
    return JsonResponse({"message": "Hi there,"}) 