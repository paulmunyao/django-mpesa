from django.shortcuts import render
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient

# Create your views here.
"""
Handles the STK push callback from the Safaricom M-Pesa API.

This view function is responsible for processing the STK push callback from the Safaricom M-Pesa API. It receives the callback request, extracts the necessary information, and returns a response to the API.

The function first checks if the request method is GET, as this is the expected method for the callback. It then creates an instance of the MpesaClient class, sets the necessary parameters for the STK push (phone number, amount, account reference, transaction description, and callback URL), and initiates the STK push using the stk_push method of the MpesaClient.

If the STK push is successful, the function returns the response from the API. If an exception occurs during the process, the function handles the exception and returns an error message with a 500 status code.
"""


def stk_push_callback(request):
    if request.method == "GET":
        try:
            cl = MpesaClient()
            party_a = request.GET["phone_number"]
            amount = int(request.GET["amount"])
            account_reference = "iLAB Africa Digital learning"
            transaction_desc = "Successful transaction"
            callback_url = (
                "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            )
            response = cl.stk_push(
                party_a, amount, account_reference, transaction_desc, callback_url
            )
            return HttpResponse(response)

        except Exception as e:
            # Handle any exceptions that may occur during the STK push
            error_message = f"Error occurred during STK push: {str(e)}"
            return HttpResponse(error_message, status=500)
    else:
        return HttpResponse("Method not allowed", status=405)