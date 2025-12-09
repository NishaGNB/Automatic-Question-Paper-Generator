import hashlib


def normalize_question_text(text: str) -> str:
    return " ".join(text.strip().lower().split())


def question_hash(text: str) -> str:
    normalized = normalize_question_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def filter_reference_by_topics(reference_text: str, topics: str) -> str:
    """Simple NLP-like filter: keep paragraphs mentioning at least one topic token."""
    topic_tokens = [t.strip().lower() for t in topics.replace("\n", ",").split(",") if t.strip()]
    if not topic_tokens:
        return reference_text
    paragraphs = [p.strip() for p in reference_text.split("\n\n") if p.strip()]
    selected = []
    for p in paragraphs:
        low = p.lower()
        if any(tok in low for tok in topic_tokens):
            selected.append(p)
    return "\n\n".join(selected) if selected else reference_text
