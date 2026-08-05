import json
import re
from pathlib import Path


MARKERS = (
    "Live hypotheses:",
    "Refuted hypotheses",
    "Chain:",
)


def inspect_raw_file(path: Path) -> dict:
    raw_text = path.read_text(encoding="utf-8")

    marker_counts = {
        marker: raw_text.count(marker)
        for marker in MARKERS
    }

    # Search the parsed JSON recursively, but do not require a role.
    data = json.loads(raw_text)
    matches = []

    def walk(value, json_path="$"):
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, f"{json_path}.{key}")

        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{json_path}[{index}]")

        elif isinstance(value, str):
            if any(marker in value for marker in MARKERS):
                matches.append(
                    {
                        "json_path": json_path,
                        "preview": value[:1000],
                        "full_text": value,
                    }
                )

    walk(data)

    return {
    "file": path.name,
    "raw_marker_counts": marker_counts,
    "matched_string_count": len(matches),
    "nodes_with_compressed_context": [
        {
            "node_index": index,
            "source_path": match["json_path"],
            "has_compressed_chain_context": True,
            "compressed_chain_context": match["full_text"],
        }
        for index, match in enumerate(matches)
    ],
}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("fix_traj", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = inspect_raw_file(args.fix_traj)
    output = json.dumps(result, indent=2, ensure_ascii=False)

    print(output)

    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"\nSaved to {args.output}")