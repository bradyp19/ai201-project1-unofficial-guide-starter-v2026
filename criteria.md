# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
My documents are short (~317 characters), and each of my five questions is answered by one sentence in one document, so retrieval should usually hit. But the corpus has near-duplicates (seven dining halls, seven dorms with parallel laundry/noise posts, and CS/BIOL/ECON course posts), so one question can pull the wrong sibling. Allowing one miss covers that; 5 of 5 would be too strict for embeddings that confuse similar-sounding documents.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Source names come from retrieval metadata, not from the model's memory, so attribution is mechanical and I expect all five. If it fails, it means the generation prompt or source line is broken, not that the question was hard, so I see no reason to allow a miss.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
My out-of-scope questions (Mongolia, diesel engines, World Cup, ibuprofen, Rust) share no vocabulary with campus life, so I expect a clear distance gap. One miss is allowed because short posts embed loosely and a generic question could land just under the cutoff. (To be updated with the actual distances in Milestone 4.)

---

## 4. Something about your chunks

In `python app.py chunks -n 5`, at least 4 of 5 sampled chunks must read as a complete thought, with no sentence cut in half at either end, and no chunk may be just a title line (e.g. "On the printing quota") with no content under it.

**Why this target:**
Most of my documents are a title line plus one to three sentences, and the answer often sits in a single sentence (e.g. "$30 ... roughly 600 black-and-white pages"). A chunk boundary through that sentence would separate a figure from what it describes. A title-only chunk would embed as a topic with no facts. Both are observable by reading five chunks.



---

## 5. Your choice

For at least 4 of my 5 test questions, the source named in the answer is the document that actually contains the `expects` text (e.g. the printing question cites `admin_printing_quota.txt`), not merely some retrieved document.

**Why this target:**
Criterion 2 only checks that a source is present. With near-duplicate documents (seven laundry posts, seven dining halls), a system can answer correctly yet cite the wrong sibling, which would mislead a student checking the claim. I allow one miss for the same sibling-confusion reason as criterion 1.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
