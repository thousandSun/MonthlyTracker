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
            payment_string = f"| {payment_name.title()}: PAID IN FULL |"
            print("-"*len(payment_string))
            print(payment_string)
            print("-"*len(payment_string))


def process_payment(expense, amount):
    index, payment = _get_bill(expense)

    if payment is not None:
        if not payment['complete']:
            payment_remaining = payment['remaining']
            payment_paid = payment['paid']

            payment_remaining -= amount
            payment_paid += amount
            payment['amount'] = amount
            if payment_remaining <= 0:
                payment['complete'] = True
            else:
                payment['remaining'] = payment_remaining
                payment['paid'] = payment_paid
            print('Payment successful')
        else:
            print("!! Ezpense not found !!")
    _update_and_write(payment, index)


def quick_pay(expense):
    index, payment = _get_bill(expense)

    if payment is not None:
        if not payment['complete']:
            payment_amount = payment['amount']
            payment_remaining = payment['remaining']
            payment_paid = payment['paid']

            payment_remaining -= payment_amount
            payment_paid += payment_amount
            if payment_remaining <= 0:
                payment['complete'] = True
            else:
                payment['remaining'] = payment_remaining
                payment['paid'] = payment_paid
            print('payment successful')
        else:
            print("!! Expense not found !!")
    _update_and_write(payment, index)


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


def _get_bill(expense):
    payments = _get_payments()

    for i, payment in enumerate(payments):
        if payment['expense'] == expense:
            return i, payment
    return None


def find_bill(bill):
    payments = _get_payments()
    # print(payments)
    return any(payment['expense'] == bill for payment in payments)


def _update_and_write(payment, index):
    payments = _get_payments()
    payments[index] = payment

    _write_file(payments)


"""quick_pay(): found = False
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
"""
"""process_payment():  payments = _get_payments()
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
"""
