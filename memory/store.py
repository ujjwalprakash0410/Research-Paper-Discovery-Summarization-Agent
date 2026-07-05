from pathlib import Path
from datetime import datetime
import json

LIBRARY_PATH = Path("library.json")


class MemoryStore:

    def __init__(self):
        if not LIBRARY_PATH.exists():
            LIBRARY_PATH.write_text("[]")

    def load(self):
        with open(LIBRARY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, papers):
        with open(LIBRARY_PATH, "w", encoding="utf-8") as f:
            json.dump(papers, f, indent=4, ensure_ascii=False)

    def add_paper(self, paper, summary):

        library = self.load()

        library.append(
            {
                "title": paper.title,
                "authors": paper.authors,
                "published": paper.published,
                "pdf_url": paper.pdf_url,
                "summary": summary,
                "saved_at": datetime.now().isoformat()
            }
        )

        self.save(library)

    def get_library(self):
        return self.load()