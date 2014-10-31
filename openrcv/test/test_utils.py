
import sys

from openrcv.utils import ObjectExtension, ReprMixin, StringInfo, UncloseableFile
from openrcv.utiltest.helpers import UnitCase


class ReprMixinTest(UnitCase):

    class ReprSample(ReprMixin):

        def repr_desc(self):
            return "foo"

    def test_repr(self):
        obj = ReprMixin()
        expected = "<ReprMixin: [--] %s>" % hex(id(obj))
        self.assertEqual(repr(obj), expected)

    def test_repr__implemented(self):
        obj = ReprMixinTest.ReprSample()
        expected = "<ReprSample: [foo] %s>" % hex(id(obj))
        self.assertEqual(repr(obj), expected)


class ObjectExtensionTests(UnitCase):

    class Foo(object):
        def value(self):
            return 3

    class FooExtension(ObjectExtension):
        def value(self):
            return 4

    def test_repr(self):
        """Check that existing methods are inherited."""
        obj = self.Foo()
        ext = ObjectExtension(obj)
        start = "<ObjectExtension: [object=<openrcv.test.test_utils.ObjectExtensionTests.Foo object"
        self.assertTrue(repr(ext).startswith(start))

    def test_inheritance(self):
        """Check that existing methods are inherited."""
        obj = self.Foo()
        ext = ObjectExtension(obj)
        self.assertEqual(ext.value(), 3)

    def test_overriding(self):
        """Check that existing methods can be overridden."""
        obj = self.Foo()
        ext = self.FooExtension(obj)
        self.assertEqual(ext.value(), 4)


class UncloseableFileTests(UnitCase):

    def test_standard_stream(self):
        """Test that closing a standard stream doesn't do anything when wrapped."""
        # It's better to test with sys.stdout than with sys.stderr,
        # because if the test fails with sys.stderr, then we won't see
        # any of the test output from that point on.
        f = UncloseableFile(sys.stdout)
        self.assertFalse(f.closed)
        f.close()
        self.assertFalse(f.closed)


class StringInfoTest(UnitCase):

    def test_init(self):
        stream = StringInfo("abc")
        self.assertEqual(stream.value, "abc")

    def test_init__no_args(self):
        stream = StringInfo()
        self.assertEqual(stream.value, None)

    def test_open__read(self):
        stream = StringInfo("abc")
        with stream.open() as f:
            out = f.read()
        self.assertEqual(out, "abc")
        # The value is also still available as an attribute.
        self.assertEqual(stream.value, "abc")

    def test_open__write(self):
        stream = StringInfo()
        with stream.open("w") as f:
            f.write("abc")
        # The value can be obtained from the attribute.
        self.assertEqual(stream.value, "abc")

    def test_open__write__non_none(self):
        """Test writing to a StringInfo initialized to a string."""
        stream = StringInfo()
        stream.value = ""  # Even an empty string triggers the ValueError.
        with self.assertRaises(ValueError):
            stream.open("w")
