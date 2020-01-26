# Aisle Map - Visual Sales Data
A visual representation of sales data.

<p align="center">
<img src="https://github.com/aaronphaneuf/aisle_map/blob/master/images/tea_heatmap.PNG">
</p>

## What is AisleMap?
AisleMap is simply a heat map of product on a shelf. Sales data is displayed in the same placement as it appears on your
physical display, because the product is entered left to right.

## What is the purpose of AisleMap?
AisleMap is meant as a tool to aid those who merchandise and order product. On the merchandising side, top selling product
could be switched to the bottom shelf, often without loss of sales and lower selling product could be moved to eye level, as a strategy to increase sales. For ordering, sales data is essential to balancing having enough stock and minimizing loss.

<p align="center">
<img src="https://github.com/aaronphaneuf/aisle_map/blob/master/images/comparison.PNG">
</p>

## Internal Language
Like any industry, internal language exists in grocery which I will define as needed here:

set or bay : Grocery store aisles are composed of bays measuring ≈ 1m in width. These bays contain shelves which are adjustable in placement and once stocked result in the set. For example, the tea "set", is one or more bays which are merchandised with tea products.

facings: More often than not, top selling items have multiple facings on in a set. A bag of salted chips may sell more than a flavoured variety, so two facings of the former allows for more product to be stocked.

UPC/PLU: A unique identifier for an item. Commonly found on the back or bottom of a product.

## Usage
The store compiles a .txt file containing two required columns: UPC and Quantity (of facings). Since their easiest option of scanning
multiple items is a handheld scanner running our POS software, the output file looks like the following, which I take into consideration
when declaring the dataframe:

<p align="center">
<img src="https://github.com/aaronphaneuf/aisle_map/blob/master/images/storescan.PNG">
</p>

When a shelf has ended, 5 digit PLUs are entered to signify the start of a new shelf. These identifiers are:
[77985, 77986, 77987, 77988, 77989, 77990, 77991, 77992, 77993, 77994, 77995, 77996, 77997, 77998, 77999]

aislemap.py is then executed, asking for date input and quickly generates a heat map in html format.

## Expanding
The program currently exists as an executable, which outputs a .html file. The main goal is to have it running on a server in a Flask environment which will save local store data and allow for quicker, more efficient data filtering.
