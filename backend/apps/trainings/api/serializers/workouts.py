from apps.accounts.models import User
from apps.trainings.models import Workout
from rest_framework import serializers


class StartWorkoutSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField()

    def create(self, validated_data):
        user = User.objects.get(chat_id=validated_data["chat_id"])

        return Workout.objects.create(
            user=user,
        )


class FinishWorkoutSerializer(serializers.Serializer):
    workout_id = serializers.IntegerField()

    def validate_workout_id(self, value):
        if not Workout.objects.filter(id=value).exists():
            raise serializers.ValidationError("workout not found")
        return value
