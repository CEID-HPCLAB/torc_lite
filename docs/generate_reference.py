"""Generate source-backed demo pages (do not edit generated pages by hand)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "docs" / "generated" / "examples"
DEMOS = {
    "masterslave": ("Master–worker", "Basic task creation, input copies and output values."),
    "fibo": ("Recursive Fibonacci", "Nested tasks with a serial recursion cutoff."),
    "broadcast": ("Broadcast", "Distributing shared scalar/array values before spawning tasks."),
    "struct": ("Struct arguments", "In/out task data packed into a C struct."),
    "zerolength": ("Zero-length arguments", "Arguments whose element count may be zero."),
    "async": ("Asynchronous callback pattern", "Advanced detached and direct task operations."),
    "pipe": ("Pipeline / SPMD pattern", "Advanced MPI, local threading and scheduler coordination."),
    "mbench1": ("Microbenchmark", "A task-creation / completion overhead example."),
}


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    index = ["# Bundled demo source", "", "These pages embed the C source from the checked-out repository at documentation build time.", "",
             "The source is authoritative: read the accompanying [usage guides](../../examples/) before adapting an example.", ""]
    for stem, (title, description) in DEMOS.items():
        source = ROOT / "demo" / f"{stem}.c"
        if not source.is_file():
            raise FileNotFoundError(f"Expected demo source not found: {source}")
        content = source.read_text(encoding="utf-8", errors="replace")
        # Use a fence longer than any in the source so it cannot terminate prematurely.
        fence = "`" * (max([3] + [len(s) for s in content.split() if s.startswith("``")]) + 1)
        text = (f"# {title} — source\n\n{description}\n\n"
                f"**Repository:** [`demo/{stem}.c`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/demo/{stem}.c). "
                f"This page is generated from the live code at build time.\n\n"
                f"{fence}c\n{content.rstrip()}\n{fence}\n")
        (DEST / f"{stem}.md").write_text(text, encoding="utf-8")
        index.append(f"- [{title}]({stem}.md): {description}")
    (DEST / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    header_dir = ROOT / "docs" / "generated" / "headers"
    header_dir.mkdir(parents=True, exist_ok=True)
    for name, title, language in (("torc.h", "C API public header", "c"), ("torcf.h", "Fortran declaration header", "fortran")):
        source = ROOT / "include" / name
        if not source.is_file():
            raise FileNotFoundError(f"Expected header source not found: {source}")
        content = source.read_text(encoding="utf-8", errors="replace")
        output = (f"# {title} — current source\n\n"
                  f"Automatically generated from [`include/{name}`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/include/{name}) "
                  f"in the checked-out repository.\n\n"
                  f"````{language}\n{content.rstrip()}\n````\n")
        (header_dir / (name.removesuffix(".h") + ".md")).write_text(output, encoding="utf-8")
    print(f"Generated {len(DEMOS)} demo source pages and 2 public header pages")


if __name__ == "__main__":
    main()
