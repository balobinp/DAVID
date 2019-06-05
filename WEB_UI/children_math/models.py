from django.db import models

class Task01(models.Model):
    """Simple addition subtraction task"""
    user_id = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    first = models.FloatField()
    second = models.FloatField()
    sign = models.CharField(max_length=15)
    user_answer = models.FloatField()

    def __str__(self): # ChildrenMath.objects.all()
        return '{} {} {} {} {} {}'.format(self.user_id, self.date,
                                             self.first, self.sign, self.second, self.user_answer)
