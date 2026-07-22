# Changelog

## 2.2.0

- Changed the public package to expose exactly one root `SKILL.md`; twelve stage modules now live as internal workflow references so WorkBuddy-style recursive installers show one skill instead of many cards.
- Replaced destructive install/upgrade behavior with timestamped backups, failure rollback, legacy-entry archiving, and recoverable uninstall archives.
- Added validation and smoke coverage that reject nested skill manifests and recursive force-delete commands.
- Added an optional beginner rough-cut route that delegates to an installed `video-use` skill, preserves originals, requires strategy approval, and records an approved `working_video` for downstream stages.
- Added honest transcription onboarding: existing timing first, hosted word-level transcription recommended for precision rough cuts with possible cost disclosed, and local word-level transcription kept optional.
- Added screenshot/demo onboarding with semantic, exact-second or spoken-sentence, and hybrid placement modes; exact user anchors are explicitly described as more precise.
- Added GSAP runtime/plugin guidance plus `tools/gsap_check.py` for offline package version, license-header, and plugin-role inspection without vendoring a personal download folder.
- Added a brand-neutral visual-quality contract for typography, caption line policy, component geometry, alignment, and public/private style separation.
- Added deterministic `DESIGN.md` validation with `tools/design_check.py`.
- Added seek-safe `focus-frame`, `seekable-type`, `split-reveal`, and `glass-notification` GSAP recipes based on reusable component behavior without copying a creator-specific visual style.
- Added preview gates for real font weights, level text baselines, stable caption line counts, glass contrast, and deterministic seek behavior.
- Added explicit anti-patterns for unrequested hand-drawn graphics, thin oversized loose type, skewed readable text, timer-driven animation, and brand leakage into public defaults.

## 2.1.0

- Added an offline GSAP semantic motion recipe catalog with eleven reusable recipes and intent mappings.
- Added `restrained`, `balanced`, and duration-aware `energetic` motion density guidance.
- Added deterministic `MOTION_PLAN.json` validation for recipe IDs, timing, caption evidence, protected regions, fallbacks, and energetic coverage.
- Added screenshot visual-language matching with `low`, `medium`, and `high` reference strength.
- Added project-local `STYLE_REFERENCE.md` extraction with explicit anti-copy and static-motion inference boundaries.
- Improved beginner onboarding so a reference screenshot is optional, recommended choices are explained plainly, and safe defaults remain available.
- Added offline smoke coverage for valid, under-designed, and protected-region motion plans.

## 2.0.0

- Added a root router and eleven focused child skills.
- Added beginner project initialization and resumable project state.
- Added explicit quality gates for source, captions, design, preview, approval, and final export.
- Added project doctor, caption consistency check, privacy scan, and no-dependency skill validation.
- Added Codex and Claude Code installers plus uninstall support.
- Added explicit-feedback learning and privacy-safe self-iteration rules.
- Added post-delivery retrospectives and deterministic private-profile rule inheritance.
- Added schema migration registry and adoption path for older projects.
- Added smoke tests and GitHub Actions validation.
- Corrected export guidance so a low-resolution proxy is never presented as a true high-resolution final.
