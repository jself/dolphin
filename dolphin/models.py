from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField

from dolphin import settings
from dolphin.backends import redisbackend

class RedisModel(models.Model):
    def save(self, *args, **kwargs):
        from ipdb import set_trace; set_trace()
        schema = redisbackend.RedisSchema(self.__dict__)
        backend = redisbackend.RedisBackend()

class FeatureFlag(models.Model):
    name = models.SlugField(max_length=255, unique=True, db_index=True)
    enabled = models.BooleanField(blank=True, default=False, help_text="Flag is in use, if unchecked will be disabled altogether", db_index=True)

    #users
    registered_only = models.BooleanField(blank=True, default=False, help_text="Limit to registered users")
    staff_only = models.BooleanField(blank=True, default=False, help_text="Limit to staff users")
    limit_to_users = models.BooleanField(blank=True, default=False, help_text="Limit to specific users")
    users = models.ManyToManyField(User, blank=True) #TODO - do we want this to be many to many? possibly comma delimited charfield or something

    #geolocation
    enable_geo = models.BooleanField(blank=True, default=False, help_text="Enable geolocation")
    center = GeopositionField(null=True)
    radius = models.FloatField(blank=True, null=True, help_text="Distance in miles") #TODO - allow km/meters/etc

    #A/B testing stuff
    random = models.BooleanField(blank=True, default=False, help_text="Randomized A/B testing")
    maximum_b_tests = models.IntegerField(default=0, help_text="Maximum number of B tests, leave at 0 for infinite")
    current_b_tests = models.IntegerField(default=0, editable=True, help_text="Only updated if maximum_b_tests is set, updated once per view")
    b_test_start = models.DateTimeField(blank=True, null=True, db_index=True, help_text = "Optional start date/time of B tests")
    b_test_end = models.DateTimeField(blank=True, null=True, db_index=True, help_text = "Option end date/time of B tests")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if settings.DOLPHIN_USE_REDIS:
            from ipdb import set_trace; set_trace()
        return super(FeatureFlag, self).save(*args, **kwargs)


