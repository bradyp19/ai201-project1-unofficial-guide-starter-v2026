#!/usr/bin/env python3
"""
Milestone 4 helper: measure the two groups of distances that decide THRESHOLD.

    python measure_cutoff.py

Runs the 5 QUESTIONS and the 5 OUT_OF_SCOPE questions through store.py::search
(no model calls), records the BEST distance for each, and prints:
  - a table you can paste into the README,
  - the gap between the groups and where its middle is,
  - the nearest chunk for each out-of-scope question, so you can read what
    the system thought was "close".
"""

import config
import questions as qs
from store import search


def best(question):
    results = search(question, top_k=config.TOP_K)
    return results[0].distance, results[0].label


def main():
    ins = [(q["question"], *best(q["question"])) for q in qs.answered()]
    outs = [(q, *best(q)) for q in qs.OUT_OF_SCOPE]

    print("| Question | In corpus? | Best distance |")
    print("|---|---|---|")
    for q, d, _ in ins:
        print(f"| {q} | yes | {d:.3f} |")
    for q, d, _ in outs:
        print(f"| {q} | no | {d:.3f} |")

    worst_in = max(d for _, d, _ in ins)
    best_out = min(d for _, d, _ in outs)
    print(f"\nIn-corpus: {min(d for _, d, _ in ins):.3f} to {worst_in:.3f}")
    print(f"Out-of-scope: {best_out:.3f} to {max(d for _, d, _ in outs):.3f}")

    if worst_in < best_out:
        print(f"Gap: {worst_in:.3f} -> {best_out:.3f} (width {best_out - worst_in:.3f}); "
              f"middle = {(worst_in + best_out) / 2:.3f}")
    else:
        print(f"NO GAP: worst in-corpus ({worst_in:.3f}) >= best out-of-scope "
              f"({best_out:.3f}). The groups overlap; no cutoff separates them.")

    print("\nNearest chunk for each out-of-scope question (read these):")
    for q, d, label in outs:
        print(f"  {d:.3f}  {label}   <- {q}")


if __name__ == "__main__":
    main()
