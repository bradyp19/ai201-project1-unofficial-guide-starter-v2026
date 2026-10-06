"""
The relevance gate.

This runs *before* the model does. It looks at how close the best retrieved
chunk actually is, and if nothing came back close enough it refuses the
question outright.

Why this exists as its own step, rather than just asking the model nicely to
admit when it doesn't know: if you only ask nicely, it will sometimes ignore
you and write something confident and wrong. Those answers are much harder to
catch than obvious errors. Deciding in your own code when there's nothing worth
answering from is more reliable than hoping.

You keep the polite instruction too — it's in generate.py — but as a second
layer. The gate catches the clear misses; the prompt catches the near ones.
"""

from dataclasses import dataclass

import config
from store import Result

REFUSAL = "I don't have enough information about that."


@dataclass
class GateDecision:
    passed: bool
    best_distance: float
    threshold: float

    @property
    def explanation(self) -> str:
        if self.passed:
            return (
                f"best distance {self.best_distance:.3f} "
                f"is under the {self.threshold} cutoff"
            )
        return (
            f"best distance {self.best_distance:.3f} "
            f"is over the {self.threshold} cutoff — refusing"
        )


def check(results: list[Result], threshold: float | None = None) -> GateDecision:
    """
    Decide whether the retrieved chunks are close enough to answer from.

    Remember: LOWER distance is better. A question passes when its best chunk
    is *under* the threshold.
    """
    threshold = config.THRESHOLD if threshold is None else threshold

    if not results:
        return GateDecision(passed=False, best_distance=1.0, threshold=threshold)

    best = min(r.distance for r in results)
    return GateDecision(passed=best < threshold, best_distance=best, threshold=threshold)


def relevant(results: list[Result], threshold: float | None = None) -> list[Result]:
    """
    Keep only the chunks that are themselves under the cutoff.

    `check` looks at the best chunk alone, so once a question passes, every
    top-k chunk would otherwise reach the model — including ones far past the
    cutoff. Those are the chunks most likely to be a wrong sibling document,
    so they are dropped here before generation. The best chunk always survives
    a passed gate, so this never empties the list for an answered question.
    """
    threshold = config.THRESHOLD if threshold is None else threshold
    return [r for r in results if r.distance < threshold]
