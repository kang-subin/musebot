from datetime import datetime
import pytz
import dateparser
from typing import NamedTuple, Optional


class ToolResult(NamedTuple):
    success: bool
    message: str


class ToolService:
    CITY_TZ = {
        "서울": "Asia/Seoul",
        "뉴욕": "America/New_York",
        "la": "America/Los_Angeles",
        "런던": "Europe/London",
        "도쿄": "Asia/Tokyo",
        "파리": "Europe/Paris"
    }

    def execute_tool(self, intent: str, text: str) -> Optional[ToolResult]:
        actions = {
            "date_calculation": self.calculate_days_from_text,
            "time_conversion": self.get_current_time_in_timezone
        }
        action = actions.get(intent)
        if action:
            return action(text)
        return None

    def calculate_days_from_text(self, text: str) -> ToolResult:
        
        parsed_date = dateparser.parse(text, languages=["ko", "en"])
        if not parsed_date:
            return ToolResult(False, "날짜를 인식하지 못했습니다.")

        delta = (parsed_date.date() - datetime.today().date()).days
        if delta > 0:
            return ToolResult(True, f"{delta}일 남았습니다.")
        elif delta == 0:
            return ToolResult(True, "오늘입니다!")
        else:
            return ToolResult(True, f"{abs(delta)}일 지났습니다.")

    def get_current_time_in_timezone(self, text: str) -> ToolResult:
        for city, tz_name in self.CITY_TZ.items():
            if city.lower() in text.lower():
                now = datetime.now(pytz.timezone(tz_name))
                return ToolResult(True, now.strftime(f"{city} 현재 시각: %Y-%m-%d %H:%M:%S"))
        return ToolResult(False, "도시를 인식하지 못했습니다.")
