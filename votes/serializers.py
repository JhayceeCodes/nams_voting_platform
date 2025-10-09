from rest_framework import serializers
from .models import Election, Position, Candidate, Vote
from django.contrib.auth import get_user_model

User = get_user_model()


class CandidateSerializer(serializers.ModelSerializer):

   class Meta:
        model = Candidate
        fields = ["id", "name", "image", "position"]
        """extra_kwargs = {
            "position": {"read_only": True},
        }
"""

class PositionSerializer(serializers.ModelSerializer):
    """candidates = CandidateSerializer(many=True, required=False)

    class Meta:
        model = Position
        fields = ["id", "name", "election", "candidates"]"""
    candidates = CandidateSerializer(many=True, required=False)

    class Meta:
        model = Position
        fields = ["id", "name", "election", "candidates"]
        extra_kwargs = {
            "election": {"read_only": True},
        }


class ElectionSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, required=False)
   
    class Meta:
        model = Election
        fields = ["id", "title", "description", "start_date", "end_date", "positions"]

    def create(self, validated_data):
        positions_data = validated_data.pop("positions", [])
        election = Election.objects.create(**validated_data)

        for position_data in positions_data:
            candidates_data = position_data.pop("candidates", [])
            position = Position.objects.create(election=election, **position_data)

            for candidate_data in candidates_data:
                Candidate.objects.create(position=position, **candidate_data)

        return election


class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.ReadOnlyField(source="voter.username")  # show username instead of ID

    class Meta:
        model = Vote
        fields = ["id", "election", "position", "candidate", "voter"]

    def validate(self, data):
        """
        Custom validation:
        - Ensure candidate belongs to the given position.
        - Ensure position belongs to the given election.
        """
        candidate = data["candidate"]
        position = data["position"]
        election = data["election"]

        if candidate.position != position:
            raise serializers.ValidationError("Candidate does not belong to this position.")
        if position.election != election:
            raise serializers.ValidationError("Position does not belong to this election.")
        return data

    def create(self, validated_data):
        """
        Automatically set the voter as the logged-in user.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["voter"] = request.user
        return super().create(validated_data)
    



class VoterSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["matric_no", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(
            matric_no=validated_data["matric_no"],
            username=validated_data["matric_no"],  # also set username to matric_no
            is_voter=True,
            is_admin=False,
        )
        user.set_password(password)
        user.save()
        return user