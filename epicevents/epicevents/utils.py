from typing import Union
from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import User, Client


def get_id_by_email(email: str) -> Union[int, None]:
    try:
        return User.objects.get(email=email).id
    except ObjectDoesNotExist:
        try:
            return Client.objects.get(email=email).id
        except ObjectDoesNotExist:
            raise ValidationError("email does not exists.")
