from external_dependency import dark_magic


def is_credit_card_fraud(transaction):
    fraud_probability = dark_magic(transaction)
    if fraud_probability > 0.99:
        return True
    else:
        return False
