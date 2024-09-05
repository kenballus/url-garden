import subprocess
import sys
from typing import Iterable


def parse_afl_map(filename: str) -> set[int]:
    """Extracts the edge IDs from an afl-showmap output. Ignores edge counts."""
    with open(filename) as f:
        return set(map(lambda line: int(line.strip().split(":")[0]), f.readlines()))


def get_all_prefixes(b: bytes) -> Iterable[bytes]:
    """Returns an iterable of all prefixes of a given string."""
    return (b[:i] for i in range(len(b) + 1))


def execute(target: str, the_input: bytes) -> set[int]:
    subprocess.run(
        f"./AFLplusplus/afl-showmap -o trace_{target} -- ./targets/{target}/venv/bin/python3 ./targets/{target}/target.py".split(),
        input=the_input,
        capture_output=True,
    )
    return parse_afl_map(f"trace_{target}")


def compute_deltas(target_dir: str) -> dict[bytes, set[int]]:
    deltas: dict[bytes, set[int]] = {}
    the_whole_input: bytes = sys.stdin.buffer.read()
    prev_map: set[int] = set()
    for prefix in get_all_prefixes(the_whole_input):
        the_map: set[int] = execute(target_dir, prefix)
        deltas[prefix] = the_map - prev_map
        prev_map = the_map
    return deltas


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <target>")
    else:
        for prefix, delta in compute_deltas(sys.argv[1]).items():
            if len(delta) > 0:
                print(f"{prefix}: {len(delta)} new edges.")
