import re
import json
from typing import Any, Optional

def extract_json_from_text(text: str) -> Optional[Any]:
   
    if not text:
        return None

    try:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return None

        json_str = match.group()
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None