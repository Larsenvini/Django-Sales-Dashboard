from django.db import models

class Venda(models.Model):
    data_venda = models.DateField(default='1970-01-01')  # Default date
    produto = models.CharField(max_length=100, default='Unknown Product')  # Default product name
    quantidade = models.IntegerField(default=0)  # Default quantity
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, db_column='preço')  # Default price
    regiao = models.CharField(max_length=100, default='Unknown Region')  # Default region
    vendedor = models.CharField(max_length=100, default='Unknown Seller')  # Default seller
    total_vendas = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Default total sales

    def __str__(self):
        return f"{self.produto} sold by {self.vendedor} on {self.data_venda}"
