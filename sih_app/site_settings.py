from django.db import models

class SiteSetting(models.Model):
    quote_update_interval = models.PositiveIntegerField(default=3600, help_text="Quote update interval in seconds")

    def __str__(self):
        return f"Site Settings (Quote interval: {self.quote_update_interval}s)"
