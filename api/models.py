from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ExerciseScore(models.Model):

    class ExerciseType(models.TextChoices):
        SCALE = 'scale', _('Scale')
        ARPEGGIO = 'arpeggio', _('Arpeggio')
        CHORD = 'chord', _('Chord')

    class Tonic(models.TextChoices):
        C = 'C'
        Db = 'Db'
        D = 'D'
        Eb = 'Eb'
        E = 'E'
        F = 'F'
        Fs = 'F#'
        G = 'G'
        Ab = 'Ab'
        A = 'A'
        Bb = 'Bb'
        B = 'B'

    class Mode(models.TextChoices):
        MAJOR = 'major', _('Major')
        MINOR = 'minor', _('minor')
        MIN_MEL = 'melod', _('melodic minor')
        MIN_HARM = 'harm', _('harmonic minor')
        CHROM = 'chrom', _('chromatic')
        WHOLE = 'whole', _('whole tone')

    class Inversion(models.TextChoices):
        ROOT = '0', _('root position')
        FIRST = '1', _('first inversion')
        SECOND = '2', _('second inversion')
        THIRD = '3', _('third inversion')

    class Interval(models.TextChoices):
        THIRD = '3rd', _('separated by a 3rd')
        SIXTH = '6th', _('separated by a 6th')

    class Motion(models.TextChoices):
        SIMILAR = 'sim', _('similar motion')
        CONTRARY = 'cont', _('contrary motion')

    type = models.CharField(12, choices=ExerciseType.choices)
    tonic = models.CharField(4, choices=Tonic.choices)
    mode = models.CharField(8, choices=Mode.choices)
    inversion = models.CharField(1, choices=Inversion.choices, null=True, blank=True)
    interval = models.CharField(1, choices=Interval.choices, null=True, blank=True)
    motion = models.CharField(1, choices=Motion.choices, default=Motion.SIMILAR)

    accuracy = models.FloatField()
    notes_per_minute = models.FloatField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    exercise_scores = models.ForeignKey(ExerciseScore, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + '\'s profile'

    def get_score(self):
        pass


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
