VENV_DIR ?= .venv
SYSTEM_PYTHON ?= python3
VENV_PYTHON := $(VENV_DIR)/bin/python3
PYTHON := $(if $(wildcard $(VENV_PYTHON)),$(VENV_PYTHON),$(SYSTEM_PYTHON))
TEXBIN_DIR := $(firstword $(dir $(wildcard /Library/TeX/texbin/latexmk)) $(dir $(wildcard $(HOME)/Library/TinyTeX/bin/*/latexmk)))
LATEXMK ?= $(if $(TEXBIN_DIR),$(TEXBIN_DIR)latexmk,latexmk)

.PHONY: setup build-docx revise-docx build-tex check

setup:
	$(SYSTEM_PYTHON) -m venv $(VENV_DIR)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

build-docx:
	$(PYTHON) build_pr_joint_submission.py

revise-docx:
	$(PYTHON) revise_pr_joint_spotting_docx.py

build-tex:
	@command -v $(LATEXMK) >/dev/null 2>&1 || { echo "latexmk not found. Install MacTeX or an equivalent TeX distribution first."; exit 1; }
	cd pr_cas_sc_overleaf && PATH="$(TEXBIN_DIR):$$PATH" $(LATEXMK) -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
	cd els-cas-templates && PATH="$(TEXBIN_DIR):$$PATH" $(LATEXMK) -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build-autoarchival autoarchival_pr_submission.tex

check:
	$(PYTHON) -c "import docx; print('python-docx import: ok')"
	$(PYTHON) -m py_compile build_pr_joint_submission.py revise_pr_joint_spotting_docx.py
