from rest_framework import serializers
from django.utils import timezone
from .models import Task
from categories.models import Category
from categories.serializers import CategorySerializer


class TaskSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),   # ✅ provide a safe default queryset
        required=False,
        allow_null=True
    )
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 'status',
            'due_date', 'category', 'category_details', 'is_overdue',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        # ✅ safely filter categories by the logged-in user, if available
        if request and hasattr(request, 'user'):
            self.fields['category'].queryset = request.user.categories.all()

    def get_is_overdue(self, obj):
        """Return True if task is overdue and not completed."""
        if obj.due_date and obj.status != 'completed':
            return obj.due_date < timezone.now()
        return False

    def validate_due_date(self, value):
        """Prevent setting due date in the past."""
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
