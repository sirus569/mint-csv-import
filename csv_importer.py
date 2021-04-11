from csv import DictReader
from typing import List
import pathlib
from dataclasses import dataclass
from urllib import parse
from utils.constants import CATEGORY_TO_ID_MAPPING


@dataclass
class Transaction:
    amount: float
    category: str
    post_date: str
    transaction_date: str
    description: str
    merchant: str
    type_: str

    @property
    def url_transaction_date(self) -> str:
        dateoutput = self.transaction_date.replace("/", "%2F")
        dateoutput = dateoutput.replace(".", "%2F")
        dateoutput = dateoutput.replace("-", "%2F")
        return dateoutput

    @property
    def url_merchant(self) -> str:
        return parse.quote(self.merchant)

    @property
    def category_id(self) -> str:
        if not (self.category or len(self.category)):
            print(f"Can't find categoryID {self.category}")
            return '20'  # mint's uncategorized category

        return str(CATEGORY_TO_ID_MAPPING.get(self.category, 20))

    @property
    def url_category(self) -> str:
        return parse.quote(self.category)

    @property
    def is_expense(self) -> str:
        return 'false' if self.amount < 0 else 'true'

    @property
    def url_amount(self) -> str:
        return str(self.amount)


def read_file(csv_name: str) -> List:
    current_path = pathlib.Path(__file__).parent.absolute()
    absolute_path = pathlib.Path().joinpath(
        current_path,
        "apple_transactions",
        csv_name
    )
    lines = []
    with open(absolute_path, 'r') as theFile:
        reader = DictReader(theFile)
        for line in reader:
            new_line = {}
            new_line["transaction_date"] = line["Transaction Date"]
            new_line["post_date"] = line["Clearing Date"]
            new_line["type_"] = line["Type"]
            new_line["amount"] = float(line["Amount (USD)"])

            del line["Transaction Date"]
            del line["Clearing Date"]
            del line["Type"]
            del line["Amount (USD)"]

            for key, value in line.items():
                new_line[key.lower()] = value
            lines.append(Transaction(**new_line))

    return lines


if __name__ == "__main__":
    from pprint import pprint
    pprint(read_file("january-2021.csv"))
