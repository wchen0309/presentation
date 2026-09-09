# Premium desktop DPT enclosure concept

This branch contains a parametric CadQuery redesign for a premium desktop double-pulse-test enclosure.

## Design intent
- Closed-solid CAD, not surface-only concept geometry.
- Separate fixed left hood and hinged right test chamber.
- Large top access for oscilloscope probes and DUT replacement.
- Smoked observation window, black technical waist band, silver/white instrument body, four structural corner posts.
- Internal electronics intentionally omitted at this stage so the industrial-design envelope can be settled first.

## Current envelope
Approx. 430 mm W × 390 mm D × 300 mm H excluding the opened lid.

## Files
- `premium_dpt_enclosure.py`: parametric CadQuery source.
- `DPT_Premium_Enclosure_Closed.step`: closed-state STEP.
- `DPT_Premium_Enclosure_Open.step`: open-state STEP.
- `DPT_Premium_Enclosure_Closed_preview.png`: closed-state preview.
- `DPT_Premium_Enclosure_Open_preview.png`: open-state preview.

## Open-source reference
The parametric enclosure workflow is derived in spirit from `CadQuery/cadquery-contrib/examples/Parametric_Enclosure.py`, which is MIT licensed. The present enclosure geometry, proportions, chamber split, fascia, lid, windows and posts are newly designed for this DPT concept.

Original MIT copyright: Copyright (c) 2018 Dave Cowden.
