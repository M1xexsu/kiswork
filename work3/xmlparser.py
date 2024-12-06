import xml.etree.ElementTree as ET
import re

class xm:
    def __init__(self):
        self.constants = {}

    def parse_constant(self, expr):
        if not expr.startswith('.(') or not expr.endswith(').'):
            raise SyntaxError(f"Not an expression: {expr}")
        expr = expr[2:-2]
        operands = re.split(r"\s+", expr)
        result = self._recursive_parse(operands)
        return str(result)

    def _recursive_parse(self, operands):
        if not operands:
            raise SyntaxError("Invalid expression: missing operands or operator")
        operator = operands.pop(0)
        resolved_operands = []

        while operands:
            operand = operands.pop(0)
            if re.match(r"[A-Z]+", operand):
                resolved_operands.append(self._resolve_constant(operand))
            elif operand in "+-*/min":
                operands.insert(0, operand)
                resolved_operands.append(self._recursive_parse(operands))
            else:
                resolved_operands.append(float(operand))

        if operator == "min":
            return min(resolved_operands)
        elif operator == "+":
            return sum(resolved_operands)
        elif operator == "-":
            if len(resolved_operands) != 2:
                raise SyntaxError("Subtraction requires exactly 2 operands")
            return resolved_operands[0] - resolved_operands[1]
        elif operator == "*":
            result = 1
            for op in resolved_operands:
                result *= op
            return result
        elif operator == "/":
            if len(resolved_operands) != 2:
                raise SyntaxError("Division requires exactly 2 operands")
            return resolved_operands[0] / resolved_operands[1]
        else:
            raise SyntaxError(f"Unsupported operator: {operator}")

    
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
            tree = ET.fromstring(xml_file)
            return self._convert_element(tree)
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
            #lines.append(f"(def {name} {value});")
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