"""Simple closure journal."""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from .core import MonadAnswer


DEFAULT_PATH = "closure_journal.jsonl"


def append_entry(source: str, monad: MonadAnswer, path: str = DEFAULT_PATH, extra: Optional[Dict] = None) -> None:
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "source": source,
        "pole_a": monad.pole_a,
        "pole_b": monad.pole_b,
        "dominant": monad.dominant,
        "closure": round(monad.closure, 3),
        "relation_type": monad.relation_type,
    }
    if extra:
        entry.update(extra)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_journal(path: str = DEFAULT_PATH) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


def summary(path: str = DEFAULT_PATH) -> Dict[str, Any]:
    entries = load_journal(path)
    if not entries:
        return {"count": 0, "avg_closure": 0.0, "sources": []}
    closures = [e.get("closure", 0) for e in entries]
    sources = sorted({e.get("source", "?") for e in entries})
    return {
        "count": len(entries),
        "avg_closure": round(sum(closures) / len(closures), 3),
        "sources": sources,
    }


class JournalRecorder:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path

    def record_results(self, source: str, level_results: Dict) -> int:
        count = 0
        for level_name, level_res in level_results.items():
            if not hasattr(level_res, "monads"):
                continue
            for monad in level_res.monads:
                if monad.is_strongly_closed(0.60):
                    append_entry(source, monad, self.path, extra={"level": level_name})
                    count += 1
        return count
