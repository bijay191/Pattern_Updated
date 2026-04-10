from django.db import models


class TableLog(models.Model):
    filename = models.CharField(max_length=500, unique=True)
    client = models.CharField(max_length=100)
    cuttingfloor = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.filename


class GeneratedPattern(models.Model):
    filename = models.CharField(max_length=500, unique=True)
    client = models.CharField(max_length=100)
    regex = models.CharField(max_length=500)

    def __str__(self):
        return self.filename


class PatternLayoutMapping(models.Model):
    payor = models.CharField(max_length=100)
    layout_id = models.IntegerField()
    datatype = models.CharField(max_length=100)
    employergroup = models.CharField(max_length=100)
    layouttype = models.CharField(max_length=100)
    pattern = models.CharField(max_length=500)
    cuttingfloor = models.CharField(max_length=500, null=True, blank=True)
    addeddate = models.DateField(auto_now_add=True)
    modifieddate = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.payor} - {self.layout_id}"