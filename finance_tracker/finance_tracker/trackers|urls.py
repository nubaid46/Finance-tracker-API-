from django.urls import path
from .views import (
    RegisterView,
    TransactionListCreateView,
    TransactionDetailView,
    SavingGoalListCreateView,
    SavingGoalDetailView,
    AnalyticsView,
    AnomalyDetectionView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("transactions/", TransactionListCreateView.as_view(), name="transactions"),
    path("transactions/<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path("goals/", SavingGoalListCreateView.as_view(), name="goals"),
    path("goals/<int:pk>/", SavingGoalDetailView.as_view(), name="goal-detail"),
    path("analytics/", AnalyticsView.as_view(), name="analytics"),
    path("anomalies/", AnomalyDetectionView.as_view(), name="anomalies"),
]
