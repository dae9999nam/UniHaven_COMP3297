from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.core.mail import send_mail
from django.conf import settings

from authentication.authentication import ServiceTokenAuthentication
from .models import Reservation
from .serializers import ReservationSerializer
from Accommodations.serializers import AccommodationSerializer

# Create and list reservations
class CreateReservation(generics.ListCreateAPIView):
    # Allow both session-login (for browsable API) and service-token auth
    authentication_classes = [SessionAuthentication, ServiceTokenAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.all()

    def perform_create(self, serializer):
        reservation = serializer.save()
        print(f"[DEBUG] Created reservation: ID={reservation.reservation_id}, contact={reservation.contact}, accommodation={reservation.accommodation.name}")

        # Notify the user
        user_subject = 'Your Reservation Confirmation'
        user_message = (
            f"Hello {reservation.contact},\n"
            f"Your reservation (ID: {reservation.reservation_id}) for {reservation.accommodation.name} is confirmed.\n"
            "Thank you for using UniHaven."
        )
        print(f"[DEBUG] Sending user email: subject={user_subject}, to={reservation.contact}")
        send_mail(user_subject, user_message, settings.DEFAULT_FROM_EMAIL, [reservation.contact], fail_silently=False)

        # Notify specialists
        for uni in reservation.accommodation.universities.all():
            support_email = uni.specialist_email.strip()
            print(f"[DEBUG] University {uni.code} specialist_email: '{support_email}'")
            support_subject = f"New reservation #{reservation.reservation_id}"
            support_message = (
                f"A new reservation has been created:\n"
                f"• ID: {reservation.reservation_id}\n"
                f"• Property: {reservation.accommodation.name}\n"
                f"• Dates: {reservation.start_date} to {reservation.end_date}\n"
                f"• Contact: {reservation.contact}\n"
            )
            if support_email:
                print(f"[DEBUG] Sending specialist email: subject={support_subject}, to={support_email}")
                send_mail(support_subject, support_message, settings.DEFAULT_FROM_EMAIL, [support_email], fail_silently=False)
            else:
                print(f"--- Specialist Notification for {uni.code} (no email configured) ---")
                print(f"Subject: {support_subject}")
                print(support_message)

# Update reservation
class ModifyReservation(generics.RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, ServiceTokenAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ReservationSerializer
    lookup_field           = 'pk'

    def get_queryset(self):
        return Reservation.objects.all()

    def perform_update(self, serializer):
        reservation = serializer.save()
        print(f"[DEBUG] Modified reservation: ID={reservation.reservation_id}, contact={reservation.contact}")

        # Notify the user
        user_subject = 'Your Reservation Has Been Updated'
        user_message = (
            f"Hello {reservation.contact},\n"
            f"Your reservation (ID: {reservation.reservation_id}) for {reservation.accommodation.name} has been updated.\n"
            "Please review the changes in your account."
        )
        print(f"[DEBUG] Sending user update email: subject={user_subject}, to={reservation.contact}")
        send_mail(user_subject, user_message, settings.DEFAULT_FROM_EMAIL, [reservation.contact], fail_silently=False)

        # Notify specialists
        for uni in reservation.accommodation.universities.all():
            support_email = uni.specialist_email.strip()
            print(f"[DEBUG] University {uni.code} specialist_email: '{support_email}'")
            support_subject = f"Reservation #{reservation.reservation_id} Updated"
            support_message = (
                f"A reservation has been updated:\n"
                f"• ID: {reservation.reservation_id}\n"
                f"• Property: {reservation.accommodation.name}\n"
                f"• Dates: {reservation.start_date} to {reservation.end_date}\n"
                f"• Contact: {reservation.contact}\n"
            )
            if support_email:
                print(f"[DEBUG] Sending specialist update email: subject={support_subject}, to={support_email}")
                send_mail(support_subject, support_message, settings.DEFAULT_FROM_EMAIL, [support_email], fail_silently=False)
            else:
                print(f"--- Specialist Update Notification for {uni.code} (no email configured) ---")
                print(f"Subject: {support_subject}")
                print(support_message)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# Cancel reservation
class CancelReservation(generics.RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, ServiceTokenAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ReservationSerializer
    lookup_field           = 'pk'

    def get_queryset(self):
        return Reservation.objects.all()

    def perform_update(self, serializer):
        reservation = serializer.save(status='cancelled')
        print(f"[DEBUG] Cancelled reservation: ID={reservation.reservation_id}, contact={reservation.contact}")

        # Notify the user
        user_subject = 'Your Reservation Has Been Cancelled'
        user_message = (
            f"Hello {reservation.contact},\n"
            f"Your reservation (ID: {reservation.reservation_id}) for {reservation.accommodation.name} has been cancelled.\n"
            "We hope to serve you again soon."
        )
        print(f"[DEBUG] Sending user cancellation email: subject={user_subject}, to={reservation.contact}")
        send_mail(user_subject, user_message, settings.DEFAULT_FROM_EMAIL, [reservation.contact], fail_silently=False)

        # Notify specialists
        for uni in reservation.accommodation.universities.all():
            support_email = uni.specialist_email.strip()
            print(f"[DEBUG] University {uni.code} specialist_email: '{support_email}'")
            support_subject = f"Reservation #{reservation.reservation_id} Cancelled"
            support_message = (
                f"A reservation has been cancelled:\n"
                f"• ID: {reservation.reservation_id}\n"
                f"• Property: {reservation.accommodation.name}\n"
                f"• Dates: {reservation.start_date} to {reservation.end_date}\n"
                f"• Contact: {reservation.contact}\n"
            )
            if support_email:
                print(f"[DEBUG] Sending specialist cancellation email: subject={support_subject}, to={support_email}")
                send_mail(support_subject, support_message, settings.DEFAULT_FROM_EMAIL, [support_email], fail_silently=False)
            else:
                print(f"--- Specialist Cancellation Notification for {uni.code} (no email configured) ---")
                print(f"Subject: {support_subject}")
                print(support_message)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# View all reservations
class ViewReservationList(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, ServiceTokenAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.all()

# View reserved accommodation detail
class ViewReservedAccommodationDetail(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, ServiceTokenAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = AccommodationSerializer
    lookup_url_kwarg       = 'pk'

    def get_object(self):
        reservation = get_object_or_404(Reservation, pk=self.kwargs['pk'])
        return reservation.accommodation
