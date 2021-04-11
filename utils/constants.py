from utils import file_reader
from datetime import datetime
from pytz import timezone

URL = "https://mint.intuit.com/updateTransaction.xevent"  # grab from POST request header in devtools
REFERER = "https://mint.intuit.com/transaction.event?accountId=https://mint.intuit.com/transaction.event"  # grab from POST request header in devtools
TOKEN = '66059787IDXhAG8MQ2hxcRXCQUJ1jxI682MZTzYRcISIYJA'  # grab from POST request form body in devtools

MINT_REQUEST_COOKIE = file_reader.read_cookies()
TODAY = datetime.now(tz=timezone("US/Pacific"))

# Define mapping of import categories to : Mint Category IDs
"""
    #################################
    Process Categories
    #################################

    Support is limited to the categories I needed at the time, if you need to map more you can. To get category ids:
    1. Go to mint
    2. Add a transactions
    3. Right click "inspect-element" on the category you want
    4. The ID is in the <li> item that encapsulates the a href
    5. Add mapping here based on string match from your CSV to the catID you got from mint (following existing examples)
"""
CATEGORY_TO_ID_MAPPING = {
    # Chase categories - incomplete
    'Gas': 1401,
    'Food & Drink': 7,
    'Health & Wellness': 5,
    'Personal': 4,
    'Automotive': 14,
    'Professional Services': 17,
    'Fees & Adjustments': 16,
    # American Express Categories - Incomplete
    # American Express doesn't provide category information for payments, so I recommend manually changing those to "Payment"
    'Merchandise & Supplies-Groceries': 701,
    'Transportation-Fuel': 1401,
    'Fees & Adjustments-Fees & Adjustments': 16,
    'Merchandise & Supplies-Wholesale Stores': 2,
    'Restaurant-Restaurant': 707,
    'Payment': 2101,
    # The following categories are Mint categories.
    # Citi does not included categories in downloaded transactions so I added my own categories using the Mint categories.
    # These mappings make sure those categories don't get mapped to 'uncategorized:20' when they aren't found in the mappings
    # for the other banks above.
    #
    # If you want to change a category mapping, be mindful that some category names may be repeated because Mint uses
    # the same category name as another bank.
    'Auto & Transport': 14,
    'Auto Insurance': 1405,
    'Auto Payment': 1404,
    'Gas & Fuel': 1401,
    'Parking': 1402,
    'Public Transportation': 1406,
    'Service & Parts': 1403,
    'Bills & Utilities': 13,
    'Home Phone': 1302,
    'Internet': 1303,
    'Mobile Phone': 1304,
    'Television': 1301,
    'Utilities': 1306,
    'Business Services': 17,
    'Advertising': 1701,
    'Legal': 1705,
    'Office Supplies': 1702,
    'Printing': 1703,
    'Shipping': 1704,
    'Education': 10,
    'Books & Supplies': 1003,
    'Student Loan': 1002,
    'Tuition': 1001,
    'Entertainment': 1,
    'Amusement': 102,
    'Arts': 101,
    'Movies & DVDs': 104,
    'Music': 103,
    'Newspapers & Magazines': 105,
    'Fees & Charges': 16,
    'ATM Fee': 1605,
    'Bank Fee': 1606,
    'Finance Charge': 1604,
    'Late Fee': 1602,
    'Service Fee': 1601,
    'Trade Commissions': 1607,
    'Financial': 11,
    'Financial Advisor': 1105,
    'Life Insurance': 1102,
    'Food & Dining': 7,
    'Alcohol & Bars': 708,
    'Coffee Shops': 704,
    'Fast Food': 706,
    'Groceries': 701,
    'Restaurants': 707,
    'Gifts & Donations': 8,
    'Charity': 802,
    'Gift': 801,
    'Health & Fitness': 5,
    'Dentist': 501,
    'Doctor': 502,
    'Eyecare': 503,
    'Gym': 507,
    'Health Insurance': 506,
    'Pharmacy': 505,
    'Sports': 508,
    'Home': 12,
    'Furnishings': 1201,
    'Home Improvement': 1203,
    'Home Insurance': 1206,
    'Home Services': 1204,
    'Home Supplies': 1208,
    'Lawn & Garden': 1202,
    'Mortgage & Rent': 1207,
    'Income': 30,
    'Bonus': 3004,
    'Interest Income': 3005,
    'Paycheck': 3001,
    'Reimbursement': 3006,
    'Rental Income': 3007,
    'Returned Purchase': 3003,
    'Kids': 6,
    'Allowance': 610,
    'Baby Supplies': 611,
    'Babysitter & Daycare': 602,
    'Child Support': 603,
    'Kids Activities': 609,
    'Toys': 606,
    'Misc Expenses': 70,
    'Personal Care': 4,
    'Hair': 403,
    'Laundry': 406,
    'Spa & Massage': 404,
    'Pets': 9,
    'Pet Food & Supplies': 901,
    'Pet Grooming': 902,
    'Veterinary': 903,
    'Shopping': 2,
    'Books': 202,
    'Clothing': 201,
    'Electronics & Software': 204,
    'Hobbies': 206,
    'Sporting Goods': 207,
    'Taxes': 19,
    'Federal Tax': 1901,
    'Local Tax': 1903,
    'Property Tax': 1905,
    'Sales Tax': 1904,
    'State Tax': 1902,
    'Transfer': 21,
    'Credit Card Payment': 2101,
    'Transfer for Cash Spending': 2102,
    'Travel': 15,
    'Air Travel': 1501,
    'Hotel': 1502,
    'Rental Car & Taxi': 1503,
    'Vacation': 1504,
    'Uncategorized': 20,
    'Cash & ATM': 2001,
    'Check': 2002,
    'Hide from Budgets & Trends': 40,
}
