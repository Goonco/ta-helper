import os
import json
from src import config

import nbformat
from nbclient import NotebookClient

from src.data_class import Result


class Runner:
    """Run notebooks with a single input."""

    def __init__(self, inputs):
        with open(config.INPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(inputs, f, ensure_ascii=False, indent=2)

    def run(self, filepath):
        with open(filepath) as f:
            nb = nbformat.read(f, as_version=4)

        for cell in nb.cells:
            self._modify_cell(cell)

        client = NotebookClient(nb, timeout=20, kernel_name="python3")
        client.execute()

        results = []
        for cell in filter(lambda cell: cell.cell_type == "code", nb.cells):
            for output in cell.get("outputs", []):
                if output.output_type == "stream":
                    text = output.text
                elif output.output_type == "execute_result":
                    text = output["data"].get("text/plain", "")
                elif output.output_type == "error":
                    text = f"{output['ename']}: {output['evalue']}"
                results.append(Result(output.output_type, text))
        return results

    def clean_up(self):
        if os.path.exists(config.INPUT_PATH):
            os.remove(config.INPUT_PATH)
        # ToDo : writefile remove

    def _modify_cell(self, cell):
        if cell.cell_type != "code":
            return

        if "input(" not in cell.source:
            return

        lines = cell.source.splitlines()
        new_lines = []

        if lines and lines[0].strip().startswith("%%writefile"):
            new_lines.append(lines[0])
            new_lines.append("from src.fake_input import fakeInput")
            new_lines.extend(
                line.replace("input(", "fakeInput.fake_input(") for line in lines[1:]
            )
        else:
            # 그냥 맨 위에 import 삽입
            new_lines.append("from src.fake_input import fakeInput")
            new_lines.extend(
                line.replace("input(", "fakeInput.fake_input(") for line in lines
            )

        cell.source = "\n".join(new_lines)
