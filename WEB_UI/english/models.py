from django.db import models

class IrregularVerbs(models.Model):
    infinitive = models.CharField(max_length = 50)
    past = models.CharField(max_length = 50)
    participle = models.CharField(max_length=50)
    translation = models.CharField(max_length=50)
    def __str__(self): # Здесь определяется что будет выводиться на Post.objects.all()
        return self.infinitive
    def get_all_fields(self):
        return '{},{},{},{}'.format(self.infinitive, self.past, self.participle, self.translation)
