from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, MonthlySummaryView, MonthlyCategorySummaryView

router = DefaultRouter()
router.register(r'', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('reports/summary/', MonthlySummaryView.as_view()),
    path('reports/by_category/', MonthlyCategorySummaryView.as_view()),
    
]