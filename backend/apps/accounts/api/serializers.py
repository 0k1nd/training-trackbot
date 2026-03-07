from rest_framework import serializers

from apps.accounts.models import User


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