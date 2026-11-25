"""One-line deadline excuse writer.

Writes a single-line joke giving an excuse for missing a deadline to
entry.txt. The line must be 1 to 200 characters, a single line, with no
trailing newline, per the bounty gate.

The joke: the report was finished on time, but the laptop renamed the
file to yet another "final" version and buried it somewhere unknown.
It is a real excuse for a missed deadline, a single sentence that lands
its punch at the end, and it sounds like something a person would
actually say when cornered by a boss, with a fresh angle on the tired
"my file got lost" story.
"""

import os

ENTRY = (
    "I finished the report on time, but my laptop renamed it "
    "final_FINAL_v2(3) and hid it in a folder I have never seen."
)

MAX_CHARS = 200


def count_chars(text):
    """Return the character count of the entry (gate counts characters)."""
    return len(text)


def validate(text):
    """Check the entry against the gate.

    The gate requires UTF-8 text of 1 to 200 characters, not only
    whitespace, and the bounty requires a single line with no trailing
    newline. Each check below maps to one of those requirements, and
    raises a clear error naming the failed rule so a bad entry is
    caught locally before it ever reaches the server.
    """
    if not text or text.strip() == "":
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) != len(text.strip()):
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not 1 <= count_chars(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be 1-200 characters, got %d" % count_chars(text)
        )


def write_entry(output_dir):
    """Write the validated entry to entry.txt with safe permissions."""
    validate(ENTRY)
    os.makedirs(output_dir, exist_ok=True)
    os.chmod(output_dir, 0o755)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    os.chmod(path, 0o644)
    return path


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(output_dir)
    print("Wrote %d characters to %s" % (len(ENTRY), path))


if __name__ == "__main__":
    main()
