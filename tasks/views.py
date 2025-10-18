from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        """Mark a task as complete"""
        task = self.get_object()
        task.mark_complete()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def incomplete(self, request, pk=None):
        """Mark a task as incomplete"""
        task = self.get_object()
        task.mark_incomplete()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get task statistics for the user"""
        user_tasks = self.get_queryset()
        
        total_tasks = user_tasks.count()
        completed_tasks = user_tasks.filter(status='completed').count()
        pending_tasks = user_tasks.filter(status='pending').count()
        in_progress_tasks = user_tasks.filter(status='in_progress').count()
        
        stats = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'completion_rate': round(
                (completed_tasks / total_tasks * 100), 2
            ) if total_tasks > 0 else 0
        }
        
        return Response(stats)