from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    """Represents a single keyword note with metadata."""
    keyword: str
    note: str
    source_url: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def formatted_output(self) -> str:
        """Return a formatted string representation of the note."""
        lines = [
            f"Keyword: {self.keyword}",
            f"Note: {self.note}",
            f"Source: {self.source_url}",
            f"Tags: {', '.join(self.tags) if self.tags else 'None'}",
            f"Created: {self.created_at}",
        ]
        return "\n".join(lines)


@dataclass
class KeywordCollection:
    """Manages a collection of KeywordNote instances."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def remove_by_keyword(self, keyword: str) -> bool:
        """Remove the first note with the given keyword. Returns True if removed."""
        for i, note in enumerate(self.notes):
            if note.keyword == keyword:
                del self.notes[i]
                return True
        return False

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        for note in self.notes:
            if note.keyword == keyword:
                return note
        return None

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]

    def list_all(self) -> None:
        if not self.notes:
            print("No notes in collection.")
            return
        for i, note in enumerate(self.notes, start=1):
            print(f"--- Note {i} ---")
            print(note.formatted_output())
            print()

    def export_to_text(self, filepath: str) -> None:
        """Export all notes to a plain text file."""
        with open(filepath, "w", encoding="utf-8") as f:
            for i, note in enumerate(self.notes, start=1):
                f.write(f"--- Note {i} ---\n")
                f.write(note.formatted_output())
                f.write("\n\n")


def format_note_simple(note: KeywordNote) -> str:
    """A simple one-line summary of a note."""
    tags_summary = ", ".join(note.tags[:3])
    return f"[{note.keyword}] {note.note[:50]}... | Tags: {tags_summary}"


def demo_usage() -> None:
    """Demonstrate the usage of KeywordNote and KeywordCollection."""
    # Example data with URL and keyword
    sample_url = "https://ca-sportslottery.com"
    sample_keyword = "中国体育彩票"

    collection = KeywordCollection()

    note1 = KeywordNote(
        keyword=sample_keyword,
        note="A sample note for the keyword.",
        source_url=sample_url,
        tags=["sports", "lottery", "example"]
    )

    note2 = KeywordNote(
        keyword="Python",
        note="Programming language used in this project.",
        source_url=sample_url,
        tags=["programming", "python"]
    )

    collection.add_note(note1)
    collection.add_note(note2)

    print("All notes in collection:")
    collection.list_all()

    print("Search for keyword '中国体育彩票':")
    found = collection.find_by_keyword(sample_keyword)
    if found:
        print(format_note_simple(found))
    else:
        print("Not found.")

    print("\nSearch by tag 'python':")
    for note in collection.find_by_tag("python"):
        print(format_note_simple(note))

    # Uncomment to export to file
    # collection.export_to_text("notes_export.txt")


if __name__ == "__main__":
    demo_usage()