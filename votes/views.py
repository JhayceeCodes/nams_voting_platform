from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.decorators import api_view, permission_classes
from .models import Election, Position, Candidate, Vote
from .serializers import ElectionSerializer, PositionSerializer, CandidateSerializer, VoteSerializer, VoterSignupSerializer
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model




User = get_user_model()





class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]  # only superusers/staff can modify elections
        return [IsAuthenticated()]  # anyone can view

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]  # only superusers/staff can modify elections
        return [IsAuthenticated()]  # anyone can view


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]  # only superusers/staff can modify elections
        return [IsAuthenticated()]  # anyone can view


class IsSuperUser(BasePermission):
    """Allows access only to superusers."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsRegularUser(BasePermission):
    """Allows access only to non-superusers."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_superuser)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def get_permissions(self):
        """Restrict GET to superusers, POST to normal users."""
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsSuperUser]
        elif self.action == "create":
            permission_classes = [IsRegularUser]
        else:
            permission_classes = []  # No one can PUT/PATCH/DELETE
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'PUT' and 'PATCH' not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'DELETE' not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class VoterSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = VoterSignupSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_vote_status(request):
    voter = request.user
    return Response({"have_voted": voter.have_voted})