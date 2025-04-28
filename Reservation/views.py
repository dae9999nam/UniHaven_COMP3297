from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings

from authentication.authentication import ServiceTokenAuthentication
from .models import Reservation
from .serializers import ReservationSerializer
from Accommodations.models import Accommodation
from Accommodations.serializers import AccommodationSerializer
from .forms import ReservationForm


# API endpoints scoped per university via service tokens
class CreateReservation(generics.ListCreateAPIView):
    authentication_classes = [ServiceTokenAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ReservationSerializer

    def get_queryset(self):
        uni = getattr(self.request.auth, 'university', None)
        qs = Reservation.objects.all()
        return qs.filter(accommodation__universities=uni) if uni else qs

    def perform_create(self, serializer):
        reservation = serializer.save()
        subject = 'Your Reservation Confirmation'
        message = (
            f"Hello {reservation.contact},\n"
            f"Your reservation (ID: {reservation.reservation_id}) "
            f"for {reservation.accommodation.name} is confirmed.\n"
            "Thank you for using UniHaven."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [reservation.contact],
            fail_silently=False,
        )


class ModifyReservation(generics.RetrieveUpdateAPIView):
    authentication_classes = [ServiceTokenAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ReservationSerializer
    lookup_field           = 'pk'

    def get_queryset(self):
        uni = getattr(self.request.auth, 'university', None)
        qs = Reservation.objects.all()
        return qs.filter(accommodation__universities=uni) if uni else qs


class CancelReservation(generics.RetrieveUpdateAPIView):  
    authentication_classes = [ServiceTokenAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ReservationSerializer
    lookup_field           = 'pk'

    def get_queryset(self):
        uni = getattr(self.request.auth, 'university', None)
        qs = Reservation.objects.all()
        return qs.filter(accommodation__universities=uni) if uni else qs

    def perform_update(self, serializer):
        reservation = serializer.save(status='cancelled')
        subject = 'Your Reservation Has Been Cancelled'
        message = (
            f"Hello {reservation.contact},\n"
            f"Your reservation (ID: {reservation.reservation_id}) "
            f"for {reservation.accommodation.name} has been cancelled.\n"
            "We hope to serve you again soon."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [reservation.contact],
            fail_silently=False,
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ViewReservationList(generics.ListAPIView):
    authentication_classes = [ServiceTokenAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ReservationSerializer

    def get_queryset(self):
        uni = getattr(self.request.auth, 'university', None)
        qs = Reservation.objects.all()
        return qs.filter(accommodation__universities=uni) if uni else qs


class ViewReservedAccommodationDetail(generics.RetrieveAPIView):
    authentication_classes = [ServiceTokenAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = AccommodationSerializer
    lookup_url_kwarg       = 'pk'

    def get_object(self):
        uni = getattr(self.request.auth, 'university', None)
        reservation = get_object_or_404(
            Reservation.objects.filter(accommodation__universities=uni),
            pk=self.kwargs['pk']
        )
        return reservation.accommodation


# Optional UI form-based views (no templates)

def reserve_accommodation(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.accommodation = accommodation
            reservation.save()
            subject = 'Your Reservation Confirmation'
            message = (
                f"Hello {reservation.contact},\n"
                f"You have successfully reserved {accommodation.name}.\n"
                f"Reservation ID: {reservation.reservation_id}"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [reservation.contact],
                fail_silently=False,
            )
            return redirect('reservation_success')
    else:
        form = ReservationForm()
    return HttpResponse("Reservation form page (no template).")


def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        subject = 'Your Reservation Has Been Cancelled'
        message = (
            f"Hello {reservation.contact},\n"
            f"Your reservation (ID: {reservation.reservation_id}) has been cancelled."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [reservation.contact],
            fail_silently=False,
        )
        return redirect('cancellation_success')
    return HttpResponse("Cancellation form page (no template).")


def reservation_success(request):
    message = "Your reservation has been successfully created."
    print(message)
    return HttpResponse(message)


def cancellation_success(request):
    message = "Your reservation has been successfully cancelled."
    print(message)
    return HttpResponse(message)
