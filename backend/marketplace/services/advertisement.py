from django.contrib.auth.models import User

from marketplace.models import Advertisement


def approve_advertisement(approver: User, advertisement: Advertisement) -> bool:
    """Takes a user with admin privileges and an advertisement to
    approve on behalf of this user."""
    if approver.is_staff:
        advertisement.is_approved = True
        advertisement.save()
    return approver.is_staff
