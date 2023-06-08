from django.shortcuts import redirect, get_object_or_404, render
from django.conf import settings
from shop.models import Product
from .cart import Cart
from .models import CartItem
from django.http import JsonResponse
from .models import Order, OrderItem
from .forms import CheckoutForm
from django.contrib import messages
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
from email.mime.text import MIMEText
from google.oauth2.service_account import Credentials

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    cart_items = sum(item['quantity'] for item in cart)
    return JsonResponse({"cart_total_items": cart_items})


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_items_count(request):
    cart = Cart(request)
    total_items = sum(item['quantity'] for item in cart)
    return JsonResponse({'cart_total_items': total_items})


def get_google_auth_credentials_from_service_account():
    creds = Credentials.from_service_account_file(os.path.join(settings.BASE_DIR, 'alayaptichkastore-20b2e4a72bf1.json'))
    return creds


def get_google_auth_credentials_from_pickle():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=8081)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def send_mail_with_gmail(sender, to, subject, message_text):
    creds = get_google_auth_credentials_from_service_account()
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return service.users().messages().send(userId="me", body={"raw": raw_message.decode("utf-8")}).execute()


def checkout(request):
    print(f"Checkout function called. Method: {request.method}")  # Debug line
    cart = Cart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            print(f"Form is valid")  # Debug line

            # extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']

            order = Order.objects.create(
                user=request.user,
                name=name,
                email=email,
                phone=phone,
                address=address,
                paid=False
            )

            if request.user.is_authenticated:
                print(f"Current user: {request.user}")  # Debug line
                order_items_str = ''
                total_cost = 0
                for item in cart:
                    print(
                        f"Creating OrderItem for product: {item['product']}, price: {item['price']}, quantity: {item['quantity']}")  # Debug line
                    OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
                    order_items_str += f"{item['product']} (Quantity: {item['quantity']}, Price: {item['price']})\n"
                    total_cost += item['price'] * item['quantity']

                # update user info
                request.user.name = name
                request.user.email = email
                request.user.phone = phone
                request.user.address = address
                request.user.save()

                # email sending
                try:
                    send_mail_with_gmail(
                        'alaya-ptichka@alayaptichkastore.iam.gserviceaccount.com',
                        request.user.email,
                        'Order Confirmation',
                        f'Thank you for your order.\n\nOrder details:\n{order_items_str}\nTotal cost: {total_cost}\n\nWe are processing your order and will email you once your items have been dispatched.\nFor payment, please contact us on Telegram at https://t.me/vermilioh.',
                    )
                except HttpError as error:
                    print(f'An error occurred while trying to send the email: {error}')

                cart.clear()
                return redirect('cart:confirmation')
            else:
                messages.error(request, 'You need to be logged in to complete the order.')
        else:
            messages.error(request, 'There was an error with the form. Please check your information and try again.')
    else:
        form = CheckoutForm()

    return render(request, 'cart/checkout.html', {'cart': cart, 'form': form})


def confirmation(request):
    last_order = Order.objects.filter(user=request.user).last()
    return render(request, 'cart/confirmation.html', {'order': last_order})


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def update_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity'))
    cart.update(product, quantity)
    return JsonResponse({"status": "ok"})




