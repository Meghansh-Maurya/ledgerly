from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TransactionsSerializer
from .filters import TransactionFilter
from .models import Transactions
from django.utils import timezone
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    
    def get_queryset(self):
        return Transactions.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class MonthlySummaryView(APIView):
    def get(self, request):
        today = timezone.now()
        
        transactions = Transactions.objects.filter(
            user=request.user,
            date__year=today.year,
            date__month=today.month
        )
        
        income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        
        
        response = {
            "income" : income,
            "expense" : expense,
            "savings" : income - expense,
        }
        
        return Response(response)
    
    
class MonthlyCategorySummaryView(APIView):
    def get(self, request):
        today = timezone.now()
        
        transactions = Transactions.objects.filter(
            user=request.user,
            type="expense",
            date__year=today.year,
            date__month=today.month
        )
        
        breakdown = transactions.values('category').annotate(total = Sum('amount'))
        
        return Response(breakdown)
    
        
