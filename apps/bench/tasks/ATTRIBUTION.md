# Data attribution

`tasks/*/data.jsonl` are seeded, stratified samples of the sources below.

| Task | Source | License | Sample |
|---|---|---|---|
| massive-ja-intent | [MASSIVE 1.1](https://github.com/alexa/massive), ja-JP, Amazon | CC BY 4.0 | test split, up to 5 per intent (288) |
| ja-toxicity | [LLM-jp Toxicity Dataset](https://gitlab.llm-jp.nii.ac.jp/datasets/llm-jp-toxicity-dataset) via [p1atdev/LLM-jp-Toxicity-Dataset](https://huggingface.co/datasets/p1atdev/LLM-jp-Toxicity-Dataset), LLM-jp | CC BY 4.0 | texts up to 1,000 characters, 150 toxic / 150 nontoxic (300) |
| helpsteer2-helpfulness | [HelpSteer2](https://huggingface.co/datasets/nvidia/HelpSteer2) (revision 990b271), NVIDIA | CC BY 4.0 | validation split, prompt and response under 4,000 characters, 60 per helpfulness level (300); `ratings` from its disagreements file |
| gh-gemini-* | public issues and pull requests of [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli), fetched with the Skill's `github.py fetch` | written by their authors on GitHub; authors reduced to their role | see each task's `data.jsonl` |
| gh-ruff-* | public issues and pull requests of [astral-sh/ruff](https://github.com/astral-sh/ruff), fetched with the Skill's `github.py fetch` | written by their authors on GitHub; authors reduced to their role | see each task's `data.jsonl` |

Email addresses and one leaked API key quoted in these texts are replaced with `[email redacted]` and `AIzaSy-REDACTED`; nothing else is changed.

The repository's Apache-2.0 license covers its code, not these data samples, which keep their sources' terms.

`ja-toxicity` contains offensive text by design.
