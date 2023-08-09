# Gxscalc

This is a Python package for speed-based calculation of F-ZERO GX.

## Requirements

This package requires pandas and matplotlib.
Also, speed data files created by [my AviUtl plugin](https://github.com/cycloawaodorin/fzgx_smr_ks) are required as input.

## Installation

Gxscalc is available on PyPI:

    $ python -m pip install gxscalc

## Usage

```python3
from gxscalc import mtp

mtp('./sample/sa70_on.txt', './sample/sa70_off.txt') #=> (1224.2514114466828, -2.465287050388536)
```

### `gxscalc.mtp(on, off, *, std=5, rng=10, return_figure=False, with_frames=True)`
Calculate the approximated MT point from two speed data files of deceleration.
The accuracy compared to [Naegleria's spreadsheet](https://docs.google.com/spreadsheets/d/1kyl0kAi_-NaM9RCPIwThixogTYESL4zdpmbbH_qDlmI/edit#gid=0) is within about 3 km/h.

<dl>
 <dt><code>on</code>: str | pandas.DataFrame</dt>
  <dd>File path or DataFrame of speed data for deceleration while going on the accelerator.</dd>
 <dt><code>off</code>: str | pandas.DataFrame</dt>
  <dd>File path or DataFrame of speed data for deceleration while going off the accelerator.</dd>
 <dt><code>std</code>: numeric</dt>
  <dd>Standard deviation of gaussian window for moving average.</dd>
 <dt><code>rng</code>: numeric</dt>
  <dd>Values farther than <code>std*rng</code> will not be used for moving average.</dd>
 <dt><code>return_figure</code>: boolean</dt>
  <dd>If this is true, mtp() returns figure of speed vs moving averaged acceleration graph as optional output.</dd>
 <dt><code>with_frames</code>: boolean</dt>
  <dd>Set this false if <code>on</code> and <code>off</code> don't have the frame column.</dd>
 <dt>returns: (float, float, [matplotlib.figure.Figure, matplotlib.axes.Axes])</dt>
  <dd>Returns the tuple of (MT point [km/h], Acceleration at MT point [km/h/f]). If <code>return_figure</code> is <code>True</code>, returns (MT point, Acceleration at MT point, <code>Figure</code> of the graph, <code>Axes</code> of the graph) instead. If no cross points are detected from the inputs, it returns (<code>None</code>, <code>None</code>) or (<code>None</code>, <code>None</code>, <code>Figure</code>, <code>Axes</code>) since the MT point can not be calculated.</dd>
</dl>

### `gxscalc.distance(file, fps=60)`
Calculate the approximated travelled distance of given speed data file via trapezoidal rule.
The unit of input speed is km/h and the unit of output length is m.

<dl>
 <dt><code>file</code>: str | pandas.DataFrame</dt>
  <dd>File path or DataFrame of speed data to be calculated.</dd>
 <dt><code>fps</code>: numeric</dt>
  <dd>The reciprocal of time between the adjacent speed values, in seconds.</dd>
 <dt><code>with_frames</code>: boolean</dt>
  <dd>Set this false if <code>file</code> doesn't have the frame column.</dd>
 <dt>returns: float</dt>
  <dd>Returns the travelled distance in meter.</dd>
</dl>


## Notice
The input speed data files are assumed to be created by [my AviUtl plugin](https://github.com/cycloawaodorin/fzgx_smr_ks).
The files should include frame numbers and separators should be spaces (default settings of the plugin).
'./sample/sa70_on.txt' and './sample/sa70_off.txt' are sample input files, which are data of Space Angler at 70%.

If you have speed-only text file, call functions with `with_frames=False`.
If you need some modification before calling gxscalc functions, you can send DataFrame objects instead of file paths of the speed data.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/cycloawaodorin/gxscalc.
