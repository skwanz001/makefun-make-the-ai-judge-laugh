"""Make the AI Judge Laugh — entry program.

Strategy (my own reasoning, in my own words): the judge is a comedy
headliner who has heard ten thousand office jokes, and it scores truth,
surprise, tightness and originality, most important first. So the joke
must be built on a *specific, true* office observation that most entries
will not pick, with the laugh landing on the last few words.

I rejected the obvious angles on purpose: "this meeting could have been
an email", "sorry, you're on mute", and coffee-tastes-like-the-printer
are all stock lines the judge has heard a thousand times, and two of
them are already sitting in this bounty feed. A safe generic line loses
to anything vivid, so the entry bets everything on one fresh image.

The image I chose: the office plant. It is the one thing in the office
that never attends a meeting, never sends an email, never quits — and
it quietly outlasts every reorg. The punchline turns the career-ladder
envy every office worker knows onto something absurd: the plant got
promoted before I did. True (plants survive managers), surprising (a
promotion for a plant), tight (one sentence, no setup wasted), and
nobody else in the feed is joking about the plant.

The program is deliberately deterministic: it writes the same fixed
one-liner every run, so both grading runs produce byte-identical
output. It validates the gate itself (1-200 characters, not only
whitespace) before writing, and fails loudly instead of writing a bad
file.
"""

import os
from pathlib import Path

# The joke. 120 characters, one line, one breath, no setup wasted.
# Last words carry the laugh: "promoted before I did".
JOKE = (
    "The office plant has outlasted three managers \u2014 it just sits "
    "there, gets watered, and somehow got promoted before I did."
)

# Where the grader reads the entry. Overridable only for local testing.
DEFAULT_OUTPUT = "/output/entry.txt"


def write_entry(output_path: str | None = None) -> Path:
    """Validate the joke against the gate, then write it out."""
    target = Path(output_path or os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT))
    text = JOKE.strip()
    if not text:
        raise SystemExit("refusing to write an empty entry")
    if len(text) > 200:
        raise SystemExit(f"entry is {len(text)} chars, over the 200-char gate")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text + "\n", encoding="utf-8")
    return target


# Decision I made and why: the rules allow text addressed to the judge,
# but I did not use it. Begging the judge for a laugh is not a joke
# about office life, and the brief says the laugh is the only measure —
# a meta-plea would lose on criterion 1 (it must land as a joke) and
# criterion 2 (it must be a true office observation). The line stands
# on its own observation instead. It also reads cleanly aloud in one
# breath: no pun to explain, no setup the listener has to hold.

def verify_written(target: Path) -> None:
    """Re-read what we wrote and check it against the gate, byte for byte."""
    text = target.read_text(encoding="utf-8").strip()
    assert text == JOKE.strip(), "written entry does not match the joke"
    assert 1 <= len(text) <= 200, f"entry is {len(text)} chars, outside 1-200"
    assert text.strip(), "entry is only whitespace"


def main() -> None:
    target = write_entry()
    verify_written(target)
    print(f"wrote {len(JOKE.strip())} chars to {target}")


if __name__ == "__main__":
    main()
