from django.http import JsonResponse


def success(data='success', message='成功'):
    return JsonResponse({'Code': 200, 'Msg': message, 'Data': data})


def error(message='失败', status=200, code=400, data='error'):
    res = JsonResponse({'Code': code, 'Msg': message, 'Data': data})
    res.status_code = status
    return res
