# Pack Regeneration — Badar Mechanization v0.2

## Purpose

The active A/B ZIPs are generated artifacts and conversation downloads can expire.

This document records how to regenerate them without changing the scientific study.

## Frozen inputs

- external evidence commit:
  `bd0037e06a881a066e0cd8070b635cace59240d1`
- candidate manifest:
  `candidate-events-v0.2.csv`
- frozen frame selection:
  `frame-selection-v0.2.csv`
- annotator instructions:
  `INDEPENDENT-ANNOTATOR-INSTRUCTIONS-v0.2.md`
- builder:
  `tools/build_blind_packs.py`

## Frozen frame set

`frame-selection-v0.2.csv` identifies:

- 43 events
- 102 unique full-resolution source-frame files
- all events eligible
- maximum latest-frame gap 182 seconds

The source images live in the private external evidence repo under:

`traders/badar-tanveer/evidence/stream_frames/<stream_id>/`

## Historical successful build

GitHub Actions run:

`45954672567`

Build results are frozen in `PACK-FREEZE.md`.

## Temporary staging method

Because the external evidence repo is private and a Target-First workflow token cannot read it directly:

1. create a disposable Target-First branch from current main;
2. copy only the 102 blobs listed in `frame-selection-v0.2.csv` to:
   `_badar_v02_source_frames/<stream>/<file>.jpg`;
3. verify exactly 102 expected paths and zero extras;
4. run the builder with:
   `BADAR_V02_SOURCE_ROOT=<staged frame root>`;
5. freeze pack/crosswalk hashes;
6. move the disposable branch ref back to Target-First main so the staged binary commit chain is no longer referenced.

No source-image binaries belong in Target-First main.

## Rebuild identity

Blind IDs are intentionally random.

Therefore a regenerated pack is scientifically equivalent but will not have the same ZIP hash or crosswalk hash.

Once an A/B pack generation has been handed to annotators, its exact hashes and corresponding crosswalk commitment become the active frozen version and must not be replaced mid-study.

The current active generation is the one in:

`active-pack-manifest-v0.2.csv`

## Current active hashes

- A:
  `8a3673345c3f35ffbfb8acc7ed7b6ede9e83210d48c563eb238dccdcac026a67`
- B:
  `1561b0a9ea61b22b7968247ae39e4c18420a402479adc93513ba754dade2bca8`
- crosswalk commitment:
  `8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096`

Do not regenerate once annotation has begun unless the active generation is formally abandoned and a new version is frozen before viewing returned labels.
