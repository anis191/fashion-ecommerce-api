from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from .managers import UserManager

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
 
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
 
    objects = UserManager()
 
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
 
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]
 
    def __str__(self) -> str:
        return self.email
 
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

class Address(BaseModel):
    class AddressType(models.TextChoices):
        SHIPPING = "shipping", _("Shipping")
        BILLING = "billing", _("Billing")
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    address_type = models.CharField(
        max_length=10,
        choices=AddressType.choices,
        default=AddressType.SHIPPING,
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")
        ordering = ["-is_default", "-created_at"]
    
    def __str__(self) -> str:
        return f"{self.full_name} — {self.street_address}, {self.city}"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(
                user=self.user,
                address_type=self.address_type,
                is_default=True,
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
 
