The folder contains binary files for 1968, 70, and 1972 surveys.

They 1976 survey was too big for github it can be downloaded here:

https://catalog.archives.gov/id/1501572: "Download 1976 Survey (compressed)"

The "convert.py" file works for 68-72 files, just needs editing the last field, "convert1976.py" works for the 76 one.

Additionally the county and state data in corrupted, so I added a "county.py" script that fills the data using external table of cities.
