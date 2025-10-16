"""
Авторизация и управление пользователями для Trials Service

Endpoints:
- POST /api/v1/auth/register/ - Регистрация нового пользователя
- POST /api/v1/auth/login/ - Вход (получение токена)
- POST /api/v1/auth/logout/ - Выход (удаление токена)
- GET /api/v1/auth/me/ - Текущий пользователь
- PUT /api/v1/auth/me/ - Обновить профиль
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .auth_serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Регистрация нового пользователя
    
    POST /api/v1/auth/register/
    Body: {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Иван",
        "last_name": "Иванов"
    }
    
    Returns:
        {
            "user": {...},
            "token": "abc123..."
        }
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Создаем токен для пользователя
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    Вход в систему (получение токена)
    
    POST /api/v1/auth/login/
    Body: {
        "username": "testuser",
        "password": "securepassword123"
    }
    
    Returns:
        {
            "user": {...},
            "token": "abc123..."
        }
    """
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    # Аутентификация пользователя
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({
            'success': False,
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
        return Response({
            'success': False,
            'error': 'User account is disabled'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Получаем или создаем токен
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'success': True,
        'message': 'Login successful',
        'user': UserSerializer(user).data,
        'token': token.key
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """
    Выход из системы (удаление токена)
    
    POST /api/v1/auth/logout/
    Headers: Authorization: Token abc123...
    
    Returns:
        {
            "success": true,
            "message": "Logout successful"
        }
    """
    try:
        # Удаляем токен текущего пользователя
        request.user.auth_token.delete()
        return Response({
            'success': True,
            'message': 'Logout successful'
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Получить или обновить данные текущего пользователя
    
    GET /api/v1/auth/me/
    Headers: Authorization: Token abc123...
    
    Returns:
        {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Иван",
            "last_name": "Иванов",
            "is_staff": false
        }
    
    PUT/PATCH /api/v1/auth/me/
    Body: {
        "first_name": "Петр",
        "last_name": "Петров",
        "email": "new@example.com"
    }
    """
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = UserSerializer(
            request.user, 
            data=request.data, 
            partial=partial
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Profile updated successfully',
                'user': serializer.data
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """
    Изменить пароль текущего пользователя
    
    POST /api/v1/auth/change-password/
    Body: {
        "old_password": "current_password",
        "new_password": "new_secure_password"
    }
    """
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response({
            'success': False,
            'error': 'Both old_password and new_password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Проверяем старый пароль
    if not request.user.check_password(old_password):
        return Response({
            'success': False,
            'error': 'Old password is incorrect'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Устанавливаем новый пароль
    request.user.set_password(new_password)
    request.user.save()
    
    # Пересоздаем токен (для безопасности)
    Token.objects.filter(user=request.user).delete()
    token = Token.objects.create(user=request.user)
    
    return Response({
        'success': True,
        'message': 'Password changed successfully',
        'token': token.key  # Новый токен
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    """
    Список всех пользователей (для администраторов и автокомплита)
    
    GET /api/v1/auth/users/
    Query params:
        - search: поиск по username, first_name, last_name
        - is_staff: только админы
    """
    users = User.objects.filter(is_active=True)
    
    # Фильтрация
    search = request.query_params.get('search')
    if search:
        users = users.filter(
            username__icontains=search
        ) | users.filter(
            first_name__icontains=search
        ) | users.filter(
            last_name__icontains=search
        )
    
    is_staff = request.query_params.get('is_staff')
    if is_staff is not None:
        users = users.filter(is_staff=is_staff.lower() == 'true')
    
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

