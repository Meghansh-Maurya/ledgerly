from rest_framework import serializers
from .models import Transactions

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = "__all__"
        read_only_fields = ["user", "added_time"]
        