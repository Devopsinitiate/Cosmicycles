from django.test import SimpleTestCase
from django.template import Template, Context


class CustomFilterTests(SimpleTestCase):
    def test_color_hex(self):
        t = Template("{% load custom_filters %}{{ 'blue'|color_hex:'500' }}")
        out = t.render(Context({}))
        self.assertIn("#", out)

    def test_color_hex_unknown(self):
        t = Template("{% load custom_filters %}{{ 'unknown'|color_hex:'500' }}")
        out = t.render(Context({}))
        self.assertEqual(out, "#f9fafb")

    def test_div(self):
        t = Template("{% load custom_filters %}{{ 10|div:3 }}")
        out = t.render(Context({}))
        self.assertAlmostEqual(float(out), 3.333, places=2)

    def test_div_by_zero(self):
        t = Template("{% load custom_filters %}{{ 10|div:0 }}")
        out = t.render(Context({}))
        self.assertEqual(out, "0")

    def test_mul(self):
        t = Template("{% load custom_filters %}{{ 5|mul:3 }}")
        out = t.render(Context({}))
        self.assertEqual(out, "15")

    def test_sub(self):
        t = Template("{% load custom_filters %}{{ 10|sub:3 }}")
        out = t.render(Context({}))
        self.assertEqual(out, "7")


class RenderHelpersTests(SimpleTestCase):
    def test_render_recommendations_none(self):
        t = Template(
            "{% load render_helpers %}{% render_recommendations val %}"
        )
        out = t.render(Context({"val": None}))
        self.assertEqual(out, "")

    def test_render_recommendations_dict(self):
        data = '{"Focus": ["Meditate", "Exercise"]}'
        t = Template(
            "{% load render_helpers %}{% render_recommendations val %}"
        )
        out = t.render(Context({"val": data}))
        self.assertIn("Focus", out)
        self.assertIn("Meditate", out)
        self.assertIn("Exercise", out)

    def test_render_recommendations_semicolon(self):
        t = Template(
            "{% load render_helpers %}{% render_recommendations val %}"
        )
        out = t.render(Context({"val": "Meditate; Exercise"}))
        self.assertIn("Meditate", out)
        self.assertIn("Exercise", out)
