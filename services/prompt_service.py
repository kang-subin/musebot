import os
from core.db_service import DBService

class PromptService:

    def __init__(self, prompts_dir="prompts", use_db=False):
        self.prompts_dir = prompts_dir
        self.use_db = use_db
        self.db_service = DBService() if use_db else None

    def get_prompt(self, intent: str) -> str:
        return (
            self._get_prompt_from_db(intent) if self.use_db
            else self._get_prompt_from_file(intent)
        )
    
    def _get_prompt_from_file(self, intent: str) -> str:
        filename = f"{intent}.txt"
        filepath = os.path.join(self.prompts_dir, filename)

        if not os.path.exists(filepath):
            return ""

        with open(filepath, "r", encoding="utf-8") as file:
            return file.read().strip()
        
    def _get_prompt_from_db(self, intent: str) -> str:
        return self.db_service.get_prompt(intent)
