# ============================================================
# MAIN.PY — MAIN RUNNER / ORCHESTRATOR
#
# What this file does:
# - Sends the same question to multiple search adapters
# - Runs the adapters in parallel
# - Collects their results
# - Chooses the best answer using simple scoring rules
#
# Think of this like:
# - adapters = search engines
# - main.py = the driver
# ============================================================

from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from adapters.tavily_adapter import tavily_query
from adapters.brave_adapter import brave_query

load_dotenv()

# ============================================================
# LIST OF SEARCH ADAPTERS
#
# To add another search provider later,
# add its adapter function to this list.
# ============================================================

ADAPTERS = [
    ("tavily", tavily_query),
    ("brave", brave_query),
]

# ============================================================
# RUN ALL ADAPTERS IN PARALLEL
#
# Tavily and Brave search at the same time.
# If one API fails, the other can still return results.
# ============================================================

def run_all(query: str) -> list[dict]:
    results = []

    with ThreadPoolExecutor(max_workers=len(ADAPTERS)) as executor:
        futures = {
            executor.submit(fn, query): name
            for name, fn in ADAPTERS
        }

        for future in as_completed(futures):
            name = futures[future]

            try:
                out = future.result()
                out["provider"] = name
                out["error"] = False
                results.append(out)

            except Exception as e:
                results.append({
                    "provider": name,
                    "answer": f"[ERROR from {name}] {e}",
                    "sources": [],
                    "error": True,
                })

    return results


# ============================================================
# PICK BEST ANSWER
#
# Rules:
# - Never choose an API error as the best answer
# - Prefer a direct answer
# - Prefer results with more sources
# ============================================================

def pick_best(results: list[dict]) -> dict:
    successful_results = [
        result for result in results
        if not result.get("error", False)
    ]

    if not successful_results:
        return {
            "provider": "none",
            "answer": "All search providers failed.",
            "sources": [],
            "error": True,
        }

    def score(result: dict) -> int:
        answer = result.get("answer", "")

        has_direct_answer = (
            bool(answer)
            and "No direct answer" not in answer
        )

        num_sources = len(result.get("sources", []))

        return (100 if has_direct_answer else 0) + num_sources

    return max(successful_results, key=score)


# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    query = input("Enter a search question: ").strip()

    if not query:
        print("Please enter a question.")
        raise SystemExit

    all_results = run_all(query)

    best = pick_best(all_results)

    print("\n=== BEST ANSWER ===")
    print(best.get("answer", "[No answer]"))

    print("\n=== BEST SOURCES ===")
    for i, source in enumerate(best.get("sources", []), start=1):
        title = source.get("title", "")
        url = source.get("url", "")
        print(f"{i}. {title} - {url}")

    print("\n=== DEBUG: WHAT EACH API RETURNED ===")
    for result in all_results:
        provider = result.get("provider")
        source_count = len(result.get("sources", []))
        status = "ERROR" if result.get("error") else "OK"

        print(f"- {provider}: {source_count} sources ({status})")
