from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color', 'task_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_task_count(self, obj):
        return obj.tasks.count()
    
    def validate_name(self, value):
        user = self.context['request'].user
        # Check if category with this name exists for this user
        if Category.objects.filter(name=value, user=user).exists():
            if not self.instance or self.instance.name != value:
                raise serializers.ValidationError(
                    "You already have a category with this name."
                )
        return value
