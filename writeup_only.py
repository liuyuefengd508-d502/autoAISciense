"""LLM-light writeup + review entry point.

When the LLM proxy is rate-limited, this script lets you skip the expensive
ideation / novelty / experiment-loop phases of `launch_scientist.py` and just
do the final two phases:

    1. perform_writeup -> compiles `templates/<exp>/latex/template.tex` into a
       PDF, using `notes.txt` + `experiment.py` + Semantic Scholar / OpenAlex
       citations.
    2. perform_review  -> generates a JSON review.

Prerequisites (already produced by hand or by an earlier run):
  - `templates/<experiment>/run_0/final_info.json`        baseline results
  - `templates/<experiment>/run_1/final_info.json`        improved results
  - `templates/<experiment>/notes.txt`                    description of runs
  - `templates/<experiment>/latex/template.tex`           paper skeleton
  - `templates/<experiment>/ideas.json`                   one entry whose
        Name will be used as the result-folder slug; the script will
        materialise the writeup under
        `results/<experiment>/<timestamp>_<Name>/`.

Environment:
  - OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_API_BASE, OPENALEX_MAIL_ADDRESS

Usage:
    python writeup_only.py --model gpt-5.4 --experiment htr_baseline \\
        --idea elastic_aug --engine openalex
"""

from __future__ import annotations

import argparse
import json
import os
import os.path as osp
import shutil
from datetime import datetime

from ai_scientist.llm import create_client, AVAILABLE_LLMS
from ai_scientist.perform_writeup import perform_writeup
from ai_scientist.perform_review import load_paper, perform_review

# Late imports to avoid pulling aider when the user just wants help text.
from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--experiment", required=True, help="Template folder name under templates/")
    p.add_argument("--idea", required=True, help="Idea Name to look up in templates/<exp>/ideas.json")
    p.add_argument(
        "--model",
        default="gpt-5.4",
        choices=AVAILABLE_LLMS,
        help="Model used for writeup AND review (unless --review-model given)",
    )
    p.add_argument("--review-model", default=None, choices=AVAILABLE_LLMS)
    p.add_argument(
        "--engine",
        default="openalex",
        choices=["semanticscholar", "openalex"],
        help="Citation engine.",
    )
    p.add_argument(
        "--results-dir",
        default=None,
        help="Existing results/<exp>/<timestamp>_<idea>/ folder to reuse. "
        "If omitted, a fresh one is created from templates/<exp>/.",
    )
    return p.parse_args()


def _build_aider_model(model_name: str):
    if model_name == "deepseek-coder-v2-0724":
        return Model("deepseek/deepseek-coder")
    if model_name == "deepseek-reasoner":
        return Model("deepseek/deepseek-reasoner")
    if model_name == "llama3.1-405b":
        return Model("openrouter/meta-llama/llama-3.1-405b-instruct")
    if "gpt" in model_name or "o1" in model_name or "o3" in model_name:
        return Model(f"openai/{model_name}")
    return Model(model_name)


def _load_idea(base_dir: str, idea_name: str):
    with open(osp.join(base_dir, "ideas.json"), "r", encoding="utf-8") as f:
        ideas = json.load(f)
    for idea in ideas:
        if idea.get("Name") == idea_name:
            return idea
    raise SystemExit(
        f"Idea {idea_name!r} not found in {base_dir}/ideas.json. "
        f"Available: {[i.get('Name') for i in ideas]}"
    )


def _materialise_results_dir(base_dir: str, results_root: str, idea_name: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = osp.join(results_root, f"{timestamp}_{idea_name}")
    shutil.copytree(base_dir, folder, dirs_exist_ok=True)
    return folder


def main():
    args = parse_args()
    base_dir = osp.join("templates", args.experiment)
    results_root = osp.join("results", args.experiment)
    if not osp.exists(base_dir):
        raise SystemExit(f"{base_dir} not found.")

    idea = _load_idea(base_dir, args.idea)

    folder_name = args.results_dir or _materialise_results_dir(
        base_dir, results_root, idea["Name"]
    )
    print(f"[writeup_only] Working in {folder_name}")

    # Sanity-check required artefacts.
    must_exist = [
        osp.join(folder_name, "run_0", "final_info.json"),
        osp.join(folder_name, "run_1", "final_info.json"),
        osp.join(folder_name, "notes.txt"),
        osp.join(folder_name, "latex", "template.tex"),
    ]
    missing = [p for p in must_exist if not osp.exists(p)]
    if missing:
        raise SystemExit(
            "Missing prerequisites for writeup:\n  - "
            + "\n  - ".join(missing)
            + "\n\nThis script does not generate runs; produce them first."
        )

    # Build an aider Coder that operates on (experiment.py, latex/template.tex,
    # notes.txt) just like launch_scientist's writeup phase.
    exp_file = osp.join(folder_name, "experiment.py")
    writeup_file = osp.join(folder_name, "latex", "template.tex")
    notes = osp.join(folder_name, "notes.txt")
    fnames = [exp_file, writeup_file, notes]

    io = InputOutput(
        yes=True,
        chat_history_file=osp.join(folder_name, "writeup_aider.txt"),
    )
    main_model = _build_aider_model(args.model)
    coder = Coder.create(
        main_model=main_model,
        fnames=fnames,
        io=io,
        stream=True,            # required for shareapi.cloud-style proxies
        use_git=False,
        edit_format="diff",
    )

    client, client_model = create_client(args.model)

    print(f"[writeup_only] Starting LaTeX writeup (model={args.model}, engine={args.engine})")
    perform_writeup(idea, folder_name, coder, client, client_model, engine=args.engine)
    print("[writeup_only] Writeup done.")

    pdf_path = osp.join(folder_name, f"{idea['Name']}.pdf")
    if not osp.exists(pdf_path):
        print(f"[writeup_only] WARN: expected PDF at {pdf_path}; skipping review.")
        return
    print(f"[writeup_only] PDF: {pdf_path}")

    review_model_name = args.review_model or args.model
    review_client, review_model_id = create_client(review_model_name)
    paper_text = load_paper(pdf_path)
    print(f"[writeup_only] Starting review (model={review_model_name})")
    review = perform_review(
        paper_text,
        model=review_model_id,
        client=review_client,
        num_reflections=2,
        num_fs_examples=1,
        num_reviews_ensemble=1,
        temperature=0.1,
    )
    review_path = osp.join(folder_name, "review.txt")
    with open(review_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(review, indent=4))
    print(f"[writeup_only] Review: {review_path}")
    print(f"[writeup_only] Done. Outputs under {folder_name}")


if __name__ == "__main__":
    main()
