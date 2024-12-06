import xml.etree.ElementTree as ET
import re

class xm:
    def __init__(self):
        self.constants = {}

    def parse_constant(self, expr):
        match = re.match(r"\.\(([\+\-\*/]|min)\s+([A-Z0-9\s]+)\)\.", expr)
        if not match:
            raise SyntaxError(f"Invalid constant expression: {expr}")

        operator, operands = match.groups()
        operands = operands.split()
        if operator == "min":
            result = min(map(self._resolve_constant, operands))
        elif operator == "+":
            result = sum(map(self._resolve_constant, operands))
        elif operator == "-":
            result = self._resolve_constant(operands[0]) - self._resolve_constant(operands[1])
        elif operator == "*":
            result = self._resolve_constant(operands[0]) * self._resolve_constant(operands[1])
        elif operator == "/":
            result = self._resolve_constant(operands[0]) / self._resolve_constant(operands[1])
        else:
            raise SyntaxError(f"Unsupported operator: {operator}")

    # Преобразуем результат в строку
        return str(result)

    
    def _resolve_constant(self, value):
        if value.startswith('"') and value.endswith('"'):
            return value.strip('"')
        elif value.isdigit():
            return int(value)
        elif value in self.constants:
            return self.constants[value]
        else:
            raise ValueError(f"Undefined constant: {value}")
    
    def parse_xml(self, xml_file):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            return self._convert_element(root)
        except ET.ParseError as e:
            raise SyntaxError(f"Invalid XML: {e}")

    def _convert_element(self, element):
        lines = []
        if element.tag == "comment":
            if "type" in element.attrib and element.attrib["type"] == "multi":
                lines.append("(*")
                lines.extend([line.text.strip() for line in element])
                lines.append("*)")
            else:
                lines.append(f"' {element.text.strip()}")
        elif element.tag == "constant":
            name = element.attrib["name"]
            value = element.text.strip()
            self.constants[name] = self._resolve_constant(value)
            lines.append(f"(def {name} {value});")
        elif element.tag == "array":
            values = " ".join(str(self._resolve_constant(v)) for v in element.text.strip().split())
            lines.append(f"[ {values} ]")
        elif element.tag == "expression":
            lines.append(self.parse_constant(element.text.strip()))
        else:
            for child in element:
                lines.extend(self._convert_element(child))
        return lines
    
    def convert(self, xml_file, output_file):
        try:
            config_lines = self.parse_xml(xml_file)
            with open(output_file, "w") as f:
                f.write("\n".join(config_lines))
            print(f"Conversion completed. Output saved to {output_file}")
        except Exception as e:
            print(f"Error: {e}")