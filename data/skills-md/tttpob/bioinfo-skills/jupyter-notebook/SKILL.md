---
name: jupyter-notebook
description: Search and edit Jupyter notebooks through safe text-based workflows when the assistant should not handle raw .ipynb JSON directly. Use when you need to inspect, search, change, review, or patch a notebook by either searching it through a ripgrep preprocessor or converting it to a readable text notebook with Jupytext and syncing the changes back into the original .ipynb file while preserving outputs when possible.
---

# Jupyter Notebook Search and Editing via Jupytext

## Overview

Use this skill when the task is "search or modify a notebook", but working on raw `.ipynb` JSON directly is not practical.

This skill covers two notebook-safe operations:

1. Search notebook content through `rg` with `scripts/rg_ipynb_preprocessor.py`.
2. Edit notebook content through a temporary Jupytext text representation and sync it back to `.ipynb`.

Default workflow:

1. Search notebook content safely when you need to locate cells or text inside `.ipynb`.
2. Convert the current `.ipynb` notebook into a readable text notebook in a temporary location.
3. Edit the text notebook instead of the `.ipynb`.
4. Sync the edited text back into the original `.ipynb`.

This skill is intentionally narrow. It is not about maintaining paired notebooks long term. It is a bridge for notebook search and editing.

## Quick Start

### Check tool

Before editing a notebook, verify that `jupytext` is available:

```bash
bash scripts/check_jupytext.sh
```

### Export notebook to text

Convert a notebook into a readable Python text notebook in `py:percent` format.
Always pass an explicit output path, and prefer a temporary file under `TMPDIR`:

```bash
tmp_py="${TMPDIR:-/tmp}/notebook.edit.py"
bash scripts/export_text_notebook.sh notebook.ipynb "$tmp_py"
```

### Search notebook content with `rg`

When searching `.ipynb` files, do not search the raw notebook JSON directly. Use the ripgrep preprocessor so the search sees cell sources and text outputs, while base64-heavy outputs are omitted:

```bash
rg --pre ./scripts/rg_ipynb_preprocessor.py --pre-glob '*.ipynb' 'pattern' .
```

This is the preferred search path for notebook content because it avoids noisy matches inside serialized output blobs such as `image/png`.
`rg --pre` executes the preprocessor directly, so the script must be executable.

If you want that behavior to apply to ordinary recursive `rg` runs without repeating `--pre` and `--pre-glob` every time, use a temporary ripgrep config:

```bash
tmp_rg="${TMPDIR:-/tmp}/rg-ipynb-pre.rc"
printf '%s\n' \
  '--pre' \
  './scripts/rg_ipynb_preprocessor.py' \
  '--pre-glob' \
  '*.ipynb' > "$tmp_rg"

RIPGREP_CONFIG_PATH="$tmp_rg" rg 'pattern' .
rm -f "$tmp_rg"
```

With that config in place, `rg 'pattern' .` will automatically preprocess any `.ipynb` files encountered during the search, even though the command itself does not target `*.ipynb` explicitly.

### Sync text back to notebook

After editing the text notebook, update the original `.ipynb`:

```bash
bash scripts/update_ipynb_from_text.sh "$tmp_py" notebook.ipynb
```

If `notebook.ipynb` already exists, the script copies the existing notebook into a temporary workspace and uses Jupytext's `--update --to notebook` flow there so that notebook outputs and metadata are preserved when possible.

If the target `.ipynb` does not exist, the script creates a new notebook with no outputs.

## Standard Workflow

When asked to edit a notebook:

1. Run `bash scripts/check_jupytext.sh`.
2. Create a temporary text path, e.g. `tmp_py="${TMPDIR:-/tmp}/$(basename path/to/notebook.ipynb .ipynb).edit.py"`.
3. Export the target notebook with `bash scripts/export_text_notebook.sh path/to/notebook.ipynb "$tmp_py"`.
4. Read and edit the generated text notebook.
5. Sync changes back with `bash scripts/update_ipynb_from_text.sh "$tmp_py" path/to/notebook.ipynb`.
6. Remove the temporary text file if it is no longer needed.

When asked to search code that could be in a notebook, or when searching notebook content before editing, use:

```bash
rg --pre ./scripts/rg_ipynb_preprocessor.py --pre-glob '*.ipynb' 'pattern' path/to/notebooks
```

For repeated notebook searches in one shell session, you can also point `RIPGREP_CONFIG_PATH` at a temporary config containing the same `--pre` and `--pre-glob` arguments, then run plain commands such as `rg 'pattern' path/to/notebooks`.

## Format Choice

The default text format is `py:percent` because it is easy to read and round-trip safely with Jupytext:

```python
# %%
import pandas as pd

# %%
df.head()
```

The user does not need to manage paired notebooks manually. The `.py` file is usually a temporary editing artifact and should live in `TMPDIR` unless the user explicitly wants to keep it.

## Important Notes

- Prefer editing the generated text notebook, not the raw JSON inside `.ipynb`.
- Prefer searching `.ipynb` through `scripts/rg_ipynb_preprocessor.py`, not through the raw notebook JSON.
- `jupytext --update --to notebook` is the safest default when updating an existing notebook because it updates input cells while preserving outputs and metadata.
- `jupyter` itself is not required for this editing bridge. Only `jupytext` is required.
- If `jupytext` is missing, tell the user and provide installation guidance rather than guessing another conversion path.

## References

- For the exact command behavior, see [references/jupytext-roundtrip.md](references/jupytext-roundtrip.md).
