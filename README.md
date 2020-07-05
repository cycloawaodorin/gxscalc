# Gxscalc

This is a Python package for speed-based calculation of F-ZERO GX.

## Requirements

This package requires numpy and pandas.
Also, speed data files created by [my AviUtl plugin](https://github.com/cycloawaodorin/fzgx_smr_ks) is required as input.

## Installation

Gxscalc is available on PyPI:

    $ pip install gxscalc

## Usage

### `gxscalc.mtp(on, off, *, std=5, rng=10)`
Calculate the approximated MT point from two speed data files of deceleration.
The accuracy compared to [Naegleria's spreadsheet](https://docs.google.com/spreadsheets/d/1kyl0kAi_-NaM9RCPIwThixogTYESL4zdpmbbH_qDlmI/edit#gid=0) is within about 3 km/h.

<dl>
 <dt><code>on</code>: str</dt>
  <dd>File path of speed data for deceleration while going on the accelerator.</dd>
 <dt><code>off</code>: str</dt>
  <dd>File path of speed data for deceleration while going off the accelerator.</dd>
 <dt><code>std</code>: numeric</dt>
  <dd>Standard deviation of gaussian window for moving average.</dd>
 <dt><code>rng</code>: numeric</dt>
  <dd>Values farther than <code>std*rng</code> will not be used for moving average.</dd>
 <dt>returns: (float, float)</dt>
  <dd>Returns the tuple of (MT point [km/h], Acceleration at MT point [km/h/f]).</dd>
</dl>

```python3
from gxscalc import mtp

mtp('./sample/sa70_on.txt', './sample/sa70_off.txt') #=> (1224.330134264905, -2.4656191600475066)
```

## Notice

The input speed data files are assumed to be created by [my AviUtl plugin](https://github.com/cycloawaodorin/fzgx_smr_ks).
The files should include frame numbers and separators should be spaces (default settings of the plugin).
'./sample/sa70_on.txt' and './sample/sa70_off.txt' are sample input files, which are data of Space Angler at 70%.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/cycloawaodorin/gxscalc.
