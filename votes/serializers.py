from datetime import datetime
from rest_framework import serializers
from .models import Election, Position, Candidate, Vote
from django.contrib.auth import get_user_model

User = get_user_model()



class CandidateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), required=True)

    class Meta:
        model = Candidate
        fields = ["id", "name", "image", "position"]

       

class PositionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)

    class Meta:
        model = Position
        fields = ["id", "name", "candidates", "election"]



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
        extra_kwargs = {
            "election": {"required": True},
            "position": {"required": True},
            "candidate": {"required": True},
        }

    def validate(self, data):
        
        candidate = data.get("candidate")
        position = data.get("position")
        election = data.get("election")

        # If any of the three are missing, skip relational validation
        if not all([candidate, position, election]):
            return data

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
        fields = ["full_name", "matric_no", "password"]

    def validate_matric_no(self, value):
        """
        Validate that the matric_no is exactly 9 digits long
        and that digits 3–6 are '0561'.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Matric number must contain only digits.")

        if len(value) != 9:
            raise serializers.ValidationError("Matric number must be exactly 9 digits.")

        # Check digits 3–6 (indexes 2:6)
        if value[2:6] != "0561":
            raise serializers.ValidationError("Matric number must contain '0561' as its 3rd–6th digits.")
        
        start_two = int(value[:2])
        current_year_two = int(str(datetime.now().year)[-2:])  # e.g., 25 for 2025

        if start_two < 21 or start_two > current_year_two:
            raise serializers.ValidationError(
                f"Matric number must start with 21 up to {current_year_two}."
            )

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(
            full_name=validated_data.get("full_name"),
            matric_no=validated_data["matric_no"],
            username=validated_data["matric_no"],  # also set username to matric_no
            is_voter=True,
            is_admin=False,
        )
        user.set_password(password)
        user.save()
        return user
