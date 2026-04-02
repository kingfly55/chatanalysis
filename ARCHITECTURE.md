# Chat Analysis System Architecture

## Status

This document is the **architecture phase** of a three-step pipeline:

1. **Architecture** — define what the system is, what responsibilities it has, what boundaries it enforces, and how the major parts fit together
2. **Implementation plan** — translate the architecture into an ordered execution plan with concrete milestones, files, and verification steps
3. **Implementation** — build the repository and code according to the approved plan

This document intentionally stays at the architectural level. It does **not** specify code-level implementation details, concrete algorithms, file-by-file tasks, or low-level execution mechanics except where needed to define system boundaries.

---

## 1. Purpose

The system will analyze exported Claude Code chat history in order to surface **recurring, actionable patterns** in how the user works with agents.

Its purpose is not to automate coding directly. Its purpose is to help the user answer questions such as:

- What instructions am I repeating often enough that they should become durable rules?
- What recurring workflows should become reusable skills or higher-level automation?
- Where do I repeatedly correct agents, indicating missing guardrails or missing memory?
- What kinds of outputs repeatedly miss the mark?
- What patterns show up only in certain projects, and what patterns show up across projects?
- What themes appear when starting from a seed term such as `pipeline` or `testing`?
- How do user-side patterns differ from assistant-side patterns or subagent-heavy workflows?

The system should produce **high-signal, traceable evidence** that helps the user decide what to operationalize into skills, CLAUDE.md guidance, memory, or workflow changes.

The system itself is not responsible for automatically writing those downstream artifacts, deciding which findings matter without human review, or acting like a generic chat viewer or one-shot reporting script. It exists to provide a reusable analysis environment for iterative discovery, comparison, evidence-backed judgment, and repeated refinement over the same underlying corpus.

---

## 2. Architectural principles

The architecture is guided by two source constraints:

1. The problem specification establishes the product goal: analyze the user’s Claude Code history, treat user messages as the primary signal, preserve traceability, and support exploratory decision-support rather than black-box automation.
2. The harness-engineering reference establishes the repository philosophy: documentation is the system of record, agent legibility matters, and boundaries should be explicit.

From those constraints, the system should follow these principles.

### 2.1 User-first evidence

The primary analysis target is the user’s own natural-language messages.

Assistant messages, subagent output, and tool-generated artifacts are useful, but they are secondary evidence layers. The architecture must make it easy to analyze the user corpus alone, then optionally enrich it with agent-side or subagent-side context without collapsing those roles into one undifferentiated corpus.

### 2.2 Normalize before analysis

Raw JSONL transcripts are not a stable analysis interface.

The system should establish a normalized internal representation of transcript evidence before any search, clustering, embedding, prompting, comparison, or reporting happens. That normalized layer is the contract that all later analysis depends on, even as transcript formats vary across sessions or export versions.

### 2.3 Filter semantics are architectural, not incidental

In this domain, inclusion and exclusion rules are not a minor implementation detail. They define the meaning of the corpus.

The distinction between:
- user-authored text
- assistant natural-language text
- tool calls
- tool results
- thinking blocks
- protocol/meta chatter
- operational transcript records
- subagent-related material

must be explicit in the system architecture.

### 2.4 Traceability is a first-class invariant

Every analysis result must be traceable back to:
- source project
- source session
- source transcript path
- source event/message location
- exact evidence excerpt
- the scope and analysis mode that surfaced it
- the recurrence basis used to interpret it

This is not just a reporting concern. It is a core architectural requirement because the system is intended to support decision-making, review, and refinement.

### 2.5 Analysis surfaces should share one corpus

Search, notebook exploration, LLM-based analysis, clustering, and reporting should all operate over the same normalized evidence substrate. The architecture should avoid creating one representation for search, another for notebooks, and another for LLM prompting.

The same principle applies to scope and filter definitions: the system should support comparable views over one corpus rather than a separate interpretation path for each consumer. The same evidence identities, role boundaries, and recurrence accounting rules should follow the evidence across all consumers.

### 2.6 Local-first operation

Basic ingestion, filtering, search, and analysis must work locally over exported history. Optional higher-level analysis layers may use models or embeddings, but the system should not depend on external services for its core operating mode.

Optional remote services may enrich interpretation, but they must not be required in order to inspect evidence, compare slices, or answer the core repeated-instruction and workflow questions defined by the problem specification.

### 2.7 Progressive disclosure

The system should support multiple levels of interaction:
- broad corpus exploration
- filtered search
- evidence inspection
- comparative slicing
- higher-order pattern analysis
- report generation

Users and agents should be able to move from broad discovery to fine-grained evidence inspection without changing mental models, and without losing the link between summary-level claims and concrete examples.

---

## 3. Problem framing

Claude Code transcript exports are not clean conversational text logs. They are structured operational artifacts that mix:

- user messages
- assistant messages
- tool activity
- subagent sessions
- system records
- local command wrappers
- IDE/protocol metadata
- snapshots and other auxiliary transcript events

That means the system is not simply a search engine over text files. It is a **corpus interpretation system**.

The real architectural problem is not merely storing or searching transcripts. It is converting a large, noisy body of human-agent interaction history into a form that can reveal recurring, inspectable, and actionable patterns.

The architectural challenge is to separate:
- the parts that represent meaningful human-agent interaction
- the parts that represent operational machinery
- the parts that should be searchable by default
- the parts that should be available only as supporting evidence
- the parts that matter for user-first analysis versus assistant-side comparison

This distinction is what enables trustworthy downstream analysis.

The architecture must also preserve enough of transcript reality that later inspection remains honest. That means preserving project and session boundaries, sequence and context, subagent lineage when observable, and explicit ambiguity when source records cannot be interpreted confidently. Over-normalizing the corpus into context-free text snippets would make later findings easier to generate but harder to trust.

---

## 4. System scope

### 4.1 In scope

The system is responsible for:

- discovering exported transcript data across project directories
- understanding session structure, including subagent sessions
- normalizing transcript records into analysis-ready evidence
- applying explicit inclusion/exclusion policies
- preserving enough provenance, ordering, and context for later inspection
- supporting user-only, assistant-only, and comparison-oriented analysis views
- supporting seed-term, exploratory, and comparative search
- supporting project-, session-, subset-, and subagent-scoped exploration
- supporting notebook-based and interactive exploration
- supporting optional embedding-based comparison and clustering
- supporting optional LLM-driven analysis over filtered evidence sets
- supporting recurrence analysis at multiple levels such as evidence occurrences, distinct sessions, and distinct projects
- surfacing unknown, ambiguous, or excluded transcript material for debugging and corpus-quality review rather than silently discarding it
- producing traceable reports for pattern categories such as repeated instructions, workflow patterns, corrections/frictions, workflow refinement requests, agent failures, and output-quality issues
- surfacing evidence-backed candidates for durable rules, memory, skills, workflow improvements, or review patterns without automatically enacting them
- supporting a reusable analysis environment rather than only a one-shot batch report

### 4.2 Out of scope

The system is not responsible for:

- auto-generating skills, CLAUDE.md rules, or workflow files
- modifying the original transcript data
- replacing manual judgment about which patterns deserve operationalization
- performing unrestricted black-box analysis with no traceability
- coupling the repository to one specific external model vendor
- flattening every transcript element into one undifferentiated search space and calling that analysis
- treating raw transcript browsing as the end goal
- assuming one perfect prompt, one clustering strategy, or one report will solve the problem completely
- silently converting ambiguous evidence into false certainty

### 4.3 Deferred by design

The following are intentionally left for later phases:

- exact repository scaffold and package structure
- concrete command-line interface shape
- detailed implementation sequencing
- precise prompt designs for LLM analysis
- exact clustering or scoring algorithms
- concrete persistence format choices for caches and derived artifacts
- exact UX decisions for notebooks, saved analyses, or report presentation

Those belong to the implementation-planning phase, not to architecture.

---

## 5. Architectural outcome

At a high level, the system should behave like a layered analysis platform that turns raw transcript history into reusable, inspectable evidence for human decision-making.

### 5.1 Layered model

The architecture is organized into six logical layers:

1. **Source layer** — exported Claude Code history and related metadata
2. **Discovery layer** — identifies what data exists, how it is grouped, and what scopes are available
3. **Normalization layer** — interprets raw transcript records into stable evidence units
4. **Analysis substrate** — filtered, queryable, comparable corpus views built from normalized evidence
5. **Analysis consumers** — search, notebooks, embeddings, LLM analyses, reports
6. **Decision-support outputs** — human-readable findings, evidence packs, and other traceable outputs for human review

These layers should be understood as architectural roles, not necessarily as separate runtime processes.

---

## 6. Source layer

The source layer is the exported transcript corpus under `projects/` and related metadata artifacts such as `sessions-index.json`.

### 6.1 Source characteristics

The source corpus is heterogeneous:

- many projects
- many sessions per project
- large JSONL files
- optional session metadata indexes
- nested subagent session files
- records that are conversational, operational, and protocol-oriented
- possible schema variation, partial metadata, or export differences across time
- possible missing, partial, or imperfect exports that still need to be analyzed as faithfully as possible

### 6.2 Architectural meaning of the source layer

The source layer is **authoritative** but **not analysis-ready**.

It is authoritative because it is the ground truth record of what happened.
It is not analysis-ready because its structure is optimized for interaction/runtime capture, not for semantic analysis.

The architecture should therefore assume that source records may be noisy, unevenly structured, and only partially helpful until discovery and normalization interpret them. It should also assume that some records will remain ambiguous, and that those ambiguities should be surfaced as explicit quality or interpretation caveats rather than normalized away invisibly.

### 6.3 Source immutability

The architecture should treat exported transcripts as read-only source data. Derived artifacts may be created elsewhere, but the original corpus is not to be mutated, rewritten, or “cleaned in place.”

Any derived indexes, caches, or evidence stores created later should be subordinate to this source layer and should always be traceable back to the immutable transcript corpus.

---

## 7. Discovery layer

The discovery layer answers:

- what projects exist?
- what sessions exist under each project?
- which sessions are root sessions versus subagent sessions?
- what metadata is available without fully parsing transcript bodies?
- what candidate scopes should downstream analysis operate over?

### 7.1 Responsibilities

The discovery layer is responsible for creating a navigable map of the corpus.

It should understand:
- project identity
- session identity
- transcript path
- subagent/session relationships when observable
- available session metadata from index files when present
- available temporal or ordering metadata when present
- enough scope metadata to support later filtering, comparison, and inspection

Discovery should also preserve stable identifiers for the discovered units of the corpus so that later normalization, inspection, and reporting can refer to the same project and session scopes consistently.

### 7.2 Why discovery is separate from normalization

Discovery should remain distinct from normalization because the system needs lightweight ways to:
- enumerate available data
- select analysis scope
- support project/session filtering
- support exploratory workflows
- compare slices before paying the cost of full semantic interpretation

without requiring every downstream surface to immediately parse the full body of every transcript.

This separation also matters for scale. A large corpus should remain explorable at the level of projects, sessions, and metadata even before a full semantic pass is run over every event.

### 7.3 Architectural role of session indexes

Optional index artifacts such as `sessions-index.json` should be treated as **metadata accelerators**, not as the canonical semantic source.

They can improve discoverability and speed, but they should not replace transcript parsing as the basis for actual content interpretation. If indexes are absent, incomplete, or inconsistent, discovery should still degrade gracefully rather than redefining corpus meaning.

If index-derived metadata conflicts with transcript-derived evidence later, the architecture should preserve that discrepancy as an inspectable inconsistency rather than silently preferring convenience over source truth.

---

## 8. Normalization layer

The normalization layer is the center of the architecture.

Its job is to transform raw transcript events into a stable semantic representation that downstream analysis can trust.

### 8.1 Why normalization is the center

The major ambiguity in the source data is that top-level record type does not always equal semantic meaning.

For example, a record that appears under the user channel may contain tool-generated output rather than human-authored text. Likewise, assistant activity may mix natural language with tool calls and other operational content.

Because of this, downstream consumers cannot safely analyze raw records directly.

The architecture should also allow for the possibility that one raw event yields zero, one, or multiple evidence units depending on how much semantically meaningful text it contains.

### 8.2 Normalized evidence as the system contract

The architecture should define a canonical evidence representation with enough information to answer:

- who produced this?
- what kind of content is it?
- should it be included in a given analysis mode?
- where did it come from?
- how can a human inspect it later?
- what surrounding context or session role helps interpret it?
- how should it be counted when reasoning about recurrence?

This normalized evidence model is the shared contract for:
- search
- notebook exploration
- embedding generation
- LLM prompting
- reporting
- later pattern detectors

At the architectural level, every evidence unit should carry stable provenance, semantic classification, inclusion/exclusion status, enough identity to be referenced repeatedly across different analysis runs, and enough sequence or context metadata to reconstruct its place inside the session when needed.

Where transcript semantics are uncertain, the normalized representation should preserve that uncertainty explicitly through ambiguity or confidence metadata rather than forcing false precision.

### 8.3 Required semantic distinctions

The normalization layer must explicitly distinguish among at least these semantic classes:

- human-authored user natural language
- assistant natural-language output
- tool calls
- tool results
- thinking/reasoning blocks
- protocol/meta chatter
- system/operational records
- snapshot/state records
- unknown or not-confidently-classified material

It must also preserve role- and session-level distinctions that matter to interpretation, such as whether the evidence came from a root session or a subagent-related context.

Even if later implementations refine the taxonomy, the architecture depends on these category boundaries existing.

### 8.4 Inclusion and exclusion metadata

Normalization is not only about extracting text. It is also about tagging evidence with the information needed to decide whether it belongs in:

- the primary analysis corpus
- secondary evidence layers
- forensic/debug views only

This means the normalized representation must carry both semantic classification and inclusion rationale.

That rationale matters because the user must be able to understand not only why a piece of evidence was included, but also why a potentially relevant-looking item was excluded by default.

Excluded or ambiguous material should not silently disappear. The architecture should preserve it as inspectable material so corpus-quality assumptions can be tested and the default filters can be challenged when needed.

---

## 9. Analysis substrate

The analysis substrate is the reusable filtered corpus built on top of normalized evidence.

It is the layer that makes the system useful across many analysis modes without repeating corpus interpretation logic.

### 9.1 Purpose

The analysis substrate provides consistent ways to derive views such as:

- user-only natural-language corpus
- assistant-only natural-language corpus
- combined natural-language corpus with role labels
- included evidence only
- included plus excluded evidence for debugging
- root-session-only views
- root-plus-subagent views
- project-scoped views
- session-scoped or subset-scoped views
- comparison-ready views across projects, periods, or session types
- seed-term-scoped views
- recurrence-ready views that preserve distinct session and project boundaries

### 9.2 Architectural value

Without this substrate, each consumer would need to define its own filtering rules. That would fragment semantics, produce inconsistent results, and make the system difficult to trust.

With this substrate, all analysis tools inherit the same corpus meaning.

This layer should also make analysis scope explicit and reusable so that the same slice can be searched, clustered, prompted over, and reported on without silently changing what the corpus contains.

It should additionally preserve the counting semantics needed for pattern discovery. Recurrence in this domain may need to be understood at several levels — raw occurrences, distinct sessions, distinct projects, or distinct workflow contexts. The substrate should therefore preserve those boundaries so that a long or repetitive single session does not masquerade as a broadly recurring pattern.

### 9.3 Default versus non-default views

The architecture should distinguish between:

- **default views** — high-signal corpora intended for normal use
- **non-default views** — expanded or forensic views intended for specialized inspection

Default views should prioritize semantic clarity.
Non-default views should preserve access to excluded material without polluting the main corpus.

Default views are starting points, not hidden truth. The architecture should make it easy to widen or narrow a view deliberately while preserving clarity about what changed, why it changed, and how that affects the interpretation of any findings.

---

## 10. Analysis consumers

Once the substrate exists, multiple consumers can sit on top of it without redefining corpus logic.

### 10.1 Search and exploration

One consumer is interactive search.

This surface should allow users to:
- search only user messages
- search only assistant messages
- apply project/session/subagent filters
- start from seed terms
- inspect examples with traceability
- understand why a result was included or excluded
- move from a result to the supporting source context quickly
- compare how a theme appears across different scopes
- inspect representative examples alongside recurrence signals rather than only isolated hits

Architecturally, search is not special. It is one consumer of the shared evidence substrate.

### 10.2 Notebook analysis

A second consumer is notebook-based exploration.

This is important because many useful questions are exploratory and comparative rather than fully productized.

Notebook access should allow the user to:
- load the normalized corpus into a tabular analysis environment
- group and slice by semantic labels
- compare projects, periods, or session classes
- manually inspect clusters, outliers, and repeated phrases
- prototype analysis ideas before turning them into durable workflows
- inspect included, excluded, and ambiguous evidence without redefining the underlying semantics

Architecturally, notebook use should be treated as a first-class consumer, not a side effect.

### 10.3 Embedding and clustering analysis

A third consumer is similarity-based analysis.

This layer exists to support questions like:
- what user instructions are semantically similar but phrased differently?
- what repeated correction themes cluster together?
- what sessions share similar workflow language?
- what kinds of agent responses form recurring families?
- what themes only become visible when looking across many sessions rather than exact string matches?

The architectural rule here is that embeddings should operate over **normalized natural-language evidence**, not over raw transcript lines.

This preserves signal quality and avoids contaminating semantic comparison with tool chatter and transcript machinery. Clusters or similarity results must still resolve back to representative examples, session/project distribution, and source-backed inspection.

### 10.4 LLM-driven analysis

A fourth consumer is prompted LLM analysis.

This supports higher-order interpretation tasks such as:
- classify repeated instruction patterns
- summarize correction themes
- compare prompt variants over the same filtered corpus
- synthesize candidate workflow categories
- review clusters or search result sets for latent structure
- compare user-side and assistant-side evidence slices without collapsing them

Architecturally, LLM-driven analysis should be treated as a consumer of prepared evidence slices, not as a replacement for normalization.

Prompted analyses should inherit the same scope, role labeling, and inclusion policies as every other consumer. If the same evidence slice is analyzed with different prompts or models, that should constitute different interpretations over the same evidence, not different hidden corpora.

### 10.5 Reporting

A fifth consumer is reporting.

Reports should convert analysis outputs into decision-support artifacts that answer:
- what pattern was found?
- how frequent is it?
- where does it appear?
- what evidence supports it?
- what comparisons sharpen or qualify the claim?
- how should a human inspect or verify it?
- what candidate operationalization does it suggest, if any?

Reports should remain tied to the shared substrate so they can be reproduced, questioned, and refined.

When relevant, reporting should preserve recurrence at more than one level, such as raw mentions, distinct sessions, and distinct projects, so the user can judge whether a finding is truly broad, merely repetitive, or concentrated in one context.

---

## 11. Decision-support outputs

The final layer of the architecture is the output layer: durable findings meant for human judgment.

### 11.1 Purpose of outputs

Outputs exist to support decisions, not to terminate the system.

A good output should let the user do one of the following:
- accept a pattern as meaningful
- reject it as noise
- request refinement of the analysis
- compare it against an alternate slice or interpretation
- use the evidence to design a skill, memory rule, or workflow improvement

A good output should also make it straightforward to revisit the same finding later as the corpus grows or the analysis framing changes.

### 11.2 Output types

The architecture should support outputs such as:
- ranked pattern reports
- scoped evidence packs
- comparative slices across projects or periods
- seed-term exploration summaries
- cluster inspection summaries
- prompt-comparison outputs from LLM analyses
- evidence-backed candidate operationalization queues for later human review

### 11.3 Architectural requirement for explainability

Every output should remain explainable in terms of:
- scope used
- corpus filters used
- evidence included
- evidence excluded by design
- analysis mode used
- representative examples and recurrence signals
- major caveats, ambiguities, or concentration effects that materially affect interpretation

This is necessary because the user will iterate on the system, and those iterations require understanding why a result appeared.

---

## 12. Core domain concepts

The architecture depends on a small set of domain concepts.

### 12.1 Project

A project is the top-level scope of exported transcript history. It is both:
- a unit of organization in the source corpus
- a unit of analysis scoping

A project may also represent a distinct working context whose patterns should be comparable against other projects rather than immediately merged away.

### 12.2 Session

A session is a single transcript conversation artifact. Sessions may be root sessions or subagent sessions.

A session is the primary temporal container of evidence and an important recurrence boundary. Many findings should be evaluable not only by how many evidence units exist, but also by how many distinct sessions they span.

### 12.3 Event

An event is a raw transcript record. Not every event is semantically meaningful for analysis, but every piece of evidence originates from one.

Events also provide the positional and contextual anchor points that later inspection relies on.

### 12.4 Evidence unit

An evidence unit is the normalized atomic item that downstream analysis consumes.

It is the most important domain concept in the architecture because it is the bridge between runtime transcript structure and semantic analysis. It must preserve semantic class, role context, source provenance, recurrence-relevant identity, and enough surrounding context that multiple analysis modes can reference the same item without reinterpretation.

### 12.5 Corpus view

A corpus view is a filtered subset of evidence units created for a purpose, such as “user-only natural-language messages with subagents excluded.”

A corpus view should be explicit enough to be reused across search, notebooks, similarity analysis, prompting, and reporting. It should also make clear what counting boundaries apply when interpreting recurrence.

### 12.6 Analysis run

An analysis run is any structured use of a corpus view to produce findings, whether via search, notebook logic, embeddings, or LLM prompting.

Architecturally, an analysis run should have explicit inputs and scope so that findings can be reproduced or compared later.

### 12.7 Finding

A finding is an interpreted output backed by evidence. Findings are not raw data; they are claims supported by traceable evidence.

A useful finding should preserve not just the claim itself, but also the recurrence signal, scope, representative supporting examples, and any major caveats that make the claim inspectable.

---

## 13. Architectural boundaries

To keep the system coherent, the architecture should enforce several boundaries.

### 13.1 Source boundary

Raw exported transcripts stay in the source layer. They are not the operational analysis API.

### 13.2 Semantic boundary

Normalization defines semantic meaning. Downstream consumers do not reinterpret raw transcript structures independently.

Normalization also defines ambiguity status. If source meaning is uncertain, that uncertainty belongs in the shared evidence contract rather than being silently resolved differently by each consumer.

### 13.3 Consumer boundary

Search, notebooks, embeddings, LLM analyses, and reports are consumers of the same substrate. They should not each develop their own incompatible evidence model.

Consumers may derive additional interpretations or features, but they should not redefine core inclusion semantics, role boundaries, or recurrence accounting rules behind the user’s back.

### 13.4 Output boundary

Reports and findings are downstream artifacts. They should not become implicit hidden inputs to core corpus definition.

Candidate findings may inform later analysis refinement, but they must not silently overwrite the canonical meaning of the corpus.

### 13.5 Architecture-versus-implementation boundary

This document defines:
- responsibilities
- data flow shape
- invariants
- conceptual interfaces
- layering

It does not define:
- concrete library selection
- specific classes or functions
- exact CLI syntax
- exact persistence mechanisms
- exact model providers
- exact folder naming beyond broad architectural direction

---

## 14. Canonical flows

The system should support several canonical flows.

### 14.1 Corpus understanding flow

1. Discover projects and sessions
2. Interpret transcript structure
3. Normalize raw events into evidence units
4. Produce inspectable corpus views
5. Validate that included, excluded, and ambiguous material matches architectural expectations

This flow exists to establish trust in the data.

### 14.2 Exploratory analysis flow

1. Select a scope
2. Choose a corpus view
3. Search, inspect, or slice evidence
4. Compare alternative scopes, roles, or subagent settings when useful
5. Refine scope or filters
6. Preserve traceable examples and recurrence signals

This flow is optimized for discovery.

### 14.3 Similarity analysis flow

1. Select normalized natural-language evidence
2. Create semantic representations
3. compare, cluster, or retrieve similar evidence
4. inspect resulting groups against source context and distinct session/project distribution
5. compare recurring themes against exact supporting examples

This flow is optimized for latent pattern discovery.

### 14.4 LLM analysis flow

1. Define a filtered evidence slice
2. apply a prompt or prompt family
3. capture outputs with links to evidence inputs and analysis configuration
4. compare results across prompt variants, models, or scopes
5. preserve enough provenance to revisit or challenge the interpretation later

This flow is optimized for interpretive experimentation.

### 14.5 Reporting flow

1. Select a pattern category or analysis result
2. gather supporting evidence and recurrence signals at the relevant granularity
3. summarize recurrence, scope, and caveats with traceability
4. produce a human-reviewable output

This flow is optimized for decision support.

---

## 15. Default corpus policy

The architecture needs a clear default policy for what counts as analysis-worthy text.

### 15.1 Primary default corpus

The default primary corpus should be:
- user-authored
- natural-language
- non-tool
- non-thinking
- non-protocol
- non-operational

This is the cleanest foundation for repeated-instruction and workflow-pattern analysis.

The important architectural qualifier is that user authorship should be determined semantically after normalization, not assumed solely from a raw channel label.

### 15.2 Secondary default corpus

The default secondary corpus should be:
- assistant-authored natural-language output
- available for comparison and supporting evidence
- separate from the primary corpus by default

This preserves the problem specification’s user-first orientation while still supporting user-versus-assistant comparisons and output-quality analysis.

### 15.3 Non-default corpus material

The following should remain accessible but excluded from primary analysis by default:
- tool calls
- tool results
- thinking content
- system records
- snapshots
- protocol/meta wrappers

This separation is essential because these materials are useful context but poor default semantic targets.

Default exclusion should not mean permanent invisibility. The architecture must preserve access to this material for debugging, context recovery, specialized analyses of failure or workflow mechanics, and validation of whether default filters are hiding something important.

---

## 16. Subagent architecture

Subagent sessions are architecturally significant because they are related to the user’s work but are not the same as the main human-agent interaction channel.

### 16.1 Why subagents need explicit treatment

If subagent transcripts are mixed into the default corpus without distinction, they can distort pattern analysis by overweighting agent-to-agent work relative to direct user instruction.

They can also blur important comparison questions, such as whether certain behaviors are properties of the user’s direct workflow or of subagent-heavy orchestration patterns.

### 16.2 Architectural stance

Subagent sessions should be represented as explicit session types or session roles within the system, not flattened invisibly into the main session stream.

Where parent-child relationships are observable, the architecture should preserve them so that analyses can compare direct interaction workflows against subagent-heavy workflows rather than merely mix the two.

Subagent lineage should therefore be part of the reusable corpus definition, not a hidden implementation detail that only appears in specialized reports.

### 16.3 Default behavior

The architecture should support default exclusion or separate treatment of subagent content, with the ability to re-include it deliberately for broader analyses.

When subagent material is included, its role should remain visible so recurrence and pattern claims can still be interpreted correctly.

---

## 17. Notebook and research posture

The architecture should explicitly support research-style workflows.

### 17.1 Why notebooks matter architecturally

This project is not only a product surface; it is also an analysis workbench. Some of the most valuable pattern discovery will come from exploratory work before a durable analysis is formalized.

### 17.2 Architectural implication

The normalized evidence substrate must be easy to load into research environments without redefining parsing or filtering semantics.

That matters because the user wants to inspect, compare, refine, and experiment over time rather than depend on one fixed report.

Notebook workflows should be able to inspect not only included evidence, but also excluded and ambiguous material, recurrence boundaries, and comparison slices, all while relying on the same authoritative evidence model.

### 17.3 Relationship to durable tooling

Notebook analysis should be able to inform later durable features, but notebooks should not become a shadow semantics layer. The same evidence model and corpus policies must remain authoritative.

---

## 18. LLM analysis posture

The architecture should support LLM-driven analysis as a deliberate, inspectable layer rather than an opaque catch-all.

### 18.1 Why LLM analysis belongs here

Many useful questions are interpretive rather than purely lexical or statistical. LLMs can help identify themes, compare phrasing, categorize patterns, and synthesize repeated instructions.

### 18.2 Architectural constraints on LLM use

LLMs must operate on:
- filtered evidence slices
- stable evidence identities
- explicit scope definitions
- reproducible prompt inputs

This keeps prompted analysis aligned with the rest of the system and makes prompt experimentation practical.

Prompt packages should preserve role distinctions and exclusion choices so that LLMs are not given a flattened or misleading view of the corpus by default.

### 18.3 Prompt experimentation as a first-class concern

The architecture should allow the same evidence slice to be processed with multiple prompts, models, or analysis settings so the user can compare interpretations rather than hard-code one prompt path too early.

### 18.4 Relationship to traceability

LLM outputs must remain linked to the evidence that produced them. An insightful summary with no evidence trace is not sufficient for this system.

LLM analyses should therefore behave as inspectable interpretations over known evidence, not as hidden authority over what the corpus means.

Model-produced labels or summaries may be useful derived artifacts, but they should not become canonical corpus truth unless explicitly reviewed and adopted in a later layer of the system.

---

## 19. Extensibility posture

The requirements explicitly call for iterative refinement and future expansion. The architecture should therefore assume that pattern categories, scoring ideas, and analysis modes will evolve.

### 19.1 Extensible where it matters

The architecture should be easy to extend in:
- evidence categorization
- corpus views
- analysis modes
- report shapes
- pattern taxonomies
- embedding/LLM strategies
- accommodation of new transcript event types or export variations

### 19.2 Stable where it matters

The architecture should remain stable in:
- source immutability
- normalization contract
- traceability requirements
- boundary between corpus definition and analysis consumers
- user-first orientation and role separation

This balance is what lets the system evolve without semantic drift.

---

## 20. Risks and architectural mitigations

### 20.1 Risk: contaminated corpora

If the system mixes tool chatter, protocol wrappers, exported runtime noise, and human-authored text indiscriminately, findings will be noisy and misleading.

Schema variation can create a related failure mode: unfamiliar or ambiguous records may be silently misclassified and pollute the main corpus.

**Architectural mitigation:** make semantic classification, role distinction, default corpus policies, and explicit ambiguous/unknown states part of the shared evidence model.

### 20.2 Risk: analysis surfaces diverge semantically

If search, notebooks, and LLM runs each use different filtering logic, or if the same named scope means different things across consumers, the system becomes incoherent.

The same problem applies if different consumers count recurrence differently without making that visible.

**Architectural mitigation:** one normalized evidence substrate, reusable corpus views, and explicit recurrence accounting boundaries.

### 20.3 Risk: findings cannot be trusted

If outputs are not traceable to source evidence, or if they present recurrence without showing the scope and caveats behind the count, they will be hard to verify or operationalize.

**Architectural mitigation:** traceability is a system-wide invariant, and findings must preserve representative evidence, scope, and recurrence basis.

### 20.4 Risk: subagents distort conclusions

If subagent output is treated as equivalent to direct user interaction, the system may infer the wrong recurring patterns.

**Architectural mitigation:** explicit session typing, preserved parent-child lineage where observable, and subagent-aware corpus views.

### 20.5 Risk: architecture collapses into ad hoc notebooks

If exploratory workflows or one-off reports become the only place logic lives, the repository loses agent legibility, reuse, and trust.

A related risk is that the system becomes a collection of one-shot analyses rather than a reusable environment for iterating over the same corpus.

**Architectural mitigation:** notebooks and reports consume the shared substrate rather than define it, and reusable corpus views remain the system of record for analysis scope.

### 20.6 Risk: premature coupling to one analysis technique

If the system is designed around only lexical search, or only embeddings, or only LLM prompting, it will narrow too early.

Likewise, if optional remote services become required for core operation, the system will violate the local-first requirement.

**Architectural mitigation:** shared evidence substrate with multiple interchangeable consumers and a local-first core that still produces useful, inspectable outputs without external dependencies.

---

## 21. Repository architecture posture

Because this repository is intended to be developed agentically, the architecture itself should be a top-level navigational artifact.

### 21.1 Role of this document

This document should act as the repository’s architectural map:
- what the system is
- what its layers are
- what invariants it protects
- where future design and planning work should fit

It should also preserve the shared vocabulary for concepts such as project, session, evidence unit, corpus view, analysis run, and finding so later work does not fragment the design.

### 21.2 Relationship to later documents

The expected document stack is:

- **Problem specification** — what the system must achieve
- **Architecture** — what the system is and how its major parts are organized
- **Implementation plan** — how to build it in staged, verifiable steps
- **Implementation artifacts** — code, tests, commands, and operational docs

### 21.3 Agent legibility requirement

Later implementation documents should preserve the boundaries established here rather than introducing accidental alternate architectures or hiding core semantics inside ad hoc prompts, notebooks, or scripts.

---

## 22. What the system will ultimately be

In its final form, this system should be understood as:

> A local-first, scope-aware transcript intelligence and decision-support platform for analyzing Claude Code history through a normalized, traceable evidence model that supports search, exploratory analysis, semantic comparison, LLM-assisted interpretation, and human judgment.

That definition is intentionally broader than “a search tool” and narrower than “a general AI analytics platform.”

Its identity rests on three architectural commitments:

1. **normalize transcript reality into a trustworthy semantic corpus**
2. **make that corpus reusable across multiple analysis modes**
3. **keep every finding anchored to traceable evidence for human judgment**

---

## 23. Architectural summary

The system we are building is a layered analysis platform over Claude Code transcript exports.

Its architectural center is a normalized evidence model that separates meaningful natural-language interaction from operational transcript machinery while preserving the user’s messages as the primary analysis signal.

Everything else — search, notebooks, embeddings, LLM analyses, reports, and later pattern detectors — sits downstream of that substrate.

This architecture gives us:
- a clean user-first corpus
- optional agent-side comparison corpora
- explicit subagent handling
- notebook-friendly exploration
- scope-aware comparative analysis
- recurrence analysis that can distinguish raw repetition from spread across sessions or projects
- explicit handling of excluded and ambiguous material
- LLM prompt experimentation without semantic drift
- clustering and similarity analysis over clean evidence units
- reproducible, traceable outputs for human judgment
- evidence-backed candidates for durable leverage without automatic downstream action

That is the architectural foundation the later implementation-planning phase should now turn into an execution plan.
