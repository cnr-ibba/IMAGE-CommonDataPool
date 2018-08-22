from django.db import models


class SampleInfo(models.Model):
    biosample_id = models.CharField(max_length=100, primary_key=True)
