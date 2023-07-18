from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Exercise(models.Model):
    pass


class Scale(Exercise):
    scale = models.CharField(6)


class Arpeggio(Exercise):
    chord = models.CharField(6)


class ChordExercise(Exercise):
    chord = models.CharField(6)


class ExerciseScore(models.Model):
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
