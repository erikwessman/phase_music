import argparse
import json
import os

WRITE_TO = "_phases.mmd"
MERMAID_TEMPLATE = "graph TD\n\n"


def to_mermaid(config: dict) -> str:
    phases = [
        (phase["unique_id"], phase.get("next_phase")) for phase in config["phases"]
    ]

    output = MERMAID_TEMPLATE
    for uid, next_phase in phases:
        if next_phase is None:
            output += f"{uid}\n"
        else:
            output += f"{uid} --> {next_phase}\n"

    return output


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--config", help="Path to config")
    args = argparser.parse_args()

    if not os.path.exists(args.config):
        raise FileNotFoundError(f"Config not found: {args.config}")

    data = json.load(open(args.config))
    diagram = to_mermaid(data)

    with open(WRITE_TO, "w") as f:
        f.write(diagram)
