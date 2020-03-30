from django.http import HttpResponseNotFound
import json

def error404(request, exception):
    response_data = {}
    response_data['detail'] = 'The endpoint does not exist.'
    return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")

def error500(request):
    response_data = {}
    response_data['detail'] = 'Something went wrong.'
    return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")