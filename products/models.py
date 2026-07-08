import uuid
from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from catalog.models import *

class Product(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        ACTIVE = "active", _("Active")
        ARCHIVED = "archived", _("Archived")
    
    class Gender(models.TextChoices):
        MEN = "men", _("Men")
        WOMEN = "women", _("Women")
        UNISEX = "unisex", _("Unisex")
        KIDS = "kids", _("Kids")
    
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True, db_index=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products",
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="products"
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=Status.choices,
        default=Status.DRAFT, db_index=True,
    )
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.UNISEX, db_index=True)
    tags = models.ManyToManyField("Tag", blank=True, related_name="products")
    care_instructions = models.TextField(blank=True)
    material = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_new_arrival = models.BooleanField(default=False, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "category"]),
            models.Index(fields=["status", "is_featured"]),
        ]
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if Product.objects.filter(slug = slug).exists():
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"
        self.slug = slug
        super().save(*args, **kwargs)

class Tag(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
 
    def __str__(self) -> str:
        return self.name
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ProductVariant(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    name = models.CharField(max_length=255, blank=True)
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    compare_at_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Original price before discount",
    )
    stock = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(
        default=5,
        help_text="Alert when stock falls below this value.",
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight in kg for shipping calculations.",
    )
    attribute_values = models.ManyToManyField(
        AttributeValue, blank=True, related_name="variants",
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("product variant")
        verbose_name_plural = _("product variants")
        ordering = ["product", "name"]
    
    def __str__(self) -> str:
        return f"{self.product.name} — {self.sku}"
    
    @property
    def effective_price(self):
        if self.price is not None:
            return self.price
        else:
            return self.product.base_price
    
    @property
    def is_low_stock(self)-> bool:
        return 0 < self.stock <= self.low_stock_threshold
    
    @property
    def is_in_stock(self) -> bool:
        return self.stock > 0
    
class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="images",
        help_text="Link this image to a specific variant (red,color,etc.)"
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")
        ordering = ["-is_primary", "sort_order"]
    
    def __str__(self) -> str:
        return f"Image for {self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(
                product = self.product,
                is_primary = True,
            ).exclude(pk = self.pk).update(is_primary = False)
        super().save(*args, **kwargs)
