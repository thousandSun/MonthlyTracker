import json

"""JSON object will look like this
    [
        {"expense": value, "amount": value, "total": value, "remaining": value, "complete": False, "paid": value}
    ]
"""

payment_file = "monthly.json"


def create_file():  # just makes sure json file is there when it first runs
    try:
        with open(payment_file, 'x') as file:
            json.dump([], file)
    except FileExistsError:
        pass


def show_payments():
    payments = _get_payments()

    for payment in payments:
        payment_name = payment['expense']
        if not payment['complete']:
            payment_total = payment['total']
            payment_amount = payment['amount']
            payment_remaining = payment['remaining']
            paid = payment['paid']
            payment_string = f"| {payment_name.title()}: Total: ${payment_total:,.2f} " \
                             f"Payment amount: ${payment_amount:,.2f} Remaining: ${payment_remaining:,.2f} " \
                             f"Paid to date: ${paid:,.2f} |"
            print("-"*(len(payment_string)))
            print(payment_string)
            print("-"*(len(payment_string)))
        else:
            payment_string = f"| {payment['expense']}: PAID IN FULL |"
            print("-"*len(payment_string))
            print(payment_string)
            print("-"*len(payment_string))


def process_payment(expense, amount):
    payments = _get_payments()
    found = False
    for payment in payments:
        if not payment['complete']:
            if payment['expense'] == expense:
                found = True
                payment['amount'] = amount
                remaining = payment['remaining']
                remaining -= amount
                payment['remaining'] = remaining
                paid = payment['paid']
                paid += amount
                payment['paid'] = paid
                remaining = payment['remaining']
                if remaining <= 0:
                    payment['complete'] = True
        else:
            print("Nothing to pay for this bill")
    if not found:
        print("!! Expense not found !!")
    _write_file(payments)


def quick_pay(expense):
    payments = _get_payments()
    found = False
    for payment in payments:
        if not payment['complete']:
            if payment['expense'] == expense:
                found = True
                remaining = payment['remaining']
                amount = payment['amount']
                paid = payment['paid']

                remaining -= amount
                paid += amount
                if remaining <= 0:
                    payment['complete'] = True
                else:
                    payment['remaining'] = remaining
                    payment['paid'] = paid
                print("Payment success")
        else:
            found = True
            print("Nothing to pay for this bill")

    if not found:
        print("!! Expense not found !!")

    _write_file(payments)


def add_expense(expense, amount, total):
    payments = _get_payments()
    payments.append(
        {
            "expense": expense,
            "amount": amount,
            "total": total,
            "remaining": total,
            "complete": False,
            "paid": 0.0
        }
    )
    _write_file(payments)


def remove(expense):
    payments = _get_payments()
    payments = [payment for payment in payments if payment["expense"] != expense]

    _write_file(payments)


def _write_file(payments):  # functions that start with _ are considered 'private' access modifier, devs know not to use
    with open(payment_file, 'w') as file:
        json.dump(payments, file)


def _get_payments():
    with open(payment_file, 'r') as file:
        return json.load(file)
