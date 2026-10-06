# The Unofficial Guide

Brady Park, campus_life

---

# Unit 1

## What This Does

This answers questions about campus life using `campus_life`, a corpus of 88 short student posts. Most of them cover courses, housing, admin rules and dining halls, with a few on money, transit and study spaces. You can ask specific things like how long the lunch line is at Kestrel Commons, when the drop deadline is, or when the laundry room in a particular dorm is empty. Every answer names the post it came from. If nothing in the corpus is close enough to the question, it says "I don't have enough information about that" instead of guessing.

## Chunking Strategy

**Chunk size:** 600 characters (maximum)
**Overlap:** 0

My posts are short. All 88 are between 178 and 549 characters, and the median is 309. Most are a title line plus one to three short paragraphs, and the answer usually sits in a single sentence, like "$30 ... roughly 600 black-and-white pages." With the starter's 800-character windows, nothing would have been cut anyway, but a fixed window has no idea where a sentence ends. So I rewrote `split_documents` to keep each post whole if it fits under 600 characters. I picked 600 because it's just above my longest post. If a post is ever longer, the function splits it at paragraph and sentence boundaries and repeats the title on each piece, so no chunk is just a heading. Since nothing gets cut, there's nothing to overlap, so overlap is 0. The result is 88 posts and 88 chunks, averaging 317 characters.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer


**Question:** When is the best time to do laundry in Aldridge Hall?

**Answer:**

```
$ python app.py ask "When is the best time to do laundry in Aldridge Hall?"
  (best distance 0.302, cutoff 0.5)

The best time to do laundry in Aldridge Hall is Tuesday or Wednesday morning (housing_aldridge_hall_laundry.txt).

Sources retrieved: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_tamsin_court_laundry.txt
```

**My relevance cutoff:**

I set the cutoff at 0.5. To find it, I wrote `measure_cutoff.py`, which runs my five test questions and the five `OUT_OF_SCOPE` questions through retrieval only (no model calls) and records the best distance for each. The two groups were far apart. My in-corpus questions came back between 0.192 (printing quota) and 0.302 (Aldridge laundry). The out-of-scope ones came back between 0.825 (capital of Mongolia) and 0.934 (diesel engine oil). That leaves a gap of about 0.52, from 0.302 to 0.825.

The middle of the gap is around 0.56, but I went a little lower, to 0.5. A missed out-of-scope question would get a confident answer made up from campus posts, and I think that's worse than refusing a real question. Even at 0.5, my weakest real question (laundry, 0.302) still passes with about 0.2 to spare. The closest out-of-scope question is more than 0.3 above the line. I don't take that big gap too seriously, though. My out-of-scope questions are about things like the World Cup and Rust, which have nothing in common with campus life. To test that, I ran an off-topic question that sounds like it belongs on campus, "What's the parking fee at the hospital?" It came back at 0.644, much closer than anything in my out-of-scope set (0.825 and up) but still well over 0.5, so the gate refused it. That's still a good margin, but it's 0.18 closer than my five easy out-of-scope questions suggested.

After setting the number, I noticed the gate only checks the single best chunk. Once a question passed, all four retrieved chunks went to the model, including ones as far as 0.625 (`money_jobs.txt` came back for the dining dollars question). So I had Claude add `gate.py::relevant`, which uses the same 0.5 cutoff to drop each chunk that's over it before generation. That removed 6 of the 20 chunks across my five questions. It didn't catch everything: `housing_tamsin_court_laundry.txt` came back at 0.448 for the Aldridge question, which is under the cutoff. In all three runs, the answer cited it as a second source alongside the correct file. Lowering the cutoff to about 0.4 would have removed it, but it would also have removed useful context. That's a tradeoff I'll come back to in unit 2.

| Question | In corpus? | Best distance |
|---|---|---|
| Roughly how many black-and-white pages does the $30 semester printing quota cover? | yes | 0.192 |
| How long is the wait at Kestrel Commons between 12:15 and 1:00? | yes | 0.213 |
| Through which week can I drop a course, and what shows on my transcript if I drop after week two? | yes | 0.230 |
| What happens to leftover dining dollars at the end of the spring semester? | yes | 0.230 |
| When is the best time to do laundry in Aldridge Hall? | yes | 0.302 |
| What is the capital of Mongolia? | no | 0.825 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.844 |
| Who won the 1994 World Cup? | no | 0.886 |
| How do I write a for loop in Rust? | no | 0.896 |
| How do I change the oil in a diesel engine? | no | 0.934 |

## How I Used AI

**1.** Instead of just asking for a filter, I had Claude read my README, criteria, questions, chunker and config first. I told it what I'd already done (THRESHOLD set to 0.5 from measured distances) and gave it one scoped next step: filter retrieved chunks by distance, then run the `before` eval. Because it had my criteria, it checked the results against them and caught that the Aldridge laundry answer cited a different dorm's post in all three runs. That's the sibling confusion my criterion 5 predicted. I kept 0.5 and wrote it down as a criterion 5 problem instead of tuning the cutoff until it went away.

**2.** I asked Claude to write my cutoff explanation from what we'd already worked out, in my own voice. Its draft included a guess, marked as untested, that a question that sounds campus-related but isn't, like "What's the parking fee at the hospital?", would land much closer than my out-of-scope set. I didn't want an untested claim in my README, so I ran it myself. It came back at 0.644: closer than any of my out-of-scope questions, but still refused at 0.5. I replaced the guess with that number.

----

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
