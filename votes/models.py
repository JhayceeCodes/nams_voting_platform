from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_voter = models.BooleanField(default=True)
    matric_no = models.CharField(max_length=9, unique=True, default=210561000)

    def __str__(self):
        if self.is_admin:
            return f"Admin: {self.username}"
        return f"Voter: {self.matric_no or self.username}"


class Election(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Position(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="positions", null=True, blank=True)
    name = models.CharField(max_length=255)  # e.g., "President", "Secretary"

    def __str__(self):
        return f"{self.name} ({self.election.title})"


class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="candidates")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="candidates")
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='candidates/', blank=True, null=True) 

    

    def __str__(self):
        return f"{self.name} - {self.position.name} ({self.election.title})"


class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="votes", null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="votes", null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="votes", null=True)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("election", "position", "voter")  # one vote per position per election

    def __str__(self):
        return f"{self.voter} -> {self.candidate.name} ({self.position.name})"
