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


class IrregularVerbsResults(models.Model):
    user_id = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    verb_id = models.IntegerField()
    user_answer = models.CharField(max_length=255)

    def __str__(self):
        return '{} {} {} {}'.format(self.user_id, self.date, self.verb_id, self.user_answer)
