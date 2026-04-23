from apps.accounts.models import User
from apps.trainings.models import Workout
from rest_framework import serializers


class StartWorkoutSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField()

    def validate(self, attrs):
        user = User.objects.filter(chat_id=attrs["chat_id"]).first()
        if not user:
            raise serializers.ValidationError("user not found")

        active_workout = Workout.objects.filter(
            user=user,
            finished_at__isnull=True,
        ).first()
        if active_workout:
            raise serializers.ValidationError("active workout already exists")

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        return Workout.objects.create(
            user=validated_data["user"],
        )


class FinishWorkoutSerializer(serializers.Serializer):
    workout_id = serializers.IntegerField()
    chat_id = serializers.IntegerField()

    def validate(self, attrs):
        workout = Workout.objects.filter(
            id=attrs["workout_id"], user__chat_id=attrs["chat_id"]
        ).first()

        if not workout:
            raise serializers.ValidationError("workout not found")

        attrs["workout"] = workout
        return attrs
