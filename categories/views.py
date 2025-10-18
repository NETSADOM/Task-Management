from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer
from tasks.serializers import TaskSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing categories.
    Provides: list, create, retrieve, update, partial_update, and destroy
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only categories belonging to the authenticated user"""
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the user when creating a category"""
        serializer.save(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """
        GET /api/categories/{id}/
        Get a specific category by ID
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """
        PUT /api/categories/{id}/
        Update a category (full update)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /api/categories/{id}/
        Partial update of a category
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        DELETE /api/categories/{id}/
        Delete a category
        """
        instance = self.get_object()
        category_name = instance.name
        self.perform_destroy(instance)
        return Response(
            {"message": f"Category '{category_name}' deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """
        GET /api/categories/{id}/tasks/
        Get all tasks in a specific category
        """
        category = self.get_object()
        tasks = category.tasks.all()
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response(serializer.data)