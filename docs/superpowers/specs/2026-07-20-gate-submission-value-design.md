# Gate Submission Value and Publication Design

## Objective

Reframe Gate around the developer problem it solves, publish the existing live
real-project recording as a public YouTube video, make that video the primary
Devpost demo, and audit the release for confirmed defects before publishing the
final repository state.

The central product statement is:

> Codex says "done." Gate checks whether that is true.

Gate succeeds when a coding agent's completion claim becomes falsifiable,
protected, reproducible, and independently auditable. Gate does not claim that
verified code is universally correct or that it can compensate for a weak
acceptance test suite.

## Scope

This publication pass includes:

- integrating the attached problem-led README material with the current
  installation, plugin, CLI, security, demo, and provenance documentation;
- preserving five source-backed examples of the real verification problem;
- removing references to Gate's former license from current-facing license and
  attribution copy while retaining the canonical GPL terms and NOTICE;
- uploading the existing 2:55 live recording to YouTube with public visibility;
- replacing Devpost's primary demo video and rewriting its opening around the
  problem, evidence, solution, and live proof;
- reviewing the installer, launcher, protected-state handling, and supporting
  documentation for confirmed correctness or security defects;
- testing, committing, pushing the existing feature branch, and fast-forwarding
  `master`.

This pass does not:

- claim Gate makes software 100% correct;
- claim that ordinary Codex failed the demonstrated coding task;
- alter or revoke rights attached to copies distributed under prior terms;
- add speculative features during the bug audit;
- replace Gate's core verification contract with plugin-specific behavior; or
- describe the scripted adversarial fixture as a live AI run.

## Public Evidence Contract

README and Devpost may use the following source-backed claims, with links placed
next to the claims they support:

1. OpenAI reports that internal coding agents sometimes illegitimately edit
   tests to make them pass and labels reward hacking "Rare but high severity."
   Source:
   `https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/`
2. METR reports a Claude 3.7 software-engineering attempt that directly edited
   a provided tests file to cause all tests to pass. Source:
   `https://metr.org/evaluations/claude-3-7-report/`
3. The 2025 Stack Overflow Developer Survey reports 46% distrust versus 33%
   trust in AI-tool accuracy, with 3.1% highly trusting the output. Source:
   `https://survey.stackoverflow.co/2025/ai`
4. DORA describes a verification tax in which time saved writing is re-spent
   auditing and reports 30% of developers with little or no trust in
   AI-generated code. Source:
   `https://dora.dev/insights/balancing-ai-tensions/`
5. The cited SWE-bench correctness study reports that 7.8% of evaluated
   plausible patches were accepted by narrower validation while failing the
   developer-written test suite, and that 29.6% exhibited behavior different
   from oracle patches. Source: `https://arxiv.org/html/2503.15223v1`.

The copy must distinguish observed evidence from Gate-specific inference. The
sources establish that narrow validation, test manipulation, trust, and review
overhead are real problems. The claim that Gate is an appropriate control for
these problems is the project's reasoned product position.

## README Information Architecture

The attached README is the narrative base, but it must be merged rather than
copied blindly. Repository facts and commands from the current README remain
authoritative.

The final order is:

1. Product statement and concise mechanism.
2. `Why Gate exists`, including five concrete failure modes and public evidence.
3. `How the idea became Gate`, including the full-verifier regression and the
   test-deletion red-team finding.
4. `What Gate changes`, with a without/with comparison and enforcement flow.
5. `What success means`, including an explicit weak-verifier limitation.
6. Build Week links and the new YouTube live-demo URL.
7. Supported platforms and quick-start plugin installation.
8. Standalone CLI and Codex plugin instructions.
9. GPL license and attribution.
10. Live real-project and deterministic adversarial evidence.
11. Audit verification, security limits, and build provenance.

The README remains ASCII. Smart quotes and typographic arrows from the attached
draft are converted to ordinary quotes and `->`. Counts and verdicts must match
the checked-in evidence:

- live ordinary control: 51 passed, with no Gate verdict, log, or root;
- live plugin run: 50 passed, `FINAL VERIFIED`, valid four-record chain;
- separately captured standalone CLI: 51 passed and `FINAL VERIFIED`.

## License Presentation

Current-facing copy states only that Gate is licensed under
`GPL-3.0-or-later`, links `LICENSE` and `NOTICE`, and explains the redistribution
requirements and GPLv3 section 7(b) attribution term.

References to Gate's previous license are removed from the README license and
attribution section. The canonical `LICENSE` and existing `NOTICE` remain
unchanged unless the audit finds an objective error. Third-party license facts,
such as the license of the iniconfig demo repository, are not descriptions of
Gate's license and may remain where relevant.

No copy will claim that removing historical wording retroactively revokes
rights already granted to existing recipients.

## YouTube Publication

Upload source:

`docs/video/gate-real-project-live.mp4`

Required properties:

- visibility: Public;
- audience: not made for kids;
- title: `Gate v2: Codex Says Done. Gate Verifies It. | Live Project Demo`;
- description: concise problem statement, without/with result, repository,
  plugin guide, Devpost, public evidence links, audit root, video SHA-256, and
  an honesty statement that ordinary Codex solved the coding task;
- no claim that Gate improves the implementation or proves universal
  correctness;
- auto-generated thumbnail is acceptable for this pass;
- final watch URL must be captured and verified after publication.

The description includes these integrity values:

- audit root:
  `5241d2d1e9ea87699c52333d7b8c16db8b6bbda961e9921c831992cb178c186b`;
- video SHA-256:
  `AC7240A101F72531E3CA69D6B601B5839C91318C1DC3D403660D229C23D26076`.

## Devpost Rewrite

The existing Gate project remains submitted to OpenAI Build Week. Its primary
video URL is replaced with the new public YouTube watch URL.

The description is reorganized to lead with:

1. the same-trust-boundary problem;
2. public evidence that narrow verification and reward hacking occur;
3. the developer pain created by repetitive auditing;
4. Gate's protected verifier, exact-thread retries, and chained audit record;
5. the live without/with result;
6. CLI and plugin installation paths;
7. security boundaries, evidence roots, and provenance.

Existing truthful technical details and permanent evidence links are preserved.
The published state and Build Week submission association must be re-read after
the update. Devpost's stored video URL must exactly match the public YouTube URL.

## Defect Audit

The audit covers the release surfaces most likely to affect real adoption:

- plugin installer path handling, allowlist completeness, replacement behavior,
  and preservation of unrelated marketplace entries;
- launcher interpreter selection across native Windows and WSL;
- fail-closed platform and dependency checks;
- repository/task path validation and external state placement;
- command construction and shell boundaries;
- audit log discovery and validation behavior;
- version/license metadata consistency; and
- README, plugin guide, and evidence command accuracy.

Findings require reproducible evidence. Confirmed runtime defects receive a
focused regression test and implementation fix. If runtime or packaged plugin
behavior changes, bump the plugin to `0.2.1`; documentation-only corrections do
not change the runtime version. Unconfirmed concerns are recorded as future work
instead of being presented as fixed bugs.

## Verification and Release Gates

Before publication is considered complete:

- all five evidence URLs resolve and support the adjacent wording;
- README source links and internal links are checked;
- Windows product tests pass with only documented platform skips;
- the full WSL suite passes;
- package tests and the official plugin validator pass;
- generated plugin assets match committed assets;
- the live audit chain validates to the anchored root;
- the MP4 hash matches the anchored SHA-256;
- no credential-like data appears in new documentation or evidence;
- YouTube reports Public visibility and exposes a watch URL;
- Devpost remains published and uses the same watch URL;
- the feature branch and `master` resolve to the same final commit; and
- GitHub Actions succeeds on the final `master` commit.

## Completion Evidence

The final report includes:

- final commit and branch hashes;
- YouTube and Devpost URLs;
- test and validator results;
- audit root and video hash;
- confirmed bugs fixed, or an explicit statement that no confirmed product bug
  was found;
- remaining platform and verifier limitations; and
- recommended next phases for Gate.
