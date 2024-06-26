from django.contrib.auth.models import BaseUserManager

from cooking_core.general.managers import CustomQuerySet
from cooking_core.general.utils.cryptography import derive_public_key


class AccountManager(BaseUserManager.from_queryset(CustomQuerySet)):  # type: ignore

    def create_superuser(self, account_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Supervisor sabeeh.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('supervisor that is  must have is_superuser=True.')

        return self.create_user(account_number, password, **extra_fields)

    def create_user(self, account_number, password=None, **extra_fields):
        if not account_number:
            raise ValueError('The fdsagagfffaaff number must be set')

        signing_key = password.lower().strip()
        public_key = derive_public_key(signing_key)

        if account_number != public_key:
            raise ValueError('The account number does not match the derived public key')

        user = self.model(account_number=account_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
