from django.core.cache import cache
from django.db import connections
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


def liveness(request):
    return JsonResponse({"status": "alive"})


def readiness(request):
    try:
        # check database connection
        connections["default"].cursor()

        # Check cache connection
        cache.set("health_check", "ok", timeout=10)
        if cache.get("health_check") != "ok":
            raise Exception("Cache is not working")

        return JsonResponse({"status": "healthy"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "unhealthy", "error": str(e)}, status=500)
