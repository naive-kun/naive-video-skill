# Changelog

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
