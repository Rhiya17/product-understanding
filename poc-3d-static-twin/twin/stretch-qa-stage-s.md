# Stage S deformation QA — INTERNAL ONLY

**Rights:** Tripo3D license check OPEN — do not ship

Every evaluated mesh edge was measured across all 96 frames as current length / frame-1 length. Ratios above 1.6 are visible artifacts. No geometry was invented to hide them.

| Joint band | Edges | Worst ratio | Frame | > 1.6 |
|---|---:|---:|---:|:---:|
| `front_frame_about_hub112` | 726 | 29.648× | 84 | YES |
| `lower_handle_about_hub112` | 696 | 29.648× | 84 | YES |
| `upper_handle_pivot118` | 2121 | 15.607× | 84 | YES |
| `seat_follow` | 5911 | 71.874× | 84 | YES |
| `canopy_fold` | 1888 | 11.978× | 82 | YES |
| `belly_bar_follow` | 2557 | 17.074× | 84 | YES |
| `cup_holder_compact_rotation` | 0 | n/a | n/a | no |
| `front_caster_left_prepare` | 2064 | 8.733× | 50 | YES |
| `front_caster_right_prepare` | 0 | n/a | n/a | no |
| `basket_soft_envelope_collapse` | 21613 | 25.783× | 84 | YES |

Whole-mesh worst case: **192.556× at frame 84** (edge 72474).

Mitigation applied: rigid nearest-part masks everywhere except the declared 3 cm front-frame, seat, and canopy hinge bands. The remaining fused-shell artifacts are disclosed rather than patched with invented separations or hidden linkage geometry.

Bands with no measurable scan surface: `cup_holder_compact_rotation`, `front_caster_right_prepare`. This means the nearest-part binding found no provider-mesh edges in that spatial band; it is not reported as a zero-stretch pass.
