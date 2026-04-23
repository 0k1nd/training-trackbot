from apps.trainings.models import Set
from apps.trainings.models.workouts import WorkoutExercise
from django.db.models import Max
from rest_framework import serializers


class AddSetSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField()
    workout_exercise_id = serializers.IntegerField()
    weight = serializers.FloatField(required=False)
    reps = serializers.IntegerField(required=False)
    difficulty = serializers.CharField()

    def validate(self, data):
        if data.get("weight") is None and data.get("reps") is None:
            raise serializers.ValidationError("weight or reps required")

        workout_exercise = WorkoutExercise.objects.filter(
            id=data["workout_exercise_id"],
            workout__user__chat_id=data["chat_id"],
            workout__finished_at__isnull=True,
            finished_at__isnull=True,
        ).first()

        if not workout_exercise:
            raise serializers.ValidationError("workout exercise not found")

        data["workout_exercise"] = workout_exercise
        return data

    def create(self, validated_data):
        workout_exercise = validated_data["workout_exercise"]
        max_number = workout_exercise.sets.aggregate(value=Max("set_number"))["value"] or 0

        return Set.objects.create(
            workout_exercise=workout_exercise,
            set_number=max_number + 1,
            weight=validated_data.get("weight"),
            reps=validated_data.get("reps"),
            difficulty=validated_data["difficulty"],
        )
