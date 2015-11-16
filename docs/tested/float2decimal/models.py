from django.db import models

class A(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.DecimalField(max_digits=5, decimal_places=2)
    
    def total(self):
        return self.price * self.qty


