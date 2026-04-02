# Notebook findings summary

This document summarizes the main findings from the executed notebooks in `notebooks/`.

Executed notebooks:
- `notebooks/01_corpus_exploration.ipynb`
- `notebooks/02_seed_term_analysis.ipynb`
- `notebooks/03_corpus_audit.ipynb`
- `notebooks/04_detector_review.ipynb`
- `notebooks/05_iterative_insight_analysis.ipynb`

## Execution status

All notebooks executed successfully after normalizing notebook cell IDs and running them inside an isolated virtual environment dedicated to notebook execution.

## Corpus and validation-bundle context

The iterative insight notebook confirmed the default validation bundle is substantial enough for broad analysis:

- validation root: `artifacts/chat-analysis/validation/full-smoke`
- primary analytical view: `user_nl_root_only`
- comparison view: `combined_nl_root_plus_subagent`
- detector runs: 7
- report sections: 288
- scoped sessions: 716
- unknown record shapes: 2640
- ambiguous items: 2640

This means the current bundle supports meaningful pattern discovery, but every conclusion should be interpreted in the context of a sizable ambiguous pool and the repository’s root-scoped default analysis policy.

## Scope effects are large

The notebook’s baseline comparison showed a strong scope effect when including assistant natural language and subagent sessions:

- `user_nl_root_only`: 1755 included rows, 31 projects, 690 sessions
- `combined_nl_root_plus_subagent`: 7906 included rows, 31 projects, 690 sessions
- row expansion factor: 4.5x
- raw occurrence delta: 6151
- distinct evidence delta: 6151

Interpretation:
- expanding to the broader comparison view mostly increases evidence density, not session coverage
- root-only user language remains the cleanest lens for user-intent analysis
- subagent-inclusive analysis is valuable as a sensitivity check, but it materially changes the amount of evidence in play

## The highest-signal recurring findings are quality and failure oriented

Top ranked findings from `notebooks/05_iterative_insight_analysis.ipynb` were:

1. `Output quality issue: format`
   - score: 1913.0
   - distinct sessions: 205
   - distinct projects: 18
2. `Agent failure signal: error`
   - score: 1810.0
   - distinct sessions: 172
   - distinct projects: 19
3. `Correction/frustration pattern: wrong`
   - score: 1652.0
   - distinct sessions: 148
   - distinct projects: 16
4. `Output quality issue: brief`
   - score: 1405.0
   - distinct sessions: 145
   - distinct projects: 16
5. `Repeated change request cluster: shared preamble critical rules`
   - score: 1190.0
   - distinct sessions: 132
   - distinct projects: 1

Interpretation:
- the most widespread issues are not niche workflow quirks; they are broad quality and execution breakdown signals
- formatting problems and explicit failure/error patterns recur across a large fraction of the corpus
- correction/frustration language is also highly recurrent, which suggests many runs require user steering or repair

## Detector-level pattern synthesis

The strongest detector/category aggregates were:

- `workflow_patterns`
  - sections: 113
  - total score: 5769.0
  - average distinct sessions: 4.95
- `output_quality`
  - sections: 7
  - total score: 4836.0
  - average distinct sessions: 69.14
- `refinement_requests`
  - sections: 104
  - total score: 4758.0
  - average distinct sessions: 4.4
- `corrections_frustrations`
  - sections: 9
  - total score: 4298.0
  - average distinct sessions: 44.89
- `change_requests`
  - sections: 42
  - total score: 3950.0
  - average distinct sessions: 9.52
- `agent_failures`
  - sections: 8
  - total score: 3919.0
  - average distinct sessions: 44.12

Interpretation:
- `workflow_patterns` and `refinement_requests` dominate by count, meaning the corpus contains many specific but narrower recurring workflow motifs
- `output_quality`, `corrections_frustrations`, and `agent_failures` dominate by breadth, meaning fewer categories explain more cross-session pain
- this suggests two complementary improvement tracks:
  - broad fixes for quality/failure recurrence
  - narrower workflow improvements for common operational loops

## Some evidence items act as cross-detector bridge signals

The traceability pass found evidence rows reused across many sections and detectors. Examples:

- evidence `0a66af700e208d16eea33da3946f28ff203471ec533303901661ce321ca880c0`
  - referenced by 7 sections
  - appears across all 7 detector families in the shortlist sample
- evidence `682b2260ce820b97f2e6f28f68d24328d12ecccb73fa770cf0118260497efd5f`
  - referenced by 7 sections
  - also spans all 7 detector families in the shortlist sample

Interpretation:
- certain user messages or turns are not just isolated symptoms; they simultaneously signal failure, quality, refinement, and workflow issues
- these bridge records are especially valuable for manual review because improving the underlying interaction pattern could reduce multiple detector categories at once

## Repeated instruction and prompt-template effects are real but more concentrated

The detector review notebook showed a repeated instruction finding with this recurrence:

- detector: `repeated_instructions`
- view: `user_nl_root_only`
- distinct sessions: 12
- raw occurrences: 21
- distinct projects: 6

The iterative notebook also elevated concentrated change-request clusters such as:
- `Repeated change request cluster: shared preamble critical rules`
- `Repeated change request cluster: senior adversarial reviewer performing`

Interpretation:
- prompt and preamble reuse is present and detectable
- compared with output quality and failure signals, these repeated instruction clusters appear more concentrated, but they are still strong candidates for tooling or prompt-template normalization
- one repeated change-request cluster is highly concentrated in a single project, suggesting localized workflow standardization opportunities

## Seed-term notebook confirms pipeline is a central analysis theme

The seed-term notebook run for `pipeline` showed:

- direct recurrence:
  - raw occurrences: 473
  - distinct evidence: 473
  - distinct sessions: 358
  - distinct projects: 16
- expansion recurrence:
  - raw occurrences: 25
  - distinct evidence: 25
  - distinct sessions: 10
  - distinct projects: 6

Interpretation:
- pipeline-related work is a major recurring topic across the corpus
- direct mentions are widespread and cross-project
- the expansion set is much smaller, which suggests the explicit term itself is doing most of the retrieval work in this slice

## Corpus audit confirms large excluded and ambiguous volumes

The corpus audit notebook and the iterative notebook both highlighted the same constraint: most canonical evidence is not in the primary user-NL slice.

Notable counts from the validation bundle:
- `excluded_default`: 70706
- `included_primary`: 1755
- `included_secondary`: 6151
- `ambiguous`: 2640
- unknown record shapes: 2640

Interpretation:
- the primary analytical view is intentionally narrow relative to total evidence volume
- this is good for focused user-intent analysis, but it means many operational, tool, system, and ambiguous records are excluded by design
- any future reporting or notebook work should keep these corpus boundaries visible instead of treating the primary view as the whole system

## Practical conclusions

Based on the executed notebooks, the strongest current conclusions are:

1. **Broadest recurring problems are output quality and failure handling.**
   - Formatting, brevity/quality complaints, and explicit failure markers recur across many sessions and projects.

2. **Workflow refinement signals are numerous but individually narrower.**
   - There are many recurring workflow patterns and refinement requests, but each tends to be less cross-session than the major quality/failure issues.

3. **A small number of bridge evidence items explain multiple problem categories.**
   - These should be prioritized for manual inspection and design changes because they link multiple detector families.

4. **Subagent-inclusive views dramatically increase evidence volume without expanding session coverage.**
   - Use them as a sensitivity lens, not as a drop-in replacement for root-only user analysis.

5. **Repeated prompt/preamble clusters are real and likely worth normalization.**
   - Especially where they are project-concentrated, they may reflect reusable templates or workflow conventions that should be cleaned up or standardized.

## Recommended next steps

- Review the top bridge evidence anchors surfaced by `05_iterative_insight_analysis.ipynb`
- Triage the highest-ranked `output_quality` and `agent_failures` sections first
- Audit project-concentrated repeated change-request clusters for prompt-template cleanup
- Consider a follow-up notebook or report that groups findings by project to separate global issues from team-local workflow patterns
