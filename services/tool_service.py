from datetime import datetime

class ToolService:
    def calculate_days_until(self, target_date: str) -> str:
        try:
            today = datetime.today().date()
            target = datetime.strptime(target_date, "%Y-%m-%d").date()
            delta = (target - today).days

            if delta > 0:
                return f"{delta}일 남았습니다."
            elif delta == 0:
                return "오늘입니다!"
            else:
                return f"{abs(delta)}일 지났습니다."
        except ValueError:
            return "잘못된 날짜 형식입니다. YYYY-MM-DD 형식으로 입력해주세요."

    def calculate_days_from_text(self, text: str) -> str:
        import re
        match = re.search(r"\d{4}-\d{2}-\d{2}", text)
        if match:
            date_str = match.group()
            return self.calculate_days_until(date_str)
        return "날짜를 인식하지 못했습니다. YYYY-MM-DD 형식으로 입력해주세요."
