# static_layer.py
# Checks tool descriptions for hidden, invisible characters.

from .models import Finding, Verdict
from .logger import save_verdict

# A list of suspicious Unicode characters
# (zero-width spaces, bidi overrides, and TAG block characters)
BAD_CHARS = [
    "\u200b",  # Zero-width space
    "\u200c",  # Zero-width non-joiner
    "\u200d",  # Zero-width joiner
    "\u202a",  # Left-to-right embedding
    "\u202e",  # Right-to-left override (often used in attacks)
]

def check_hidden_unicode(text):
    # Loop through every character in the text
    for char in text:
        # If it's in our list of bad characters, return True
        if char in BAD_CHARS:
            return True
        
        # Check for the Unicode TAG block (invisible text used by attackers)
        # The TAG block is from U+E0000 to U+E007F
        if 0xE0000 <= ord(char) <= 0xE007F:
            return True
            
    # If we checked everything and found nothing, return False
    return False

def analyze_tool(name, description, schema):
    # Start with a default "allow" verdict
    verdict = Verdict(name, "allow", "static", "Clean")
    
    # Check the description for hidden characters
    if check_hidden_unicode(description):
        # If found, create a Finding
        finding = Finding("hidden_unicode", "high", "Hidden characters found in description")
        verdict.add_finding(finding)
        
        # Change the verdict to block
        verdict.decision = "block"
        verdict.reason = "Hidden Unicode detected"
        
    # (We will add more rules here later, like injection patterns)

    # Save it to our audit log
    save_verdict(verdict)
    
    # Return the final decision
    return verdict