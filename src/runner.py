import os
import json
from src import config
from src.util import safe_remove, check_time

import nbformat
from nbclient import NotebookClient

from src.data_class import Result
from typing import List


class Runner:
    """Run notebooks with a single input."""

    def __init__(self, inputs):
        self.inputs = inputs
        with open(config.INPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(inputs, f, ensure_ascii=False, indent=2)
        self.created_files_and_dirs = set()

    @check_time
    def run(self, filepath) -> List[Result]:
        # print(f"Run {filepath} with {self.inputs}")
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

    def _modify_cell(self, cell):
        if cell.cell_type != "code":
            return

        lines = self._handle_magic_commands(cell)

        if "input(" not in cell.source:
            return
        new_lines = []
        new_lines.extend(self._handle_input_replacement(lines[len(new_lines) :]))
        cell.source = "\n".join(new_lines)

    def _handle_magic_commands(self, cell):
        lines = cell.source.splitlines()
        if len(lines) == 0: return []
        first_line = lines[0].strip()

        # %% is always in the first line
        if first_line.startswith("%%writefile"):
            file_name = first_line.split(" ", 1)[1]
            self.created_files_and_dirs.add(file_name)

        # % may be in the middle of the cell
        if "%mkdir" in cell.source:
            for line in lines:
                line = line.strip()
                if line.startswith("%mkdir"):
                    dir_name = line.split(" ", 1)[1]
                    self.created_files_and_dirs.add(dir_name)

        return lines

    def _handle_input_replacement(self, lines: list[str]) -> list[str]:
        new_lines = []
        for line in lines:
            if "input(" in line:
                new_lines.append("from src.fake_input import fakeInput")
                new_lines.append(line.replace("input(", "fakeInput.fake_input("))
            else:
                new_lines.append(line)
        return new_lines
