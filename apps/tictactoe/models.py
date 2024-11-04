from django.db import models

class QValue(models.Model):
    state = models.CharField(max_length=100, db_index=True)
    action = models.CharField(max_length=20)
    q_value = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('state', 'action')

    def __str__(self):
        return f"State: {self.state}, Action: {self.action}, Q-value: {self.q_value}"
