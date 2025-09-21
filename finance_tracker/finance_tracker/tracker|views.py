from django.db.models import Sum
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction, SavingGoal
from .serializers import (
    RegisterSerializer,
    TransactionSerializer,
    SavingGoalSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from decimal import Decimal

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

# Transaction endpoints
class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


# Saving goals endpoints
class SavingGoalListCreateView(generics.ListCreateAPIView):
    serializer_class = SavingGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavingGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavingGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavingGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavingGoal.objects.filter(user=self.request.user)


# Analytics: totals and category summary
class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_spent = Transaction.objects.filter(user=user).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        category_summary_qs = Transaction.objects.filter(user=user).values("category").annotate(total=Sum("amount")).order_by("-total")
        category_summary = [{ "category": row["category"], "total": row["total"] } for row in category_summary_qs]

        # Goals progress
        goals = SavingGoal.objects.filter(user=user)
        goals_data = [
            {
                "id": g.id,
                "goal_name": g.goal_name,
                "target_amount": g.target_amount,
                "current_amount": g.current_amount,
                "deadline": g.deadline,
                "progress_percent": g.progress_percent(),
            } for g in goals
        ]

        return Response({
            "total_spent": total_spent,
            "category_summary": category_summary,
            "goals": goals_data,
        })


# Anomaly detection (basic). You can plug in ML later.
class AnomalyDetectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Basic rule-based anomalies:
        # 1) Single transaction exceeding a threshold
        # 2) Transactions in a category that are unusually high compared to user's median — (simple approach here)
        user = request.user
        threshold = request.query_params.get("threshold", None)
        try:
            threshold = Decimal(threshold) if threshold is not None else Decimal("10000.00")
        except:
            threshold = Decimal("10000.00")

        anomalies = Transaction.objects.filter(user=user, amount__gt=threshold).order_by("-amount")
        serializer = TransactionSerializer(anomalies, many=True)
        return Response({"threshold": str(threshold), "anomalies": serializer.data})
