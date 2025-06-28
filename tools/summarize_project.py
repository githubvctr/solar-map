from pathlib import Path
import ast

def main():
    project_root = Path(__file__).resolve().parent.parent
    output_lines = []

    def summarize_file(file_path: Path):
        try:
            source = file_path.read_text()
            tree = ast.parse(source)
        except Exception as e:
            return [f"# Failed to parse {file_path.name}: {e}"]

        lines = [f"## File: {file_path.relative_to(project_root)}"]
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                args = ", ".join(arg.arg for arg in node.args.args)
                docstring = ast.get_docstring(node)
                lines.append(f"- def {node.name}({args}):")
                if docstring:
                    lines.append(f'    """{docstring.strip().splitlines()[0]}"""')
            elif isinstance(node, ast.ClassDef):
                lines.append(f"- class {node.name}:")
                class_doc = ast.get_docstring(node)
                if class_doc:
                    lines.append(f'    """{class_doc.strip().splitlines()[0]}"""')
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_args = ", ".join(arg.arg for arg in item.args.args)
                        method_doc = ast.get_docstring(item)
                        lines.append(f"  - def {item.name}({method_args}):")
                        if method_doc:
                            lines.append(f'      """{method_doc.strip().splitlines()[0]}"""')
        return lines

    for py_file in project_root.rglob("*.py"):
        parts = py_file.relative_to(project_root).parts
        if ".venv" in parts or "tools" in parts or any(p.startswith(".") for p in parts):
            continue
        output_lines.extend(summarize_file(py_file))
        output_lines.append("")

    summary_path = project_root / "project_summary.md"
    summary_path.write_text("\n".join(output_lines))
    print(f"✅ Project summary written to {summary_path}")

if __name__ == "__main__":
    main()