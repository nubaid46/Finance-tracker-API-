from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Transaction, SavingGoal
from django.utils import timezone
from decimal import Decimal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user


class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "user", "amount", "category", "description", "date"]

    def validate_amount(self, value):
        if value < Decimal("0"):
            raise serializers.ValidationError("Amount must be non-negative.")
        return value


class SavingGoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = SavingGoal
        fields = ["id", "user", "goal_name", "target_amount", "current_amount", "deadline", "progress_percent"]

    def get_progress_percent(self, obj):
        return obj.progress_percent()

    def validate(self, data):
        if data.get("target_amount") is not None and data.get("current_amount") is not None:
            if data["current_amount"] > data["target_amount"]:
                raise serializers.ValidationError("current_amount cannot exceed target_amount.")
        return data
