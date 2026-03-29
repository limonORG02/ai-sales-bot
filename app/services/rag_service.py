import os

class RAGService:
    def __init__(self):
        self.knowledge_path = "data/knowledge.txt"

    def get_knowledge_context(self) -> str:
        """Читает файл знаний и возвращает текст"""
        if not os.path.exists(self.knowledge_path):
            return "Информация о компании пока не загружена."
        
        with open(self.knowledge_path, "r", encoding="utf-8") as f:
            return f.read()
