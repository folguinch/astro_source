# Astro Source

Tools for managing source information and associated data.

## Dependencies:

- Commonly used packages: `astropy`, `numpy`
- [`toolkit`](https://github.com/folguinch/toolkit), [`configparseradv`](https://github.com/folguinch/configparseradv)

## How it works?

A source is defined by a configuration file of the form:

```INI
[INFO]
name: my_source
distance: 1 kpc
ra: 1h00m00s
dec: 1d00m00s
frame: icrs
luminosity: 1 L_sun
```

The values associated to `ra`, `dec`, `distance` and `luminosity` can be accesed directly as attributes.
These will return an `astropy` `Quantity` representation of the stored values.
Additional stored properties can also be read as `Quantity` with the `get_quantity` method.
The position of the source can also be retrieved as an `astropy.coordinates.SkyCoord` object through the attribute `position`.

Addtional sections can be used to specify data associated to that source or subsources:

```INI
[MM1]
type: subsource
name: mm1
ra: 1h00m01s
dec: 1d00m01s
radius: 0.1 arcsec

[data1]
type: fits_file
file: /path/to/file.fits

[data2]
type: spectral_cube
file: /path/to/file.fits
```

Subsource information can be retrieved by, e.g., `source.subsources['MM1'].info['radius']`.
The data is loaded upon request (e.g. `source.load_data(data1)`) to save resources.

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
