# homeBuyerFire
[![Build Status](https://travis-ci.com/AmritPatel/Home-Buyer-Fire.svg?branch=master)](https://travis-ci.com/AmritPatel/Home-Buyer-Fire)
[![Actions Status](https://github.com/AmritPatel/Home-Buyer-Fire/workflows/Lint/badge.svg)](https://github.com/AmritPatel/Home-Buyer-Fire/actions)
[![codecov](https://codecov.io/gh/AmritPatel/Home-Buyer-Fire/branch/master/graph/badge.svg?token=5AJUA8I31G)](https://codecov.io/gh/AmritPatel/Home-Buyer-Fire/)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FAmritPatel%2FHome-Buyer-Fire.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FAmritPatel%2FHome-Buyer-Fire?ref=badge_shield)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Project Overview

A program to predict a home's sell price using data scraped from the internet.

`homeBuyerFire` was written in Python 3.7.

## Getting Started

### Dependencies

- `beautifulsoup4`
- `geopy`
- `requests`
- `pandas`
- `configparser`

### List of Files

List all input and output files, even those considered self-explanatory. Link to specifications for standard formats and list the required fields and acceptable values in other files. If there is no rigorous definition for a format, explain its parts as clearly as possible in plain English.

#### Input

Test whatup chad

#### Output

### Example

Starting from the project's parent directory:

```
python3 ./src/reScrape.py [*path to input file*]/[*inputFilename*]
```

```
The address has been GeoCoded!
Searching within a square area of half-width 0.1 miles.
Only 1 page of Zillow search results exist in this search box.
8 recently sold homes on Zillow were found within the search box.
https://www.zillow.com/homedetails/11705-College-View-Dr-Silver-Spring-MD-20902/37316339_zpid/
https://www.zillow.com/homedetails/11714-College-View-Dr-Silver-Spring-MD-20902/37301330_zpid/
https://www.zillow.com/homedetails/3406-Glorus-Pl-Silver-Spring-MD-20902/37301367_zpid/
https://www.zillow.com/homedetails/11703-College-View-Dr-Silver-Spring-MD-20902/37316329_zpid/
https://www.zillow.com/homedetails/3400-Glorus-Pl-Silver-Spring-MD-20902/37301374_zpid/
https://www.zillow.com/homedetails/11714-Veirs-Mill-Rd-Silver-Spring-MD-20902/37301521_zpid/
https://www.zillow.com/homedetails/3402-Pendleton-Dr-Silver-Spring-MD-20902/37316316_zpid/
https://www.zillow.com/homedetails/3411-Pendleton-Dr-Silver-Spring-MD-20902/37316382_zpid/
The number of Sold Home Zillow Links scraped from all pages equals
the Zillow Result Count that was scraped from the initial page.
                                        Address Sell Price Beds Baths Home Size      Home Type Year Built               Heating  Cooling    Parking    Lot Size
0  11705 College View Dr Silver Spring MD 20902     293000    2     2     1,526  Single Family       1951            Forced air  Central    No Data  6,791 sqft
1  11714 College View Dr Silver Spring MD 20902     465000    4     3     2,843  Single Family       1962  Baseboard, Heat pump  Central    No Data  8,115 sqft
2         3406 Glorus Pl Silver Spring MD 20902     785000    5     5     5,872  Single Family       2006            Forced air  Central    No Data  0.25 Acres
3  11703 College View Dr Silver Spring MD 20902     475000    4     2     1,982  Single Family       1951            Forced air  Central  On street  6,930 sqft
4         3400 Glorus Pl Silver Spring MD 20902     395000    4     3     1,914  Single Family       1953      None, Forced air  Central    No Data  7,178 sqft
5    11714 Veirs Mill Rd Silver Spring MD 20902     383000    6     3     1,836  Single Family       1953            Forced air  Central    No Data  6,812 sqft
6      3402 Pendleton Dr Silver Spring MD 20902     340000    2     1       882  Single Family       1951            Forced air  Central    No Data  7,609 sqft
7      3411 Pendleton Dr Silver Spring MD 20902     425000   --     2     1,082  Single Family       1951                 Other  No Data    No Data  9,700 sqft
```

## Contact Info

- @MattThomas9
- @AmritPatel


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FAmritPatel%2FHome-Buyer-Fire.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FAmritPatel%2FHome-Buyer-Fire?ref=badge_large)
