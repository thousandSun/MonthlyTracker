import json

"""JSON object will look like this
    [
        {"expense": value, "amount": value, "total": value, "remaining": value, "complete": False, "paid": value}
    ]
"""

bills_file = "bills.json"


def create_file():  # just makes sure json file is there when it first runs
    try:
        with open(bills_file, 'x') as file:
            json.dump([], file)
    except FileExistsError:
        pass


def show_payments():
    bills = _get_bills()

    for bill in bills:
        bill_name = bill['expense']
        if not bill['complete']:
            bill_total = bill['total']
            bill_amount = bill['amount']
            bill_remaining = bill['remaining']
            paid = bill['paid']
            bill_string = f"| {bill_name.title()}: Total: ${bill_total:,.2f} Payment amount: ${bill_amount:,.2f} " \
                          f"Remaining: ${bill_remaining:,.2f} Paid to date: ${paid:,.2f} |"
            print("-"*(len(bill_string)))
            print(bill_string)
            print("-"*(len(bill_string)))
        else:
            payment_string = f"| {bill_name.title()}: PAID IN FULL |"
            print("-"*len(payment_string))
            print(payment_string)
            print("-"*len(payment_string))


def process_payment(expense, amount):
    index, bill = _get_bill(expense)

    if bill is not None:
        if not bill['complete']:
            bill['remaining'] -= amount
            bill['paid'] += amount
            bill['amount'] = amount
            if bill['remaining'] <= 0:
                bill['complete'] = True
            print('Payment successful')
            _update_and_write(bill, index)


def quick_pay(expense):
    index, bill = _get_bill(expense)

    if bill is not None:
        if not bill['complete']:
            bill['remaining'] -= bill['amount']
            bill['paid'] += bill['amount']
            if bill['remaining'] <= 0:
                bill['complete'] = True
            print('payment successful')
            _update_and_write(bill, index)
    else:
        print("!! Expense not found !!\n")


def add_expense(expense, amount, total):
    bills = _get_bills()
    bills.append(
        {
            "expense": expense,
            "amount": amount,
            "total": total,
            "remaining": total,
            "complete": False,
            "paid": 0.0
        }
    )
    _write_file(bills)


def remove(expense):
    bills = _get_bills()
    bills = [bill for bill in bills if bill["expense"] != expense]

    _write_file(bills)


def find_bill(bill_name):
    bills = _get_bills()
    return any(bill['expense'] == bill_name for bill in bills)


def _write_file(bills):
    with open(bills_file, 'w') as file:
        json.dump(bills, file)


def _get_bills():
    with open(bills_file, 'r') as file:
        return json.load(file)


def _get_bill(expense):
    bills = _get_bills()

    for i, bill in enumerate(bills):
        if bill['expense'] == expense:
            return i, bill

    return None, None


def _update_and_write(bill, index):
    bills = _get_bills()
    bills[index] = bill

    _write_file(bills)
