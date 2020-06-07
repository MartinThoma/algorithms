# Core Library modules
import html
import json
from itertools import zip_longest
from typing import Any, Dict, List, Tuple, Iterator

# Third party modules
import black
import requests

# First party modules
import blacken_docs


def main(user_id: str):
    for answer in get_answers(user_id):
        print(answer)
        filepath = write_answer(answer)
        print(filepath)

        fixed_md = improve_markdown(answer["body_markdown"])

        show_side_by_side(html.unescape(answer["body_markdown"]), fixed_md)
        apply_changes = get_bool("Do you want to apply those changes? [y/N]: ")
        if apply_changes:
            update_changes(answer["answer_id"], fixed_md)
        print("=" * 80)


def improve_markdown(markdown: str) -> str:
    """Improve markdown."""
    md_text = html.unescape(markdown)
    md_text = convert_code_block_style(md_text)
    fixed_md, _ = blacken_docs.format_str(
        md_text, black.FileMode(target_versions="3.6", line_length=79)
    )
    return fixed_md


def update_changes(answer_id: str, markdown: str):
    """Write `markdown` to `answer_id`. TODO."""
    print(f"update:{answer_id}")


def get_bool(text: str) -> bool:
    val = input(text).lower()
    while val not in ["y", "n"]:
        val = input(text).lower()
    return val == "y"


def show_side_by_side(orig_md: str, fixed_md: str):
    orig_lines = orig_md.split("\r\n")
    fixed_lines = fixed_md.split("\n")
    max_orig = max(len(el) for el in orig_lines)
    for orig, fixed in zip_longest(orig_lines, fixed_lines, fillvalue=""):
        print(f"{orig:<{max_orig}} | {fixed}")


def convert_code_block_style(markdown: str) -> str:
    lines = markdown.replace("\r", "").split("\n")
    line_numbers = [
        lineno
        for lineno, line in enumerate(lines)
        if line.startswith(" " * 4) or line.strip() == ""
    ]
    print(f"line_numbers={line_numbers}")
    blocks = get_blocks(line_numbers)
    if len(blocks) > 0:
        lines = adjust_blocks(lines, blocks)
    return "\n".join(lines)


def adjust_blocks(lines, blocks: List[Tuple[int, int]]):
    print(f"blocks={blocks}")
    for start, end in sorted(blocks, reverse=True):
        total = "".join(lines[start:end]).strip()
        if total == "":
            # The block is empty - skip it
            continue

        while lines[start].strip() == "":
            # The first line is empty - crop to the code
            start += 1

        while lines[end].strip() == "":
            # The last line is empty - crop to the code
            end -= 1

        if lines[start - 1].strip() == "":
            for i in range(start, end + 1):
                lines[i] = lines[i][4:]
            lines.insert(end + 1, "```")
            lines.insert(start, "```python")
    return lines


def get_blocks(line_numbers: List[int]) -> List[Tuple[int, int]]:
    """

    Examples
    --------
    >>> get_blocks([1, 2, 4, 5, 6, 7, 8, 10, 12, 14, 15, 16, 18])
    [(1, 2), (4, 8), (10, 10), (12, 12), (14, 16), (18, 18)]
    """
    start = None
    end = None
    blocks = []
    for lineno in line_numbers:
        if start is None or end is None:
            start = lineno
            end = lineno
        else:
            if lineno == end + 1:
                end = lineno
            else:
                blocks.append((start, end))
                start = lineno
                end = lineno
    if start is not None and end is not None:
        blocks.append((start, end))
    return blocks


def write_answer(answer: Dict[str, Any]) -> str:
    filepath = f"{answer['answer_id']}.txt"
    with open(filepath, "w") as f:
        f.write(html.unescape(answer["body_markdown"]))
    return filepath


def get_answers(user_id: str, page: int = 1) -> Iterator[Dict[str, Any]]:
    api_url = "https://api.stackexchange.com/2.2"
    has_more = True
    while has_more:
        url = (
            f"{api_url}/users/{user_id}/"
            f"answers?page={page}&pagesize=10&order=desc&min=1"
            f"&sort=votes&site=stackoverflow&filter=!-.EwD-_LEwMY"
        )
        r = requests.get(url)
        data = json.loads(r.text)
        yield from data["items"]
        has_more = data["has_more"]
        page += 1


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    main(user_id="562769")
