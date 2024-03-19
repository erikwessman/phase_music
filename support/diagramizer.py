import json
import os

WRITE_TO = "_diagrams"
CONFIGS = "configs"
MERMAID_TEMPLATE = "graph TD\n\n"


def to_mermaid(config: dict) -> str:
    output = MERMAID_TEMPLATE
    output += "style start fill:#1e90ff,color:#fff \n"
    output += f"start --> {config["start_phase"]} \n"

    for phase in config["phases"]:
        uid = phase["unique_id"]
        next_phase = phase.get("next_phase")
        key = phase.get("key")

        if next_phase is None:
            output += f"{uid}\n"
        else:
            output += f"{uid} --> {next_phase}\n"

        if key is not None:
            output += f"{uid} -->|{key}| {uid}\n"

    return output


if __name__ == "__main__":
    if not os.path.exists(WRITE_TO):
        os.makedirs(WRITE_TO)

    for f in os.listdir(CONFIGS):
        config_path = os.path.join(CONFIGS, f)

        with open(config_path, "r") as file:
            data = json.load(file)

        diagram = to_mermaid(data)

        new_filename = f"{os.path.splitext(f)[0]}.mmd"
        with open(os.path.join(WRITE_TO, new_filename), "w") as f:
            f.write(diagram)
