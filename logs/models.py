from django.db import models


class Log(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200)
    telegram_id = models.CharField(blank=True, null=True, max_length=200)
    data = models.CharField(blank=True, null=True, max_length=200)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.telegram_id}  | {self.data} | {self.date}'
    class Meta:
        db_table = 'Log'


class Parts(models.Model):
    partname = models.CharField(db_column='PartName', unique=True, max_length=200)  # Field name made lowercase.

    def __str__(self):
        return self.partname

    class Meta:
        db_table = 'Parts'


class Cat(models.Model):
    category = models.CharField(db_column='Category', primary_key=True, max_length=200)  # Field name made lowercase.

    def __str__(self):
        return self.category

    class Meta:
        db_table = 'Cat'


class Model(models.Model):
    modelname = models.CharField(db_column='Modelname', unique=True, max_length=200)  # Field name made lowercase.
    modelcat = models.ForeignKey(Cat, models.DO_NOTHING, db_column='ModelCat')  # Field name made lowercase.

    def __str__(self):
        return self.modelname

    class Meta:
        db_table = 'Model'


class Partprice(models.Model):
    idmodel = models.ForeignKey(Model, models.DO_NOTHING, db_column='idModel')  # Field name made lowercase.
    idpart = models.ForeignKey('Parts', models.DO_NOTHING, db_column='idPart')  # Field name made lowercase.
    pricepart = models.CharField(db_column='pricePart', max_length=200)  # Field name made lowercase.
    pricestock = models.CharField(db_column="pricePartStock", max_length=200)
    description = models.CharField(blank=True, null=True, max_length=200)
    picture = models.TextField(blank=True, null=True)  # This field type is a guess.

    def __str__(self):
        return f'{self.idmodel.modelname} {self.idpart}'
    class Meta:
        db_table = 'PartPrice'
