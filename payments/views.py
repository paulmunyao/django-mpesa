from django.http import HttpResponse
import json
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
            client = MpesaClient()
            party_a = request.GET["phone_number"]
            amount = int(request.GET["amount"])
            account_reference = "iLAB Africa Digital Learning"
            transaction_desc = "Your transaction is successful"
            callback_url = (
                "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            )
            response = client.stk_push(
                party_a,
                amount,
                account_reference,
                transaction_desc,
                callback_url,
            )
            return HttpResponse(response)

        except Exception as e:
            # Handle any exceptions that may occur during the STK push
            error_message = f"Error occurred during STK push: {str(e)}"
            return HttpResponse(error_message, status=500)
    else:
        return HttpResponse("Method not allowed", status=405)

def callback(request):
    if request.method == "GET":
        try:
            # Extracting necessary parameters from the callback request
            client = MpesaClient()
            party_a = request.GET["phone_number"]
            amount = int(request.GET["amount"])
            account_reference = ["account_reference"]
            transaction_desc = ["transaction_desc"]
            result = {
                "Body":{
                    "stkCallback":{
                        "ResultCode":"0",
                        "ResultDesc":"Request successful",
                        "MerchantRequestID":"123456",
                        "CheckoutRequestID":"789012",
                        "CallbackMetadata": {
                            "Item": [
                                {"Name": "party_a", "Value": party_a},
                                {"Name": "amount", "Value": amount},
                                {"Name": "account_reference", "Value": account_reference},
                                {"Name": "transaction_desc", "Value": transaction_desc},
                            ]
                        }
                    }
                }
            }
            result_json = json.dumps(result)
            response = client.parse_stk_result(result_json)
            return HttpResponse(response)

        except Exception as e:
            # Handle any exception that may occur during the callback request
            error_message = f"Error occurred during callback: {str(e)}"
            return HttpResponse(error_message, status=500)
    else:
        return HttpResponse("Method not allowed", status=405)
