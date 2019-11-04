# Aisle Map - Visual Sales Data
The goal for this project is to create a web application using Flask which will allow employees to login and view/update their store's aisle data. This tool will aid them in merchandising and ordering effectively to increase sales and minimize loss.

# Internal Language

Like any industry, internal language exists in grocery which I will define as needed:

set, or bay : Grocery store aisles are composed of bays measuring ≈ 1m in width. These bays contain shelves which are adjustable in placement and once stocked result in the set. For example, the tea "set", is one or more bays which are merchandised with tea products.

facings: More often than not, top selling items have multiple facings on in a set. A bag of salted chips may sell more than a flavoured variety, so two facings of the former allows for more product to be stocked.

<p align="center">
<img src="https://github.com/aaronphaneuf/aisle_map/blob/master/images/tea_heatmap.PNG">
</p>
Imagine the benefit of being able to see a set not in terms of colourful packaging, but statistical sales data with variable date ranges (week-to-date, year-to-date, etc). The head of that department could determine the amount of facings a product should have, as well as what items should be cut, or discontinued from a set. 
The image is purposely sized so item information is not visible, out of respect for my employers data, however, each cell contains the following information:

Product Name
Product Brand
Product Size
Sales History

# aile_map.py

Currently, the program will exist as an executable, which will output a .html file resulting in the above image.
An individual will scan each product in a bay from left to right, including multiples for each facing of a product. This will result in a plain text file of UPCs, titled "storefile.txt".
