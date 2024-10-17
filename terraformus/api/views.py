from rest_framework import generics, permissions

from terraformus.api.serializers import SolutionsSerializer
from terraformus.core.models import Solution
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
        return Solution.objects.filter(banned=False)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SolutionsSerializer
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
