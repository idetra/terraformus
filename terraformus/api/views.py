from rest_framework import generics, permissions

from terraformus.api.serializers import SolutionsSerializer
from terraformus.core.models import Solution


class SolutionList(generics.ListAPIView):
    def get_queryset(self):
        return Solution.objects.filter(banned=False)

    permission_classes = [permissions.IsAuthenticated]
    queryset = Solution.objects.all()
    serializer_class = SolutionsSerializer


class SolutionItem(generics.RetrieveAPIView):
    def get_queryset(self):
        return Solution.objects.filter(banned=False)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SolutionsSerializer
    lookup_field = 'uuid'
