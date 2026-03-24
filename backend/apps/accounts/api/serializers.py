from rest_framework import serializers

from apps.accounts.models import User, BodyMetrics


class RegistrationSerializer(serializers.ModelSerializer):
    chat_id = serializers.IntegerField(write_only=True, required=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("chat_id", "username")

    def create(self, validated_data):
        chat_id = validated_data.pop("chat_id")
        raw_username = validated_data.get("username") or ""

        username = raw_username.strip()
        if not username:
            username = f"user_{chat_id}"

        user, created = User.objects.get_or_create(
            chat_id=chat_id,
            defaults={"username": username},
        )

        if not created and raw_username and user.username != username:
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
