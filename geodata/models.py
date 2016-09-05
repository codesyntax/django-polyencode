from django.db import models
from django.utils.translation import ugettext as _

GEOTYPE_CHOICES = ((0, ''), (1, _('District / Neighborhood')), (2, _('Town / City')), (3, _('Valley / Region')), (4, _('Province')), (5, _('State')), (6, _('Country')))


class Place(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True, db_index=True)
    geotype = models.IntegerField(default=0, db_index=True, choices=GEOTYPE_CHOICES)
    notes = models.TextField(null=True, blank=True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child_set', on_delete=models.SET_NULL)

    added = models.DateField(_('Added'), auto_now_add=True)
    modified = models.DateField(_('Modified'), auto_now=True)

    def countChild(self):
        return self.child_set.all().count()

    def getChild(self):
        return self.child_set.all().order_by('name')

    def getPolygons(self):
        return self.polygon_set.all()

    def countPolygons(self):
        return self.polygon_set.all().count()

    def countPolygonsEx(self):
        return self.polygon_set.filter(is_exterior=True).count()

    def countPolygonsIn(self):
        return self.polygon_set.filter(is_exterior=False).count()

    def countPoints(self):
        total = 0
        for polygon in self.getPolygons():
            total = total + polygon.countPoints()
        return total

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class Polygon(models.Model):
    tokia = models.ForeignKey(Place)

    limits = models.TextField(null=True, blank=True)
    is_visible = models.BooleanField(default=1)
    is_exterior = models.BooleanField(default=1)

    encode_points = models.TextField(null=True, blank=True)
    encode_levels = models.TextField(null=True, blank=True)
    encode_zoomfactor = models.CharField(max_length=20, blank=True, null=True)
    encode_numlevels = models.CharField(max_length=20, blank=True, null=True)

    added = models.DateField(_('Added'), auto_now_add=True)
    modified = models.DateField(_('Modified'), auto_now=True)

    def getPoints(self):
        return tuple([tuple([float(b) for b in a.split(',')]) for a in self.limits.split(' ')])

    def countPoints(self):
        return len(self.limits.split(' '))

    class Meta:
        verbose_name = _('Polygon')
        verbose_name_plural = _('Polygons')

    def __unicode__(self):
        return u'%d' % self.pk
