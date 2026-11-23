# models.py
# Simple containers for our data.

class ToolDefinition:
    # One tool from an MCP server
    def __init__(self, name, description, input_schema):
        self.name = name
        self.description = description
        self.input_schema = input_schema


class Finding:
    # One problem found by the static layer
    def __init__(self, rule, severity, reason):
        self.rule = rule
        self.severity = severity
        self.reason = reason


class Verdict:
    # Our final decision about a tool
    def __init__(self, tool_name, decision, layer, reason):
        self.tool_name = tool_name
        self.decision = decision   # "allow", "block", "flag"
        self.layer = layer         # "static", "diff", "policy"
        self.reason = reason
        self.findings = []

    def add_finding(self, finding):
        # Attach one Finding to this Verdict
        self.findings.append(finding)