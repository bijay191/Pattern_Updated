from django.db import models

class FileName(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CentralizedPattern(models.Model):
    pattern = models.TextField()
    layout_id = models.IntegerField()

    def __str__(self):
        return f"{self.pattern} -> {self.layout_id}"


class GeneratedPattern(models.Model):
    file = models.ForeignKey(FileName, on_delete=models.CASCADE)
    suggested_pattern = models.TextField()
    generic_pattern = models.TextField()
    layout_id = models.IntegerField(null=True, blank=True)
    payer = models.CharField(max_length=20, null=True)
    data_type = models.CharField(max_length=20, null=True)
    file_format = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)