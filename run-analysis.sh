#!/usr/bin/env bash
# run-analysis.sh — one command to run the full ChatAnalysis pipeline
#
# Usage:
#   ./run-analysis.sh                    # uses default transcript location
#   ./run-analysis.sh ~/my-transcripts   # custom transcript directory
#
# Prerequisites:
#   pip install -e .                     # base pipeline (zero dependencies)
#   pip install -e '.[semantic-local]'   # for clustering (recommended)
#   pip install -e '.[skill-mining]'     # for LLM-backed skill mining (optional)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Resolve transcript source ──
CLAUDE_PROJECTS="${1:-}"

if [ -z "$CLAUDE_PROJECTS" ]; then
    # Auto-detect Claude Code transcript location
    if [ -d "$HOME/.claude/projects" ]; then
        CLAUDE_PROJECTS="$HOME/.claude/projects"
        echo "Auto-detected Claude Code transcripts at: $CLAUDE_PROJECTS"
    else
        echo "Error: Could not find Claude Code transcripts."
        echo ""
        echo "Claude Code stores transcripts at ~/.claude/projects/"
        echo "If yours are elsewhere, pass the path as an argument:"
        echo "  ./run-analysis.sh /path/to/your/transcripts"
        exit 1
    fi
fi

if [ ! -d "$CLAUDE_PROJECTS" ]; then
    echo "Error: Directory not found: $CLAUDE_PROJECTS"
    exit 1
fi

# Count sessions
SESSION_COUNT=$(find "$CLAUDE_PROJECTS" -name '*.jsonl' | wc -l)
if [ "$SESSION_COUNT" -eq 0 ]; then
    echo "Error: No .jsonl transcript files found in $CLAUDE_PROJECTS"
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ChatAnalysis Pipeline                                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "  Source:   $CLAUDE_PROJECTS"
echo "  Sessions: $SESSION_COUNT transcript files"
echo ""

# ── Ensure output directories exist ──
ARTIFACT_ROOT="artifacts/chat-analysis"
CONFIG="configs/chat-analysis.default.yaml"

# ── Symlink transcripts into projects/ if not already there ──
if [ ! -d "projects" ] || [ -z "$(ls -A projects/ 2>/dev/null)" ]; then
    echo "→ Linking transcripts into projects/..."
    mkdir -p projects
    # Copy directory structure (symlinks would break on some systems)
    cp -r "$CLAUDE_PROJECTS"/* projects/ 2>/dev/null || true
    echo "  Done."
    echo ""
fi

# ── Stage 1: Discover ──
echo "▸ [1/7] Discovering projects and sessions..."
chatanalysis discover \
    --config "$CONFIG" \
    --projects-root projects \
    --output-dir "$ARTIFACT_ROOT/discovery/run" \
    > /dev/null
INVENTORY="$ARTIFACT_ROOT/discovery/run/session_inventory.jsonl"
echo "  ✓ Found $(wc -l < "$INVENTORY") sessions"

# ── Stage 2: Parse ──
echo "▸ [2/7] Parsing raw events from transcripts..."
chatanalysis parse \
    --inventory "$INVENTORY" \
    --output-dir "$ARTIFACT_ROOT/parse/run" \
    > /dev/null
echo "  ✓ Raw events written"

# ── Stage 3: Normalize ──
echo "▸ [3/7] Normalizing into canonical evidence..."
chatanalysis normalize \
    --inventory "$INVENTORY" \
    --raw-events "$ARTIFACT_ROOT/parse/run/raw_events.jsonl" \
    --output-dir "$ARTIFACT_ROOT/normalize/run" \
    > /dev/null
EVIDENCE="$ARTIFACT_ROOT/normalize/run/evidence.jsonl"
echo "  ✓ $(wc -l < "$EVIDENCE") evidence records"

# ── Stage 4: Build views ──
echo "▸ [4/7] Building corpus views..."
for VIEW_NAME in user_nl_root_only root_only_all_roles; do
    chatanalysis build-view \
        --evidence "$EVIDENCE" \
        --view "$VIEW_NAME" \
        --output-dir "$ARTIFACT_ROOT/views/$VIEW_NAME" \
        > /dev/null
done
VIEW_DIR="$ARTIFACT_ROOT/views/user_nl_root_only"
VIEW_COUNT=$(wc -l < "$VIEW_DIR/corpus_view.jsonl")
echo "  ✓ user_nl_root_only: $VIEW_COUNT rows"

# ── Stage 5: Detect patterns ──
echo "▸ [5/7] Running pattern detectors..."
for DETECTOR in repeated_instructions change_requests refinement_requests workflow_patterns; do
    chatanalysis detect \
        --view-dir "$VIEW_DIR" \
        --detector "$DETECTOR" \
        --output-dir "$ARTIFACT_ROOT/detectors/$DETECTOR" \
        > /dev/null 2>&1 || true
done
echo "  ✓ 4 detectors complete"

# ── Stage 6: Extract episodes ──
echo "▸ [6/7] Extracting conversation episodes..."
chatanalysis extract-episodes \
    --evidence "$EVIDENCE" \
    --output-dir "$ARTIFACT_ROOT/episodes" \
    > /dev/null
EP_DIR="$ARTIFACT_ROOT/episodes/default"
EP_COUNT=$(python3 -c "
import json
idx = json.load(open('$EP_DIR/episode_index.json'))
print(idx['episode_count'])
")
echo "  ✓ $EP_COUNT episodes, $(python3 -c "import json; print(json.load(open('$EP_DIR/episode_index.json'))['turn_count'])") turns"

# ── Stage 7: Generate report ──
echo "▸ [7/7] Generating analysis report..."
chatanalysis report \
    --detector-run "$ARTIFACT_ROOT/detectors/repeated_instructions/detector_run.json" \
    --output-dir "$ARTIFACT_ROOT/reports/summary" \
    > /dev/null
echo "  ✓ Report written"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Pipeline complete!                                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "  Evidence:  $EVIDENCE"
echo "  Episodes:  $EP_DIR/episodes.jsonl ($EP_COUNT episodes)"
echo "  Views:     $VIEW_DIR/"
echo "  Report:    $ARTIFACT_ROOT/reports/summary/report.md"
echo ""
echo "Next steps:"
echo ""
echo "  1. Read the report:"
echo "     cat $ARTIFACT_ROOT/reports/summary/report.md"
echo ""
echo "  2. Run the clustering notebook (requires semantic-local extras):"
echo "     jupyter notebook notebooks/06_skill_mining_analysis.ipynb"
echo ""
echo "  3. Run LLM-backed skill mining (requires skill-mining extras + API key):"
echo "     chatanalysis semantic-run --method skill-mining \\"
echo "       --episode-dir $EP_DIR \\"
echo "       --disabled-by-default-check \\"
echo "       --output-dir $ARTIFACT_ROOT/semantic/skill-mining"
echo ""
