# 4. Paper Discovery

## Source: arXiv
The discovery implementation is in `agents/search.py` and uses the `arxiv` Python package. A module-level `arxiv.Client()` is created once.

## Search construction
`search_arxiv(query)` creates an `arxiv.Search` using:
- User's normalized query.
- `settings.max_search_results` (default 5).
- `arxiv.SortCriterion.Relevance`.

The function iterates through results returned by the client.

## Mapping an arXiv result to Paper

| Paper field | Source |
|---|---|
| `title` | `result.title` |
| `authors` | Author names |
| `abstract` | `result.summary` |
| `published` | Publication date formatted as YYYY-MM-DD |
| `pdf_url` | `result.pdf_url` |
| `source` | Literal `"arxiv"` |
| `score` | Optional; not populated |

The Pydantic `Paper` model is declared in `models.py`.

## Search-to-selection flow
The search node writes the Paper objects to GraphState. The next node, approval, pauses execution and exposes serialized results. The user chooses a one-based paper number, which the approval node converts to a zero-based array index.

## Limitations visible in code
- Search is arXiv-only.
- `tavily_api_key` is required by configuration but not used in the current search implementation.
- There is no multi-source deduplication or ranking.
- The optional `score` field is not populated.
- Search failures/rate limits have no explicit retry/backoff handling.
- An empty result list is not specially handled before the approval interrupt.
- Result count is capped by `MAX_SEARCH_RESULTS`, default 5.

## Relevant files
- `agents/search.py` — arXiv query and Paper mapping.
- `agents/approval.py` — human paper selection.
- `config.py` — search result limit.
- `models.py` — Paper schema.
