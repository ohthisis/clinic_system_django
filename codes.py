from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Customer,Menu
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from .serializers import MenuSerializer
from rest_framework.generics import GenericAPIView


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = make_password(data.get('password'))

        if not (name and email and password):
            return JsonResponse({'error': 'Name, email, and password are required'}, status=400)

        Customer.objects.create(email=email, name=name, password=password)

        response_data = {
            'message': 'Registration successful',
            'data': {
                'name': name,
                'email': email,
            }
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=400)
        if check_password(password, user.password):
            user_tokens = user.tokens()
            print(user_tokens)
            return JsonResponse({'message': 'Login successful'})
        
        else:
            # Passwords don't match
            return JsonResponse({'error': 'Invalid email or password'}, status=400)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

class MenuListView(GenericAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get(self, request, *args, **kwargs):
        menus_queryset = self.get_queryset()
        serializer = self.get_serializer(menus_queryset, many=True)
        return Response({'menus': serializer.data}, status=200)