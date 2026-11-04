# 7. Human Approval and Paper Library

## Approval interrupt
`agents/approval.py` uses LangGraph `interrupt` to pause after search. The payload contains a prompt and the papers serialized with `paper.model_dump()`.

When execution resumes, the selection is converted to an integer and decremented to obtain a zero-based list index. The selected paper/index are written to GraphState.

There is no explicit validation that the selected index is within range. The API model ensures `paper_number` is an integer, but does not check its bounds.

## Save interrupt
`agents/save.py` pauses with the message “Save this paper to your library? (yes/no)”. The value is lowercased and only exact `yes` triggers storage. The code does not strip surrounding whitespace, so values such as `" yes "` do not save.

## MemoryStore
Implementation: `memory/store.py`.

The library is a local JSON file at `library.json`:
- On initialization, creates an empty JSON array if the file is absent.
- `load()` reads/deserializes the file.
- `save()` rewrites it as indented UTF-8 JSON.
- `add_paper()` appends title, authors, publication date, PDF URL, summary and ISO save timestamp.
- `get_library()` returns the decoded list.

This is a saved-paper collection, not vector memory or conversational memory.

## Saved fields

| Field | Source |
|---|---|
| title | Selected Paper |
| authors | Selected Paper |
| published | Selected Paper |
| pdf_url | Selected Paper |
| summary | Summarizer node |
| saved_at | Local datetime at save time |

The abstract and source fields are not included in each saved library entry.

## Persistence limitations
- Writes are whole-file rewrites and have no explicit transactional locking.
- Duplicate papers are appended; no deduplication or update path exists.
- The API exposes the full library only; no search/filter route is implemented.
- The file is local to the process/container filesystem.
- Compose does not mount a persistent volume for `library.json`; the file can be lost when a container is replaced.
- LangGraph MemorySaver checkpoint state is separate from this paper library and is in-memory.
