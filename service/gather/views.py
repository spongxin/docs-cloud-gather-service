from django.http.response import HttpResponse, JsonResponse


def package(request):
    return HttpResponse('package')