# homeBuyerFire
[![Build Status](https://travis-ci.com/MattThomas9/Home-Buyer-Fire.svg?branch=master)](https://travis-ci.com/MattThomas9/Home-Buyer-Fire)
[![Actions Status](https://github.com/MattThomas9/Home-Buyer-Fire/workflows/Lint/badge.svg)](https://github.com/MattThomas9/Home-Buyer-Fire/actions)
[![codecov](https://codecov.io/gh/MattThomas9/Home-Buyer-Fire/branch/master/graph/badge.svg?token=5AJUA8I31G)](https://codecov.io/gh/MattThomas9/Home-Buyer-Fire/)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMattThomas9%2FHome-Buyer-Fire.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FMattThomas9%2FHome-Buyer-Fire?ref=badge_shield)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<a href="https://pypi.org/project/hbf/"><img src="https://docs.google.com/drawings/d/e/2PACX-1vR8jfxdu85njA8C-Fvv0QCGoNrIn8swDLRArTq0IZqmbz9K0_Qe-eHAJJn0OCaIJfUiU8U6EQ4rl7y2/pub?w=229&h=278" alt="hbf logo" align="right" /></a>

## Project Overview

A program to predict a home's sell price using data scraped from the internet.

`homeBuyerFire` is actively developed using a Python 3.7 interpreter.

## Installation

```
pip install hbf
```

## Example

Starting from the project's parent directory:

```
python example.py
```

```
Scraping Zillow |████████████████████████████████| 7/7

                                       Address  Sell Price  Beds  Baths  Home Size      Home Type  Year Built                         Heating  Cooling Parking  Lot Size
0  11705 College View Dr Silver Spring MD 20902    293000.0   2.0    2.0     1526.0  Single Family      1951.0                      Forced air  Central     NaN    6791.0
1  11714 College View Dr Silver Spring MD 20902    465000.0   4.0    3.0     2843.0  Single Family      1962.0  Baseboard, Heat pump, Electric  Central     NaN    8115.0
2         3406 Glorus Pl Silver Spring MD 20902    785000.0   5.0    5.0     5872.0  Single Family      2006.0                      Forced air  Central     NaN   10890.0
3  11703 College View Dr Silver Spring MD 20902    475000.0   4.0    2.0     1982.0  Single Family      1951.0                 Forced air, Gas  Central     NaN    6930.0
4         3400 Glorus Pl Silver Spring MD 20902    395000.0   4.0    3.0     1914.0  Single Family      1953.0                None, Forced air  Central     NaN    7178.0
5    11714 Veirs Mill Rd Silver Spring MD 20902    383000.0   6.0    3.0     1836.0  Single Family      1953.0                      Forced air  Central     NaN    6812.0
6      3402 Pendleton Dr Silver Spring MD 20902    340000.0   2.0    1.0      882.0  Single Family      1951.0                      Forced air  Central     NaN    7609.0

--- 15.11016297340393 seconds ---
```

## Contact Info

- @MattThomas9
- @AmritPatel


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMattThomas9%2FHome-Buyer-Fire.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FMattThomas9%2FHome-Buyer-Fire?ref=badge_large)
