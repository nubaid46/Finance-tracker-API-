from django.contrib import admin
from .models import Transaction, SavingGoal

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "category", "date", "description")
    list_filter = ("category", "date", "user")
    search_fields = ("user__username", "category", "description")

@admin.register(SavingGoal)
class SavingGoalAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "goal_name", "target_amount", "current_amount", "deadline")
    list_filter = ("deadline", "user")
    search_fields = ("goal_name", "user__username")
