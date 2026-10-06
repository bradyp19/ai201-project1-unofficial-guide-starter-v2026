#!/usr/bin/env python3
"""
Milestone 4 helper: run a few test questions through retrieval only (no model
call, no quota) and print every retrieved chunk with its distance.

    python inspect_retrieval.py              first three questions in questions.py
    python inspect_retrieval.py 0 3 4        pick questions by position
    python inspect_retrieval.py --reindex    rebuild the index first

Uses store.py::search and gate.py::check unchanged.
"""

import sys

import config
import gate
import questions as qs
from store import search, index_exists


def main():
    args = sys.argv[1:]
    if "--reindex" in args or not index_exists():
        from chunker import split_documents
        from ingest import load_documents
        from store import build_index

        args = [a for a in args if a != "--reindex"]
        n = build_index(split_documents(load_documents()))
        print(f"(re)indexed {n} chunks\n")

    items = qs.answered()
    picks = [items[int(a)] for a in args] if args else items[:3]

    for item in picks:
        results = search(item["question"], top_k=config.TOP_K)
        decision = gate.check(results)
        print("=" * 72)
        print(f"Q: {item['question']}")
        print(f"expects: {item['expects']!r}   gate: {decision.explanation}")
        for r in results:
            hit = "  <-- contains expects" if item["expects"].lower() in r.text.lower() else ""
            print(f"\n  [{r.distance:.3f}] {r.label}{hit}")
            print("  " + r.text.replace("\n", "\n  "))
        print()


if __name__ == "__main__":
    main()
