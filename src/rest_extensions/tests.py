import sys

from django.core.management.base import OutputWrapper
from django.core.management.color import color_style
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_extensions.fields import Color


out = OutputWrapper(sys.stdout)
style = color_style()
User = get_user_model()


def head(text):
    out.write(style.SQL_TABLE("# {}".format(text)))

def head1(text):
    out.write(style.MIGRATE_HEADING("## {}".format(text)))

def list1(text):
    out.write(style.SQL_FIELD("* {}".format(text)))

def list2(text):
    out.write(style.SQL_COLTYPE("    * {}".format(text)))

def info(text):
    out.write(style.HTTP_INFO(text))

def success(text):
    out.write(style.SUCCESS(text))


head("test rest_extensions")
class ColorFieldTestCase(TestCase):

    def setUp(self):
        head1("test ColorField")
        self.user = User.objects.create(username="testuser")

    def test_color_field(self):
        list1("test default color field")
        info(self.user.fav_color)
        self.assertEqual(self.user.fav_color, Color(255, 255, 255))
        list1("test save color")
        rand_color = Color.random()
        self.user.fav_color = rand_color
        self.user.save()
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.fav_color, rand_color)
        list1("test search color")
        rand_color = Color.random()
        User.objects.create(fav_color=rand_color)
        info(rand_color)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.filter(fav_color=rand_color).count(), 1)
