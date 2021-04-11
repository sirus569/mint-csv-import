"""
#################################
Pre-requisites needed
#################################

If you are missing any of the following you can install with:

	pip install $name
	Example: pip install csv 

OR if you are using pip3

	pip3 install $name 
	Example: pip3 install csv 
"""

import random
import time
import csv_importer
import mint
"""
#################################
Overview: 
#################################

Simulates bulk manual transaction adds to mint.com. Mint manual transactions are submitted as "cash transactions" which 
will mean it shows in your cash / all accounts transaction list. You cannot submit manual transactions against credit 
cards or other integrated bank accounts (even in Mint's UI this is not possible and ends up as cash transction). 

Approach Credits: 
Simulating manual transactions from UI is based on Nate H's proof of concept from https://www.youtube.com/watch?v=8AJ3g5JGmdU

Python Credits:
Credit to https://github.com/ukjimbow for his work on Mint imports for UK users in https://github.com/ukjimbow/mint-transactions

Process Documentation: 
1. Import CSV
2. Process date for correct format and HTTP encode result 
3. Process merchant for HTTP encode
4. Process categories change your banks category name into a mint category ID (limited in scope based on the categories
5 needed when I wrote this)
6. Process amount for positive or negative value indicating income or expense 
7. Send POST Request to mint as new transaction. 
8. Force Randomized Wait Time before starting next request

Future Development:
1. Replace curl command string generation with parametized curl class constructor 
2. Add support for the rest of the manual transaction items

"""

"""
#################################
Settings 
#################################
"""
min_wait = 0  # min wait time in seconds between requests, int[0-n]
max_wait = 2  # max wait time in seconds between requests, int[0-n]


"""
#################################
Import CSV using the pythons csv reader 
#################################
"""


def run(csv_name: str) -> None:
	for transaction in csv_importer.read_file(csv_name):

		if not mint.add_transaction(transaction, use_requests=True, make_request=True):
			raise Exception(
				f"MintImportException: {transaction.transaction_date} | {transaction.merchant} | {transaction.amount}")

		"""
		#################################
		Force a random wait between 2 and 5 seconds per requests to simulate UI and avoid rate limiting
		#################################
		"""
		time.sleep(random.randint(min_wait, max_wait))


if __name__ == "__main__":
	run("test-2021.csv")
