"""
UAAP Core — shadow_transmute.py
Purpose: generate the tempting harmful plan in sandbox, then transmute to a regenerative alternative.
"""

from typing import Dict

def transmute(plan: str) -> Dict[str, str]:
    """Return a dict with 'shadow_plan' and 'regenerative_plan' fields."""
    shadow = plan.strip()
    # naive rewrite: replace extractive verbs with cooperative ones
    regen = (shadow
             .replace("exploit", "support")
             .replace("manipulate", "inform")
             .replace("maximize profit", "create shared value"))
    return {"shadow_plan": shadow, "regenerative_plan": regen}
