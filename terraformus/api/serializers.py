from rest_framework import serializers
from terraformus.core.models import Solution

class SolutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        # fields = '__all__'
        exclude = ['id', 'banned', 'user']

