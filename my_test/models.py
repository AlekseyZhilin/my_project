from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name


class Items(models.Model):
    UNIT_MEASURE = (('шт', 'шт'), ('кг', 'кг'), ('м', 'м'))

    name = models.CharField(max_length=50, unique=True, db_index=True)
    unit_measurement = models.CharField(max_length=10, choices=UNIT_MEASURE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    is_product = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{self.name}, {self.unit_measurement}'


class Materials(models.Model):
    item = models.ForeignKey(Items, on_delete=models.PROTECT)
    count = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.item} {self.count}'


class Specification(models.Model):
    product = models.ForeignKey(Items, on_delete=models.PROTECT, related_name='spec_prod')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='spec_type')
    materials_table = models.ManyToManyField(Materials, related_name='tables')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{self.product}, {self.category}'
