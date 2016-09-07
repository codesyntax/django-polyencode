from django.db import models
from django.utils.translation import ugettext as _

GEOTYPE_CHOICES = ((0, ''), (1, _('District / Neighborhood')), (2, _('Town / City')), (3, _('Valley / Region')), (4, _('Province')), (5, _('State')), (6, _('Country')))


class Place(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True, db_index=True)
    geotype = models.IntegerField(verbose_name=_("Type"), default=0, db_index=True, choices=GEOTYPE_CHOICES)
    notes = models.TextField(verbose_name=_("Notes"), null=True, blank=True)
    lat = models.FloatField(verbose_name=_("Latitude"), default=0)
    lon = models.FloatField(verbose_name=_("Longitude"), default=0)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child_set', on_delete=models.SET_NULL, verbose_name=_("Parent"))

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
    place = models.ForeignKey(Place, verbose_name=_("Place"))

    limits = models.TextField(verbose_name=_("Limits"), null=True, blank=True)
    is_visible = models.BooleanField(verbose_name=_("Is visible"), default=1)
    is_exterior = models.BooleanField(verbose_name=_("Is exterior"), default=1)

    encode_points = models.TextField(verbose_name=_("Encode points"), null=True, blank=True)
    encode_levels = models.TextField(verbose_name=_("Encode levels"), null=True, blank=True)
    encode_zoomfactor = models.CharField(verbose_name=_("Encode zoom factor"), max_length=20, blank=True, null=True)
    encode_numlevels = models.CharField(verbose_name=_("Encode number levels"), max_length=20, blank=True, null=True)

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
