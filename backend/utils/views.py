# /utils/views.py

# Django
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfTokenView(APIView):
    def get(self, request):
        return Response({'message': 'CSRF cookie set'}, status=status.HTTP_200_OK)