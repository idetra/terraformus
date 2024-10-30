from rest_framework import generics, permissions

from terraformus.api.serializers import SolutionsSerializer, StrategySerializer
from terraformus.core.models import Solution, Strategy
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from terraformus.tokens import CustomRefreshToken, CustomAccessToken


class SolutionList(generics.ListAPIView):
    def get_queryset(self):
        return Solution.objects.filter(banned=False)

    permission_classes = [permissions.IsAuthenticated]
    queryset = Solution.objects.all()
    serializer_class = SolutionsSerializer


class SolutionItem(generics.RetrieveAPIView):
    def get_queryset(self):
        return Solution.objects.filter(
            banned=False).prefetch_related(
            'externalasset_set',
            'lifecycle_set__lifecycleinput_set',
            'lifecycle_set__lifecyclewaste_set'
        )

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SolutionsSerializer
    lookup_field = 'uuid'


class StrategyList(generics.ListAPIView):
    def get_queryset(self):
        print("Fetching strategies list")
        return Strategy.objects.filter(banned=False)

    permission_classes = [permissions.IsAuthenticated]
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer


class StrategyItem(generics.RetrieveAPIView):
    def get_queryset(self):
        return Strategy.objects.filter(banned=False).prefetch_related(
            'externalasset_set',
            'solutions__solution__externalasset_set',
            'solutions__solution__lifecycle_set',
            'solutions__solution__lifecycle_set__lifecycleinput_set',
            'solutions__solution__lifecycle_set__lifecyclewaste_set'
        )

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StrategySerializer
    lookup_field = 'uuid'


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            refresh = CustomRefreshToken(data['refresh'])
            user_id = refresh['user_id']
            access = CustomAccessToken.for_user(user_id)

            return Response({
                'access': str(access),
                'refresh': str(refresh),
            })
        except TokenError as e:
            raise InvalidToken(e.args[0])
