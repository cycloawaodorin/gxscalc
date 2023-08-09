# Change Log

## 0.0.1 06.Jul.2020
- First release.

## 0.0.2 26.Jul.2020
- Remove numpy from requirements.
- Add `gxscalc.distance()`.

## 0.0.3 26.Jun.2021
- Add keyword argument `return_figure` into `gxscalc.mtp()`.

## 0.0.4 26.Jun.2021
- Fix legend of `return_figure=True` for `gxscalc.mtp()`.

## 0.0.5 10.Oct.2021
- `gxscalc.mtp()` has been changed to return (None, None) when no cross points are detected.

## 0.1.0 09.Aug.2023
- Slightly changed the algorithm of `gxscalc.mtp()`.
- Add estimated MT point in the figure of `gxscalc.mtp()`.
- Add `with_frames` keyword argument into `gxscalc.mtp()` and `gxscalc.distance`.
- `gxscalc.mtp()` and `gxscalc.distance` accept direct DataFrame inputs.
