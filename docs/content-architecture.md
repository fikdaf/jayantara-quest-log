# Content Architecture

## Source of truth

The canonical learning content lives in `quests/day-XX.md`.

Each quest may begin with YAML frontmatter:

```yaml
---
id: day-01
day: 1
title: Gerbang Hiragana Pass
type: lesson
phase: foundation
level: N5
estimated_minutes: 45
skills:
  - hiragana
reward:
  badge: rookie-i
---
```

The Markdown body remains the human-readable lesson. Metadata is consumed by tooling and future applications.

## Generated data

`scripts/build_curriculum.py` converts quest frontmatter into `data/quests.generated.json`. Generated data is an index, not a second authoring surface. Do not hand-edit it.

## Curriculum configuration

`data/curriculum.yaml` defines the high-level six-phase learning journey and checkpoint dependencies. `data/badges.yaml` defines rewards.

The long-term goal is to reduce duplication by gradually moving day-specific title/type/phase/reward metadata out of `curriculum.yaml` and into quest frontmatter, while keeping phase-level configuration in `curriculum.yaml`.

## Validation

CI validates:

1. all 30 quest files exist;
2. required Markdown sections exist;
3. frontmatter identifies the correct day and phase;
4. quest type is valid;
5. a badge reward exists;
6. the generated index is reproducible.

## Application contract

A future web application should consume the generated quest index rather than parsing README content. The intended flow is:

`quests/*.md` → parser → `data/quests.generated.json` → web/quiz/progress/badge systems.
