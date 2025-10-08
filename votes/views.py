from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users can vote


class VoterSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = VoterSignupSerializer
    permission_classes = [permissions.AllowAny]