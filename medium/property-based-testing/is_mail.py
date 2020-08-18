from email.utils import parseaddr


def is_email(potential_email_address: str) -> bool:
    context, mail = parseaddr(potential_email_address)
    first_condition = len(context) == 0
    dot_after_at = (
        "@" in potential_email_address and "." in potential_email_address.split("@")[1]
    )
    return first_condition and dot_after_at
