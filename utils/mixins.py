"""
Mixins для Trials Service
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class SoftDeleteViewSetMixin:
    """
    Mixin для ViewSet с поддержкой мягкого удаления
    """
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Восстановление удаленного объекта"""
        instance = self.get_object()
        
        if not hasattr(instance, 'restore'):
            return Response(
                {'error': 'Модель не поддерживает восстановление'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.restore()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'])
    def hard_delete(self, request, pk=None):
        """Физическое удаление объекта"""
        instance = self.get_object()
        
        if hasattr(instance, 'hard_delete'):
            instance.hard_delete()
        else:
            instance.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def deleted(self, request):
        """Получить только удаленные объекты"""
        queryset = self.get_queryset().model.all_objects.dead()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


