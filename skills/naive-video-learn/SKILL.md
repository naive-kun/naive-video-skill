---
name: naive-video-learn
description: Record explicit, reusable video-editing feedback into a user's project-local Naive Video Skill profile. Use when the user says remember this style, always do this, never do this again, make future videos follow this rule, or wants the workflow to improve from confirmed revisions without exposing private information.
---

# Naive Video Learn

Turn explicit feedback into a testable project-local rule.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Preconditions

- The user must clearly confirm the preference.
- The rule must be observable and testable.
- Read `references/self-iteration.md`.

## Workflow

1. Capture a short faithful quote or paraphrase.
2. Classify scope as `project`, `profile`, or `product-candidate`.
3. Default ambiguous feedback to `project`.
4. Write the lesson to `VIDEO_LESSONS.md` using the protocol format.
5. If the lesson is an active style rule, update only the matching field in `DESIGN.md` and state.
6. For `profile` scope, initialize the private local profile when needed and add only the sanitized confirmed rule:

   ```bash
   python3 <skill_root>/tools/profile.py init
   python3 <skill_root>/tools/profile.py add-rule --stage <stage> --rule <sanitized_rule>
   ```

7. If it supersedes an older rule, mark the older lesson as superseded and keep only the active rule in `DESIGN.md`.
8. Never copy private context into this skill repository or GitHub automatically.

## Product Candidates

For a generic hard correctness issue, record only a sanitized description in the user's project and tell the maintainer it is eligible for review. Publication remains a separate maintainer action.

## Completion

Show the exact confirmed rule, its scope, and the file updated.
