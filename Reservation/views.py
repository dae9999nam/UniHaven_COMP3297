from django.shortcuts import render
from rest_framework import generics
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from Accommodations.serializers import AccommodationSerializer
from .models import Reservation
from .serializers import ReservationSerializer
# Create your views here.

# for specialist to create
class CreateReservation(generics.ListCreateAPIView):
    queryset = Reservation.objects.all() 
    serializer_class = ReservationSerializer
    
    def perform_create(self, serializer):
        reservation = serializer.save()
        self.send_confirmation_email(reservation)

    def send_confirmation_email(self, reservation):
        subject = "Your Reservation Confirmation"

        # Create HTML message
        html_message = render_to_string(
            "reservation_confirmation_email.html",
            {
                "user": reservation.user,
                "reservation": reservation,
            },
        )

        # Create plain text version
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reservation.user.email],
            fail_silently=False,
        )


# for specialist to modify
class ModifyReservation(generics.RetrieveUpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = "pk"

# for students to cancel (update status to cancelled)
class CancelReservation(generics.RetrieveUpdateAPIView):  
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        reservation = serializer.save(status="cancelled")
        self.send_cancellation_email(reservation)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def send_cancellation_email(self, reservation):
        subject = "Your Reservation Has Been Cancelled"

        # Create HTML message
        html_message = render_to_string(
            "reservation_cancellation_email.html",
            {
                "user": reservation.user,
                "reservation": reservation,
            },
        )

        # Create plain text version
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reservation.user.email],
            fail_silently=False,
        )


class ViewReservationList(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ViewReservedAccommodationDetail(generics.RetrieveAPIView):
    """
    Get accommodation details by reservation ID
    """
    serializer_class = AccommodationSerializer
    lookup_url_kwarg = 'pk'  # The reservation ID parameter

    def get_object(self):
        reservation = Reservation.objects.get(pk=self.kwargs['pk'])
        return reservation.accommodation_id