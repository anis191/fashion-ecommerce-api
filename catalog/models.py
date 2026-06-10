from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
 
from core.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="categories/", null=True, blank=True
    )
    is_active = models.BooleanField(default=True, db_index=True)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["sort_order", "name"]
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def full_path(self) -> str:
        path = [self.name]
        node = self

        while node.parent_id:
            node = node.parent
            path.insert(0, node.name)
        
        return " > ".join(path)

class Brand(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, db_index=True
    )
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="brands/", null=True, blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class Attribute(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    display_type = models.CharField(
        max_length=20,
        choices=[
            ("select", "Select"),
            ("color", "Color Swatch"),
            ("text", "Text"),
        ],
        default="select"
    )

    class Meta:
        ordering = ["name"]
 
    def __str__(self) -> str:
        return self.name

class AttributeValue(BaseModel):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values",
    )

    value = models.CharField(max_length=100)
    display_value = models.CharField(max_length=100, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [("attribute", "value")]
        ordering = ["attribute", "sort_order", "value"]
    
    def __str__(self) -> str:
        return f"{self.attribute.name}: {self.value}"
    
 