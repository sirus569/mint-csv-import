import requests
from requests.structures import CaseInsensitiveDict
from csv_importer import Transaction
import os
from utils.constants import MINT_REQUEST_COOKIE, TODAY, REFERER, TOKEN, URL


"""
#################################
Mint Client Credentials 
#################################

You will need the tags, cookie, and token to simulate a UI form submission. 
You can get these by opening developer tools > network analysis tab and doing a test submission in mint.com. 
From there look for the post request to "updateTransaction.xevent" and grab the credentials from the header and body
"""
account = "7031494"  # grab from POST request form body in devtools
tags = ["tag1563540",
        "tag1573359",
        "tag1575078",
        "tag1563542",
        "tag1563541",
        "tag1576236",
        "tag1563549",
        "tag1563543",
        "tag1563548",
        "tag1563546",
        "tag1563547",
        "tag1574257",
        "tag1576349",
        "tag180047",
        "tag180048",
        "tag1564007",
        "tag1575079",
        "tag180049",
        "tag1571747"]


verbose_output = 1  # should verbose messages be printed [0,1]


def _curl(transaction: Transaction, make_call: bool) -> str:
    # Break curl lines
    curl_line = " "

    # fragment curl command
    curl_command = "curl -i -s -k -X POST 'https://mint.intuit.com/updateTransaction.xevent'" + curl_line
    curl_host = "-H 'Host: mint.intuit.com'" + curl_line
    curl_user_agent = "-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'" + curl_line
    curl_accept = "-H 'Accept: */*'" + curl_line
    curl_accept_language = "-H 'Accept-Language: en-US,en;q=0.5'" + curl_line
    curl_compressed = "--compressed" + curl_line
    curl_x_requested_with = "-H 'X-Requested-With: XMLHttpRequest'" + curl_line
    curl_content_type = "-H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8'" + curl_line
    curl_referer = "-H 'Referer: https://mint.intuit.com/transaction.event?accountId=" + REFERER + "'" + curl_line
    curl_cookie = "-H 'Cookie: " + MINT_REQUEST_COOKIE + "'" + curl_line
    curl_connection = "-H 'Connection: close' " + curl_line
    curl_data = "--data" + curl_line

    # Fragment the curl form data
    form_p1 = "'cashTxnType=on&mtCheckNo=&" + "=0&".join(tags) + "=0&"
    form_p2 = "task=txnadd&txnId=%3A0&mtType=cash&mtAccount=" + account + "&symbol=&note=&isInvestment=false&"
    form_p3 = "catId=" + transaction.category_id + "&category=" + transaction.url_category + "&merchant=" + transaction.url_merchant + "&date=" + transaction.url_transaction_date + "&amount=" + transaction.url_amount + "&mtIsExpense=" + transaction.is_expense + "&mtCashSplitPref=1&mtCashSplit=on&"
    form_p4 = "token=" + TOKEN + "'"

    # Piece together curl form data
    curl_form = form_p1 + form_p2 + form_p3 + form_p4

    # Combine all curl fragments together into an entire curl command
    curl_input = curl_command + curl_host + curl_user_agent + curl_accept + curl_accept_language + curl_compressed + curl_x_requested_with + curl_content_type + curl_referer + curl_cookie + curl_connection + curl_data + curl_form

    """
    #################################
    Submit CURL POST Request
    #################################
    """
    print('CURL Request:', curl_input)  # what was sent to mint
    if make_call:
        curl_output = str(os.system(curl_input))  # use os sytem to run a curl request submitting the form post
    else:
        curl_output = "<None yet>"

    return curl_output


def _requests(transaction: Transaction, make_request: bool) -> bool:

    data = {"cashTxnType": "on", "mtCheckNo": "", "tag1563540": 0,
            "task": "txnadd", "txnId": "%3A0", "mtType": "cash",
            "mtAccount": account, "symbol": "", "note": f"Entered via mint script on {TODAY}", "isInvestment": "false", "catId": transaction.category_id,
            "category": transaction.url_category, "merchant": transaction.url_merchant,
            "date": transaction.url_transaction_date, "amount": transaction.url_amount,
            "mtIsExpense": transaction.is_expense, "mtCashSplitPref": "1", "mtCashSplit": "on", "token": TOKEN}

    for tag in tags:
        data[tag] = "0"

    headers = CaseInsensitiveDict()
    headers["Host"] = "mint.intuit.com"
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    headers["Accept"] = "*/*"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["X-Requested-With"] = "XMLHttpRequest"
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    headers["Referer"] = REFERER
    headers["Cookie"] = MINT_REQUEST_COOKIE
    headers["Connection"] = "close"

    data = "&".join([f"{key}={value}" for key, value in data.items()])

    if make_request:
        resp = requests.post(URL, headers=headers, data=data)
        if resp.status_code // 100 != 2 or "INTERNAL_ERROR" in resp.text:
            return False
        return resp.status_code

    return True


def add_transaction(transaction: Transaction, use_requests: bool = False, make_request: bool = False) -> bool:
    if use_requests:
        curl_output = _requests(transaction, make_request)
    else:
        curl_output = _curl(transaction, make_request)

    """
    #################################
    Verbose Output for Debug
    #################################
    """
    if verbose_output == 1:
        print('Transaction Date:', transaction.url_transaction_date)  # date of transaction
        print('Merchant', transaction.url_merchant)  # merchant Description
        print('Category ID:', transaction.category_id)  # category of transaction
        print('Category Name:', transaction.url_category)  # category of transaction
        print('Amount:', transaction.url_amount)  # amount being processed
        print('Expense:', transaction.is_expense)  # in amount expense
        print('CURL Response:', curl_output)  # what was returned from mint OR curl ERROR
        print('\n\n==============\n')  # new line break

    return curl_output
