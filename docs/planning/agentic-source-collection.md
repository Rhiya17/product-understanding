# Building an Agentic Source-Collection System

**Date:** 2026-08-20
**Status:** Design note, written from a real reference run
**Companion:** `source-vault/README.md` (the output this system produces), LLD §6.1 Source Intake (the factory component this system implements)

This doc explains how to build a system that spins up AI agents to collect
product source assets — manuals, specs, images, video sources — the way the
first-wave vault was built on 2026-08-20. It answers, in order: how the work
was split and why that many agents; what each agent's work order looked like;
what's already available off the shelf and where to run it; and what the
agent and orchestrator code look like.

---

## 1. The reference run (what actually happened)

Five products were collected into `source-vault/`. One (Graco Ready2Jet) was
consolidated inline by the orchestrator because its assets already existed
locally — no agent needed. The other four were collected by **four agents
running in parallel**, one per product:

| Agent | Product | Tokens | Tool calls | Wall clock | Result |
|---|---|---:|---:|---:|---|
| 1 | Graco SnugRide (car seat) | 100K | 77 | 12.0 min | 19 sources, 34.5 MB — incl. browser fallback when the site blocked curl |
| 2 | Bose QC Ultra (headphones) | 125K | 65 | 11.7 min | 21 sources, 9.3 MB — incl. TLS-broken CDN worked around via mirror |
| 3 | Apple MacBook Air M3 | 94K | 48 | 8.8 min | 22 sources, 12.3 MB — no PDF manual exists; captured HTML guides as markdown |
| 4 | Levoit Core 300S | 157K | 90 | 15.1 min | 21 sources, 25.6 MB — incl. Wayback recovery of deleted hi-res images |

Wall clock for the whole collection ≈ the slowest agent (~15 min), because
they ran concurrently. Total agent spend ≈ 477K tokens, ~280 tool calls.
A post-run validation script (orchestrator-side, deterministic) re-hashed
every file against every manifest: **0 integrity issues across 93 source
entries**.

Two qualitative results matter as much as the numbers:

- Every agent hit at least one obstacle no one predicted (bot-blocking,
  expired TLS certs, renamed products, deleted CDN files) and routed around
  it — this is why this is agent work and not a scraper script.
- One agent surfaced a **material product-identity finding**: the requested
  "SnugRide 35 Lite LX" had been renamed, with the child weight limit
  changed 35→30 lb and one official image still showing the old limit. A
  scripted scraper would have downloaded the wrong product silently.

---

## 2. Decomposition: how many agents, and why

**The unit of parallelism is the product.** Not the asset type, not the URL.
One agent per product, because a product is the natural boundary on four
axes:

1. **Write isolation.** Each agent owns exactly one output directory and one
   `manifest.json`. No two agents ever touch the same file, so there is no
   locking, no merge, no conflict resolution. Single-writer-per-directory is
   the rule that makes "just run them all at once" safe.
2. **Context coherence.** All of one product's assets live on one
   manufacturer's infrastructure. The agent that learns "gracobaby.com
   blocks curl, but its scene7 CDN allows direct download" applies that
   lesson to the manual, the images, *and* the compatibility chart. Split
   by asset type instead and you'd pay that discovery cost three times.
3. **Failure isolation.** An agent that dies or goes down a rabbit hole
   costs you one product, not the run.
4. **Right-sized context.** One product ≈ 50–90 tool calls ≈ 100–160K
   tokens — comfortably one agent context. Splitting finer wastes
   orchestration overhead; merging products risks context exhaustion and
   cross-product confusion.

**How many concurrently:** all of them, up to your concurrency cap. Product
collection jobs are I/O-bound and independent, so parallelism is nearly
free. The reference run used 4; the same design runs 100 products as ~10
waves of 10 (bounded by API rate limits and politeness to target sites, not
by the architecture).

**When the orchestrator does the work itself:** when the "collection" is a
local file move (Ready2Jet's assets were already in the repo). Don't spawn
an agent to do deterministic work — agents are for the part that requires
judgment (finding, verifying, adapting).

---

## 3. The work order: what each agent was told

Each agent received a **contract, not a task description**. The difference
is what makes the output mergeable and trustworthy. Every work order had
seven parts:

1. **Scope and identity.** Exact product name, the target directory (theirs
   alone), and the pre-created subdirectory layout (`manuals/ images/
   videos/ specs/`).
2. **Source policy.** Official manufacturer domains only; retailers only for
   the 360-spin audit; explicit "do not download YouTube."
3. **Per-asset-type instructions.** What a complete manual collection means
   (main manual + quick start), what image coverage means for *this*
   product (e.g., "the control panel matters — it shows the filter reset
   button"; "multiple angles matter more than usual — this is the rigid
   control product for 3D testing").
4. **Verification rules.** Every download checked with `file` (a PDF must be
   a PDF), size sanity thresholds, delete anything that turns out to be an
   HTML error page. Trust nothing a webserver returns.
5. **The manifest schema.** The exact JSON shape, field by field, including
   real SHA-256 per file, origin URL, acquisition date, authority level,
   and a rights note. This is the merge contract: because all four agents
   emitted the same schema, the orchestrator could validate all of them
   with one script.
6. **Failure and substitution protocol.** "Stop after ~3 failed approaches
   per item and record the gap" (bounds rabbit holes); "if the exact
   variant can't be found, use the closest current one and record the
   substitution prominently" (which is exactly how the SnugRide rename was
   caught instead of papered over).
7. **Report format.** What the final message must contain: exact model
   identified, files with sizes, URLs recorded, spin finding, gaps. The
   report is for the orchestrator/human; the manifest is for the system.

The single highest-leverage element is #5 + #6: **a strict output schema
plus an explicit permission to fail visibly.** Agents told "get everything"
with no gap protocol either hallucinate completeness or burn budget
retrying; agents with a gap protocol return honest, machine-readable
inventories.

---

## 4. The orchestrator's job

The orchestrator (one process, or in the reference run the main assistant
session) does the deterministic bracketing around the agents:

```
1. SELECT     pick the products; write catalog.json (identity, rationale, pairs)
2. PREPARE    create the directory skeleton; seed any locally-available product
3. SPAWN      launch one agent per product, all in parallel, each with the contract
4. AWAIT      collect completion reports as they arrive
5. VALIDATE   deterministic script: parse every manifest, re-hash every file,
              check PDF magic bytes, count files vs entries  → zero-trust merge
6. RECONCILE  apply identity surprises to the catalog (e.g. the SnugRide rename),
              record run-level gaps
7. REPORT     inventory + findings + gaps for the human
```

Step 5 is not optional. The agents already self-verified, but the
orchestrator re-verifies **with code, not with a model** — the same
layered-verification principle the ShowMe LLD applies everywhere else
(deterministic checks bracket model work). The validation script from the
reference run is ~40 lines of Python and caught nothing this time; the day
it catches something is the day it pays for itself.

---

## 5. Build options: what already exists, where to run it

You do not need to build an agent framework. Three off-the-shelf options,
in increasing order of infrastructure ownership by Anthropic:

| Option | What it gives you | You own | Best when |
|---|---|---|---|
| **Claude Agent SDK** (`claude-agent-sdk` Python / `@anthropic-ai/claude-agent-sdk` TS) | The full Claude Code harness as a library: agent loop, built-in Bash/file/WebSearch/WebFetch tools, subagents, permissions. This is effectively what the reference run used (Claude Code's Agent tool). | Hosting (your laptop, a CI job, a container) | Fastest path; zero tool code — the built-in tools are exactly what collection needs. Docs: `code.claude.com/docs/en/agent-sdk` |
| **Claude API + Tool Runner** (`anthropic` SDK, `client.beta.messages.tool_runner`) | The loop is run by the SDK; you define the tools (download, write-manifest) and get Anthropic-hosted `web_search`/`web_fetch` server tools for free. | Hosting + the tool implementations | You want the collector inside your own service — e.g. as a `showme-worker` job type — with tight control over every tool the agent can touch |
| **Managed Agents** (Anthropic-hosted, beta) | Anthropic runs the loop *and* the sandbox (bash, files, code exec). Sessions per product; **scheduled deployments** re-run collection on a cron for freshness. | Just the client that starts sessions and reads results | You want no infra at all, and you want the freshness re-crawl (LLD source-freshness requirement) to be a scheduled deployment instead of your own cron |

**Where it runs in ShowMe's architecture:** this system *is* LLD §6.1
Source Intake's acquisition half. Production shape: a `collection` job type
on the existing `showme-worker` queue — one job per product, the worker
process runs the agent (Agent SDK or Tool Runner), writes to the vault, and
emits `source.ingested` events per collected source. The orchestrator's
validation gate becomes the job's completion check. Re-collection for
freshness is the same job re-queued on a schedule with idempotency: re-fetch,
compare SHA-256, and only version-bump sources that actually changed —
which automatically feeds the LLD's invalidation pipeline (§3.4) when a
manual revision lands.

**For the MVP: run the Agent SDK version from a laptop or CI.** The queue
integration is Phase-2 polish; the agent contract and the vault schema are
the durable parts.

---

## 6. What the agent code looks like

### 6.1 Claude API + Tool Runner (self-hosted worker)

The agent is: a model, two custom tools (download, finalize), two
Anthropic-hosted server tools (web search, web fetch), and the work order as
the user message. The SDK runs the loop.

```python
# collector_agent.py
import hashlib, json, pathlib, subprocess
import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()

VAULT = pathlib.Path("source-vault")

def make_tools(product_dir: pathlib.Path):
    """Tools closed over the product directory — the agent can only write there."""

    @beta_tool
    def download_file(url: str, relative_path: str, expected_kind: str) -> str:
        """Download a file into the product's vault directory and verify it.

        Args:
            url: Direct URL of the asset to download.
            relative_path: Destination inside the product dir, e.g. "manuals/manual.pdf".
            expected_kind: One of "pdf", "image", "video". Used to verify the payload.
        """
        dest = (product_dir / relative_path).resolve()
        if product_dir.resolve() not in dest.parents:
            return json.dumps({"ok": False, "error": "path escapes product dir"})
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["curl", "-sSL", "--max-time", "120", "-o", str(dest), url],
                           capture_output=True, text=True)
        if r.returncode != 0 or not dest.exists():
            return json.dumps({"ok": False, "error": r.stderr[-500:]})
        kind = subprocess.run(["file", "-b", str(dest)], capture_output=True, text=True).stdout
        checks = {"pdf": "PDF document", "image": ("JPEG", "PNG", "WebP"), "video": "MP4"}
        want = checks[expected_kind]
        if not any(w in kind for w in ([want] if isinstance(want, str) else want)):
            dest.unlink()  # never keep an HTML error page pretending to be media
            return json.dumps({"ok": False, "error": f"payload is '{kind.strip()}', not {expected_kind}"})
        sha = hashlib.sha256(dest.read_bytes()).hexdigest()
        return json.dumps({"ok": True, "path": relative_path,
                           "bytes": dest.stat().st_size, "sha256": sha})

    @beta_tool
    def write_manifest(manifest_json: str) -> str:
        """Validate and persist the product manifest.json. Call exactly once, at the end.

        Args:
            manifest_json: The complete manifest as a JSON string, following the
                schema in the work order.
        """
        m = json.loads(manifest_json)  # raises → tool error → agent retries
        for s in m["sources"]:
            lp = s.get("local_path")
            if lp:
                p = product_dir / lp
                if not p.exists():
                    return json.dumps({"ok": False, "error": f"manifest references missing file {lp}"})
                if hashlib.sha256(p.read_bytes()).hexdigest() != s["sha256"]:
                    return json.dumps({"ok": False, "error": f"sha256 mismatch for {lp}"})
        (product_dir / "manifest.json").write_text(json.dumps(m, indent=2))
        return json.dumps({"ok": True, "entries": len(m["sources"])})

    return [download_file, write_manifest]

SERVER_TOOLS = [
    {"type": "web_search_20260209", "name": "web_search", "max_uses": 25},
    {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 40},
]

def run_collector(product_dir: pathlib.Path, work_order: str) -> str:
    runner = client.beta.messages.tool_runner(
        model="claude-opus-5",           # capable default; judgment calls live here
        max_tokens=32000,
        tools=[*make_tools(product_dir), *SERVER_TOOLS],
        messages=[{"role": "user", "content": work_order}],
    )
    last = None
    for message in runner:               # SDK drives the search→fetch→download loop
        last = message
    return next((b.text for b in last.content if b.type == "text"), "")
```

Notes on the choices:

- **The tools are the security boundary.** `download_file` refuses paths
  outside the product dir and deletes non-matching payloads; `write_manifest`
  re-verifies every hash before persisting. The model proposes; the tool
  disposes. This is the same "deterministic checks bracket model output"
  rule as everywhere else in ShowMe.
- **Server tools do the discovery.** `web_search`/`web_fetch` run on
  Anthropic's side — the agent finds the manual URL with them, then pulls
  the bytes with *your* `download_file`, so every artifact that lands on
  disk went through your verification, not the model's.
- **One caveat:** the Python tool runner does not auto-resume
  `pause_turn` (long server-tool turns). Production code should wrap the
  loop with the restart pattern from the SDK docs.
- **Production addition:** on Opus 5, enable server-side refusal fallbacks
  (`betas=["server-side-fallback-2026-07-01"]`, `fallbacks="default"`) so a
  safety-classifier decline on one request degrades gracefully instead of
  killing the product's collection job.
- The work order string is exactly the seven-part contract from §3.

### 6.2 The orchestrator (fan-out + validation)

```python
# orchestrate.py
import concurrent.futures, json, pathlib
from collector_agent import run_collector, VAULT

catalog = json.loads((VAULT / "catalog.json").read_text())

def work_order_for(product: dict) -> str:
    return WORK_ORDER_TEMPLATE.format(**product)   # the §3 contract, parameterized

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    futures = {
        pool.submit(run_collector, VAULT / p["dir"], work_order_for(p)): p["product_id"]
        for p in catalog["products"] if not (VAULT / p["dir"] / "manifest.json").exists()
    }                                              # idempotent: skip already-collected
    reports = {futures[f]: f.result() for f in concurrent.futures.as_completed(futures)}

# Zero-trust validation gate — code, not model (same script as the reference run):
# parse every manifest, re-hash every file, verify PDF magic, count files vs entries.
# Only products that pass get merged/committed; failures re-queue or go to a human.
```

### 6.3 Claude Agent SDK variant (what the reference run effectively used)

With the Agent SDK you skip writing tools entirely — the harness ships
Bash, file ops, WebSearch, and WebFetch, which is precisely the collection
toolkit. The program collapses to: `query(prompt=work_order, options=...)`
per product, run concurrently. The trade-off is a coarser security boundary
(the agent has general Bash + filesystem access within the permissions you
configure) in exchange for zero tool code and the most capable
off-the-shelf harness. See `code.claude.com/docs/en/agent-sdk` for the API;
don't reimplement its loop on the raw API — if you want fine-grained custom
tools, that's what §6.1 is for.

### 6.4 Structured reports (optional upgrade)

The reference run's agents returned free-text reports. For machine
consumption, have the final report conform to a schema — either
`client.messages.parse()` with a Pydantic model of the report, or make
`write_manifest`'s input schema `strict: true` so manifest validity is
enforced at the API layer instead of by retry.

---

## 7. Production hardening (the gap between the reference run and a system)

| Concern | What the reference run did | What production should do |
|---|---|---|
| Bot-blocked sites | One agent improvised a browser fallback | Provide a real headless-browser tool (Playwright) as a declared tool; record which fetch path was used per source |
| Broken/moved assets | One agent recovered deleted images from the Wayback Machine | Keep it — but make archive recovery a labeled provenance type in the manifest, since archived ≠ current-official |
| Politeness / ToS | Implicit | Rate-limit per domain, honor robots.txt for crawl-style access, cache fetches; collection hits each site a handful of times, not hundreds |
| Rights | Every entry stamped "generate_from NOT cleared" | Keep the deny-by-default rights vector; a separate rights-review workflow flips flags, never the collector |
| Idempotency / freshness | Skip-if-manifest-exists | Re-run on schedule; re-fetch, compare SHA-256, version-bump only real changes, emit `source.ingested` → the LLD invalidation pipeline handles downstream |
| Budgets | Agent prompts bounded retries ("~3 approaches") | Also bound tokens/cost per job (the LLD's execution-budget pattern); a collector that can't finish inside budget parks as NEEDS_REVIEW with its partial manifest |
| Validation | Post-run script, run manually | The same script as the job's completion gate; failing products don't merge |
| Identity surprises | Agent reported the SnugRide rename; human updated the catalog | Route "product renamed/superseded/spec changed" findings into the Content-Ops review queue — they are claim-level events, not collection trivia |

## 8. Appendix: where the data actually came from

Every collected file's exact `origin_url` is in its product's
`manifest.json`; video URLs that were recorded but not downloaded are in
each product's `videos/video-sources.md`. The consolidated domain inventory
of the reference run:

| Product | Domain | What came from it |
|---|---|---|
| **Graco Ready2Jet** | *(local repo POC folders)* | Manual PDF, official images, fold video — acquired during the July POCs; origin URLs pending backfill (recorded gap) |
| **Graco SnugRide Lite LX** | `www.gracobaby.com` | Product page (specs; blocked curl — accessed via browser automation) |
| | `newellbrands.imgix.net` | Both manual PDFs (EN/ES), the Apr-2026 stroller compatibility chart PDF, one image (Graco's parent-company asset CDN — allowed direct download) |
| | `s7d1.scene7.com` | 11 official gallery images (Adobe Scene7 CDN serving Graco's PDP imagery) |
| | `www.youtube.com` | 3 official Graco-channel install/harness video URLs (recorded, not downloaded) |
| | `amazon.com` | 360-spin audit only — nothing downloaded |
| **Bose QC Ultra (2nd Gen)** | `www.bose.com` / `support.bose.com` | Product page and support pages (specs, pairing procedure) |
| | `assets.bosecreative.com` | All 3 PDFs (owner's guide, safety, gestures) + 12 gallery images — used because the primary `assets.bose.com` CDN was serving an expired TLS certificate (recorded in manifest) |
| | `players.brightcove.net` | 3 official Bose how-to video embeds (URLs recorded) |
| | `360-viewer.bose.com` | 360-spin audit (CGI .glb viewer identified; nothing downloaded) |
| **Apple MacBook Air 13" M3** | `support.apple.com` | Tech specs, model-identification page, Essentials guide (HTML captured as markdown — Apple publishes no manual PDF) |
| | `help.apple.com` | 3 port-layout diagram images from the M3-era archived guide |
| | `www.apple.com` | Newsroom images, environmental report PDF, marketing page captures |
| | `store.storeimages.cdn-apple.com` | 5 store gallery renders (per-color front views) |
| | `cdsassets.apple.com` | 1 support-asset image |
| | `www.youtube.com` | Apple Support channel how-to URLs (recorded; notable gap: no official Bluetooth-pairing video exists) |
| **Levoit Core 300S** | `levoit.com` | 2 manual PDFs (300S + 300S-P revisions), spec page, 6 images — three 3000px images recovered from **Wayback Machine snapshots** of deleted levoit.com CDN URLs (provenance noted per-image in the manifest) |
| | `files.vesync.com` | Redundant copy of the 300S manual (provenance redundancy from the parent company's file host) |
| | `cdn.shopify.com` | 6 gallery images + 3 official Levoit MP4 how-to videos (Levoit's storefront CDN) |
| | `us.vesync.com` | Support page reference (support.levoit.com itself is login-gated — recorded gap) |

Patterns worth internalizing for the production system: manufacturers rarely
serve assets from their marketing domain — the bytes live on CDNs
(Scene7, imgix, Shopify, storeimages) that typically *allow* direct download
even when the storefront blocks bots; parent-company infrastructure
(Newell for Graco, VeSync for Levoit) is often the authoritative file host;
and the Wayback Machine is a legitimate recovery path for deleted official
assets as long as the archived provenance is labeled as such.

## 9. Cost model

At the reference run's consumption (~100–160K tokens/product) the model cost
is roughly **$1–4 per product** depending on model tier, plus negligible
egress — i.e., the entire 5-product first wave cost less than one generated
video attempt. Collection is not the expensive part of the factory; don't
over-optimize it. The expensive parts it feeds (extraction, verification,
generation) are where the vault's clean manifests pay off.
