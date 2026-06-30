from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProfileSerializer
from .models import Profile

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)