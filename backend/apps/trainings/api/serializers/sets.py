from apps.trainings.models import Set
from apps.trainings.models.workouts import WorkoutExercise
from rest_framework import serializers


class AddSetSerializer(serializers.Serializer):
    workout_exercise_id = serializers.IntegerField()
    weight = serializers.FloatField(required=False)
    reps = serializers.IntegerField(required=False)
    difficulty = serializers.CharField()

    def validate(self, data):
        if not data.get("weight") and not data.get("reps"):
            raise serializers.ValidationError("weight or reps required")
        return data

    def create(self, validated_data):
        we = WorkoutExercise.objects.get(id=validated_data["workout_exercise_id"])

        last_set = we.sets.order_by("-set_number").first()
        next_number = (last_set.set_number + 1) if last_set else 1

        return Set.objects.create(
            workout_exercise=we,
            set_number=next_number,
            weight=validated_data.get("weight"),
            reps=validated_data.get("reps"),
            difficulty=validated_data["difficulty"],
        )
