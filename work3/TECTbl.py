import unittest
import tempfile
from xmlparser import xm


class TestXm(unittest.TestCase):
    def setUp(self):
        self.xm_instance = xm()

    def test_parse_constant(self):
        self.assertAlmostEqual(float(self.xm_instance.parse_constant(".(+ 10 20).")), 30)
        self.assertAlmostEqual(float(self.xm_instance.parse_constant(".(- 20 10).")), 10)
        self.assertAlmostEqual(float(self.xm_instance.parse_constant(".(* 5 6).")), 30)
        self.assertAlmostEqual(float(self.xm_instance.parse_constant(".(/ 30 5).")), 6)
        self.assertAlmostEqual(float(self.xm_instance.parse_constant(".(min 10 20 5).")), 5)

    def test_parse_constant_invalid_expression(self):
        with self.assertRaises(SyntaxError):
            self.xm_instance.parse_constant("invalid expression")

    def test_resolve_constant(self):
        self.assertEqual(self.xm_instance._resolve_constant("42"), 42)
        self.assertEqual(self.xm_instance._resolve_constant('"Hello"'), "Hello")
        with self.assertRaises(ValueError):
            self.xm_instance._resolve_constant("UNDEFINED")

    def test_parse_xml(self):
        xml_content = """
        <root>
            <constant name="A">10</constant>
            <constant name="B">20</constant>
            <expression>.(+ A B).</expression>
        </root>
        """
        with tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
            temp_file.write(xml_content)
            temp_file_path = temp_file.name

        lines = self.xm_instance.parse_xml(temp_file_path)
        self.assertEqual(lines, ["30"])

    def test_parse_invalid_xml(self):
        invalid_xml_content = "<root><constant name='A'>10</constant>"
        with tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
            temp_file.write(invalid_xml_content)
            temp_file_path = temp_file.name

        with self.assertRaises(SyntaxError):
            self.xm_instance.parse_xml(temp_file_path)

    def test_convert(self):
        xml_content = """
        <root>
            <constant name="A">10</constant>
            <constant name="B">20</constant>
            <expression>.(+ A B).</expression>
        </root>
        """
        with tempfile.NamedTemporaryFile("w", delete=False) as temp_xml:
            temp_xml.write(xml_content)
            temp_xml_path = temp_xml.name

        with tempfile.NamedTemporaryFile("w", delete=False) as temp_output:
            temp_output_path = temp_output.name

        self.xm_instance.convert(temp_xml_path, temp_output_path)

        with open(temp_output_path, "r") as f:
            content = f.read()
        self.assertEqual(content.strip(), "30")


if __name__ == "__main__":
    unittest.main()
