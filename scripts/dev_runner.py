"""# DEV ONLY - not part of primary execution path.

Local deterministic demo runner for the MED-SCRIBE graph.
"""

from __future__ import annotations

import json
import sys

from dotenv import load_dotenv

from graph.config import get_execution_mode, get_model_name
from graph.graph_builder import build_graph
from graph.state import initial_state, load_schema


DEFAULT_INPUT = "I have had fever, cough, and sore throat for two days."


def main() -> None:
    load_dotenv()
    raw_input = " ".join(sys.argv[1:]).strip() or DEFAULT_INPUT
    mode = get_execution_mode()
    load_schema()
    app = build_graph()
    result = app.invoke(initial_state(raw_input))
    print(f"Execution mode: {mode}")
    if mode == "hybrid":
        print(f"Model: {get_model_name()}")
    print(json.dumps(result["final_output"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
