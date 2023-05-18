from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import UserLoginForm, UserRegistrationForm
from .models import Ticket, TicketPurchase

def index(request):
    return render(request, 'ticketing/index.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'ticketing/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_mail(
                'Registration Successful!',
                'Congratulations! You have successfully registered for the ticketing platform.',
                'noreply@ticketingplatform.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('registration_success')
    else:
        form = UserRegistrationForm()
    return render(request, 'ticketing/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def free_ticket_view(request):
    if request.method == 'POST':
        ticket = Ticket.objects.create(user=request.user)
        send_mail(
            'Free Ticket Confirmation',
            f'Congratulations! You have received a free ticket with code: {ticket.code}',
            'noreply@ticketingplatform.com',
            [request.user.email],
            fail_silently=False,
        )
        return redirect('ticket', ticket_id=ticket.id)
    return render(request, 'ticketing/free_ticket.html')

@login_required
def buy_ticket_view(request):
    if request.method == 'POST':
        ticket_purchase = TicketPurchase.objects.create(user=request.user)
        send_mail(
            'Ticket Purchase Confirmation',
            f'Thank you for purchasing a ticket! Your ticket code is: {ticket_purchase.ticket.code}',
            'noreply@ticketingplatform.com',
            [request.user.email],
            fail_silently=False,
        )
        return redirect('ticket', ticket_id=ticket_purchase.ticket.id)
    return render(request, 'ticketing/buy_ticket.html')

@login_required
def ticket_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
   

@login_required
def ticket_confirmation(request, purchase_id):
    purchase = get_object_or_404(TicketPurchase, id=purchase_id, user=request.user)

    # Send email confirmation
    subject = 'Ticket Confirmation'
    message = f'Thank you for your purchase. Your ticket code is {purchase.ticket_code}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [request.user.email]
    send_mail(subject, message, from_email, recipient_list)

    context = {'purchase': purchase}
    return render(request, 'ticket_confirmation.html', context)