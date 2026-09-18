# ============================================================
# STEVE.PY — MAIN RUNNER / ORCHESTRATOR
#
# What this file is:
# - This is the ONLY file you run in the terminal
# - This file does NOT talk to APIs directly
#
# What this file does:
# - Sends the same question to multiple adapters
# - Collects their results
# - Chooses the "best" answer
#
# Think of this like:
# - adapters = engines
# - steve.py = the driver
# ============================================================

from adapters.tavily_adapter import tavily_query
from adapters.brave_adapter import brave_query

# ============================================================
# SERVICE PARAMETER
# CHANGE ONLY THIS LINE TO ASK A DIFFERENT QUESTION
# ============================================================

QUERY = "What is Phillipa Soo's vocal range?"

# ============================================================
# LIST OF APIS TO RUN
#
# Each item:
# - name: just for tracking/debugging
# - function: the adapter function
#
# When we add more APIs, we ONLY touch this list
# ============================================================

ADAPTERS = [
    ("tavily", tavily_query),
    ("brave", brave_query),
]

# ============================================================
# RUN ALL ADAPTERS
#
# Sends the same query to every adapter
# If one API fails, the others still run
# ============================================================

def run_all(query: str) -> list[dict]:
    results = []

    for name, fn in ADAPTERS:
        try:
            out = fn(query)
            out["provider"] = name  # tag where it came from
            results.append(out)
        except Exception as e:
            results.append({
                "provider": name,
                "answer": f"[ERROR from {name}] {e}",
                "sources": [],
            })

    return results

# ============================================================
# PICK BEST ANSWER (SIMPLE VERSION ON PURPOSE)
#
# Rules:
# - Prefer answers that actually say something
# - Prefer answers with more sources
#
# Later this becomes AI logic
# ============================================================

def pick_best(results: list[dict]) -> dict:
    def score(r: dict) -> int:
        has_answer = 1 if "No direct answer" not in r.get("answer", "") else 0
        num_sources = len(r.get("sources", []))
        return (has_answer * 100) + num_sources

    return max(results, key=score)

# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    all_results = run_all(QUERY)

    best = pick_best(all_results)

    print("\n=== BEST ANSWER ===")
    print(best.get("answer", "[No answer]"))

    print("\n=== BEST SOURCES ===")
    i = 1
    for s in best.get("sources", []):
        print(f"{i}. {s.get('title', '')} - {s.get('url', '')}")
        i += 1

    # Debug: see what every API returned
    print("\n=== DEBUG: WHAT EACH API RETURNED ===")
    for r in all_results:
        print(f"- {r.get('provider')}: {len(r.get('sources', []))} sources")
