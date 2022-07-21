from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=300)
    logo = models.ImageField(upload_to='brand')


class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    backdrop_image = models.ImageField(upload_to='category')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    main_category = models.ForeignKey('products.MainCategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    backdrop_image = models.ImageField(upload_to='category')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=300)
    brand = models.ForeignKey('products.Brand', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey('products.SubCategory', on_delete=models.CASCADE)
    backdrop_image = models.ImageField(upload_to='product/%Y-%m')
    price = models.IntegerField()


class ProductSale(models.Model):
    product = models.OneToOneField('products.Product', on_delete=models.CASCADE)
    discounted_price = models.IntegerField()
    sale_ratio = models.IntegerField(default=0)


class ProductOption(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=4)
    count = models.IntegerField(default=0)


class ProductImages(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    kind = models.CharField(max_length=10)
    image = models.ImageField(upload_to='product/images/%Y-%m')

