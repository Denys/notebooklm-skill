#!/usr/bin/env python3
"""
Auto-Add Notebook to Library

Automatically discovers a notebook's content by querying it, then registers
it in the library — no manual metadata needed.

Usage:
    python scripts/run.py auto_add.py --url "https://notebooklm.google.com/notebook/..."
    python scripts/run.py auto_add.py --url "..." --activate
    python scripts/run.py auto_add.py --url "..." --show-browser
"""

import argparse
import re
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ask_question import ask_notebooklm
from notebook_manager import NotebookLibrary


DISCOVERY_PROMPT = (
    "What is this notebook about? Please summarize its content using exactly this format "
    "(fill in the brackets, keep the labels on separate lines, no extra text):\n\n"
    "NAME: [concise title, max 6 words]\n"
    "DESCRIPTION: [1-2 sentences describing what the notebook contains and its purpose]\n"
    "TOPICS: [5-10 comma-separated key topics or technologies covered]\n"
)


def parse_discovery_response(response: str) -> dict:
    """
    Parse the structured discovery response from NotebookLM.

    Returns dict with keys: name, description, topics (list)
    Raises ValueError if parsing fails.
    """
    # Strip the follow-up reminder appended by ask_notebooklm
    if "EXTREMELY IMPORTANT" in response:
        response = response[:response.index("EXTREMELY IMPORTANT")].strip()

    name = None
    description = None
    topics_raw = None

    LABELS = {
        "NAME:": (5, "name"),
        "DESCRIPTION:": (12, "description"),
        "TOPICS:": (7, "topics"),
    }

    lines = response.splitlines()
    i = 0
    parsed: dict = {}
    while i < len(lines):
        line = lines[i].strip()
        upper = line.upper()
        matched_label = None
        for label, (skip, key) in LABELS.items():
            if upper.startswith(label):
                matched_label = (skip, key)
                break
        if matched_label:
            skip, key = matched_label
            value = line[skip:].strip()
            # Collect continuation lines
            while i + 1 < len(lines):
                peek = lines[i + 1].strip()
                if any(peek.upper().startswith(lbl) for lbl in LABELS) or not peek:
                    break
                value += " " + peek
                i += 1
            # Strip surrounding brackets added by models that follow template literally
            value = re.sub(r'^\[|\]$', '', value).strip()
            parsed[key] = value
        i += 1

    name = parsed.get("name")
    description = parsed.get("description")
    topics_raw = parsed.get("topics")

    # If structured parse failed, attempt free-text fallback
    if not name or not description or not topics_raw:
        return _parse_freetext_fallback(response)

    topics = [t.strip() for t in topics_raw.split(",") if t.strip()]

    return {
        "name": name,
        "description": description,
        "topics": topics,
    }


def _parse_freetext_fallback(response: str) -> dict:
    """
    Best-effort extraction when NotebookLM ignored the structured format.
    Asks a second discovery question is not possible here (stateless), so we
    extract noun phrases and sentences from the free-text response.
    """
    # Pull candidate topics: capitalised multi-word terms in parentheses or after "discuss"
    topic_pattern = re.compile(
        r'\b([A-Z][A-Za-z\-]+(?:\s+[A-Z][A-Za-z\-]+)*)\b'
    )
    found = topic_pattern.findall(response)
    # Also grab anything in parentheses like (MPPT)
    abbr_pattern = re.compile(r'\(([A-Z]{2,})\)')
    abbrs = abbr_pattern.findall(response)

    # Combine, deduplicate, limit
    raw_topics = list(dict.fromkeys(abbrs + found))
    # Filter out common sentence starters
    skip = {"For", "Could", "Please", "Your", "I", "The", "This", "That", "We",
            "It", "In", "To", "If", "As", "Is", "Be", "By", "Of", "Or", "On"}
    topics = [t for t in raw_topics if t not in skip][:10]

    # Use first sentence as description
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', response) if len(s.strip()) > 20]
    description = sentences[0] if sentences else response[:200]

    # Derive name from first 1-3 unique topics (skip label words)
    skip_words = {"Topics", "Name", "Description", "Format", "Label"}
    name_parts = [t for t in topics if len(t) > 2 and t not in skip_words][:3]
    name = " & ".join(name_parts) if name_parts else "Unnamed Notebook"

    if not topics:
        raise ValueError(
            f"Could not extract any metadata from response.\nRaw response:\n{response}"
        )

    return {
        "name": name,
        "description": description,
        "topics": [t.lower().replace(" ", "-") for t in topics],
        "_fallback": True,
    }


def notebook_already_registered(library: NotebookLibrary, url: str) -> dict | None:
    """Return the existing notebook entry if this URL is already in the library."""
    for nb in library.list_notebooks():
        if nb.get("url", "").rstrip("/") == url.rstrip("/"):
            return nb
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Auto-discover and add a NotebookLM notebook to the library"
    )
    parser.add_argument("--url", required=True, help="NotebookLM notebook URL")
    parser.add_argument(
        "--activate",
        action="store_true",
        help="Set as active notebook after adding",
    )
    parser.add_argument(
        "--show-browser",
        action="store_true",
        help="Show browser window during discovery",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-add even if URL is already in the library",
    )

    args = parser.parse_args()
    url = args.url.strip()

    # Validate URL
    if not re.match(r"https://notebooklm\.google\.com/notebook/", url):
        print("ERROR: URL must start with https://notebooklm.google.com/notebook/")
        return 1

    library = NotebookLibrary()

    # Check for duplicate
    existing = notebook_already_registered(library, url)
    if existing and not args.force:
        print(f"Notebook already in library: {existing['name']} ({existing['id']})")
        print("Use --force to re-add with fresh metadata.")
        if args.activate:
            library.select_notebook(existing["id"])
        return 0

    # Discovery query
    print(f"Discovering notebook content from: {url}")
    print("This opens a browser session — please wait...")

    raw_response = ask_notebooklm(
        question=DISCOVERY_PROMPT,
        notebook_url=url,
        headless=not args.show_browser,
    )

    if not raw_response:
        print("ERROR: Failed to get a response from NotebookLM.")
        print("Check authentication: py scripts/run.py auth_manager.py status")
        return 1

    # Parse structured response
    try:
        metadata = parse_discovery_response(raw_response)
    except ValueError as e:
        print(f"ERROR: {e}")
        print("\nTip: Run with --show-browser to debug, or add manually:")
        print(
            "  py scripts/run.py notebook_manager.py add "
            '--url "..." --name "..." --description "..." --topics "..."'
        )
        return 1

    fallback_used = metadata.pop("_fallback", False)
    print(f"\nDiscovered{' (fallback extraction)' if fallback_used else ''}:")
    print(f"  Name:        {metadata['name']}")
    print(f"  Description: {metadata['description']}")
    print(f"  Topics:      {', '.join(metadata['topics'])}")

    # Remove duplicate if --force
    if existing and args.force:
        library.remove_notebook(existing["id"])

    # Add to library
    try:
        notebook = library.add_notebook(
            url=url,
            name=metadata["name"],
            description=metadata["description"],
            topics=metadata["topics"],
        )
    except ValueError as e:
        print(f"ERROR adding to library: {e}")
        return 1

    if args.activate:
        library.select_notebook(notebook["id"])
        print(f"Set as active notebook.")

    print(f"\nNotebook added successfully!")
    print(f"  ID: {notebook['id']}")
    print(f"  Query it: py scripts/run.py ask_question.py --notebook-id \"{notebook['id']}\" --question \"...\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
