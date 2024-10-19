
from apps.user.serializers import UserProfileSerializer
from apps.user.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class UserProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        username = request.data.get("username")
        last_name = request.data.get("last_name")
        first_name = request.data.get("first_name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        avatar_thumbnail = request.data.get("avatar_thumbnail")

        instance = self.get_object()
        data = {
            "username": username,
            "last_name": last_name,
            "first_name": first_name,
            "email": email,
            "phone": phone,
        }
        if avatar_thumbnail:
            try:
                instance.avatar_thumbnail.delete(False)
            except: pass
            data["avatar_thumbnail"] = avatar_thumbnail
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
