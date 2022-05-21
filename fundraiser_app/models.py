from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    choices_type = (
        ('Fundacja', 'Fundacja'),
        ('Organizacja pozarządowa', 'Organizacja pozarządowa'),
        ('Zbiórka lokalna', 'Zbiórka lokalna'),
    )
    type = models.CharField(max_length=64, choices=choices_type, default='Fundacja')
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'

    def __str__(self):
        return self.name

    def list_of_categories(self):
        categories = ', '.join([item.name for item in self.categories.all()])
        return categories


class Donation(models.Model):
    quantity = models.PositiveSmallIntegerField(verbose_name= 'Liczba worków')
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name= ' Instytucja')
    address_street_no = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models. TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_taken = models.BooleanField(default=False)
