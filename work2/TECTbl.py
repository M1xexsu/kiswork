import unittest
from unittest.mock import patch, mock_open, MagicMock
import xml.etree.ElementTree as ET
from reqgen import generate

class TestGenerateFunction(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.get')
    def test_generate_base_case(self, mock_requests_get, mock_file):
        pom_xml = """<project xmlns="http://maven.apache.org/POM/4.0.0">
                        <dependencies>
                            <dependency>
                                <groupId>com.example</groupId>
                                <artifactId>example-artifact</artifactId>
                                <version>1.0.0</version>
                            </dependency>
                        </dependencies>
                    </project>"""
        mock_requests_get.return_value.text = pom_xml
        generate("com.example", 1, "1.0.0")
        mock_requests_get.assert_called_once_with("https://repo1.maven.org/maven2/com/example/1.0.0/com.example-1.0.0.pom")
        mock_file().write.assert_called_with("(com.example) -> (example-artifact)\n")

    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.get')
    def test_generate_with_version_placeholder(self, mock_requests_get, mock_file):
        pom_xml = """<project xmlns="http://maven.apache.org/POM/4.0.0">
                        <dependencies>
                            <dependency>
                                <groupId>com.example</groupId>
                                <artifactId>example-artifact</artifactId>
                                <version>${project.version}</version>
                            </dependency>
                        </dependencies>
                    </project>"""
        metadata_xml = """<metadata>
                            <versioning>
                                <release>2.0.0</release>
                            </versioning>
                          </metadata>"""
        mock_requests_get.side_effect = [MagicMock(text=pom_xml), MagicMock(text=metadata_xml)]
        generate("com.example", 1, "1.0.0")
        self.assertEqual(mock_requests_get.call_count, 2)
        mock_requests_get.assert_any_call("https://repo1.maven.org/maven2/com/example/example-artifact/maven-metadata.xml")
        mock_file().write.assert_called_with("(com.example) -> (example-artifact)\n")

if __name__ == '__main__':
    unittest.main()
