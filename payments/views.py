from django.shortcuts import render
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient

# Create your views here.
def stk_push_callback(request):
    if request.method == "GET":
        try:
            cl = MpesaClient()
            phone_number = "0715494857"
            amount = 1
            account_reference = "DL00001"
            transaction_desc = "Successful transaction"
            callback_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            return HttpResponse(response)

        except Exception as e:
        # Handle any exceptions that may occur during the STK push
            error_message = f"Error occurred during STK push: {str(e)}"
            return HttpResponse(error_message, status=500)
    else:
        return HttpResponse("Method not allowed", status=405)