from rest_framework import serializers

from apps.accounts.models import User, BodyMetrics


class RegistrationSerializer(serializers.ModelSerializer):
    chat_id = serializers.IntegerField(write_only=True, required=True)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ("chat_id", "username")

    def create(self, validated_data):
        chat_id = validated_data.pop("chat_id")
        username = validated_data.get("username", "")

        user, created = User.objects.get_or_create(
            chat_id=chat_id,
            defaults={"username": username},
        )
        if not created and username and user.username != username:
            user.username = username
            user.save(update_fields=["username"])

        return user
    

class BodyMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyMetrics
        fields = [
            "id",
            "date",
            "weight_kg",
            "body_fat_percent",
            "neck_cm",
            "chest_cm",
            "waist_cm",
            "hips_cm",
            "thigh_cm",
            "calf_cm",
            "biceps_cm",
            "note",
        ]
