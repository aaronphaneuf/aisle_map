#import modules
import datetime
import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import pyodbc
from matplotlib.colors import rgb2hex

#declare shelf break upcs
shelf_breaks = [77985, 77986, 77987, 77988, 77989, 77990, 77991, 77992, 77993, 77994, 77995, 77996, 77997, 77998, 77999]

#determine YTD variables
current_year = datetime.date.today().replace(month=1, day=1)
current_year_string = str(current_year) + ' 00:00:00'
yesterday = datetime.date.today() - datetime.timedelta(days=1)
yesterday_string = str(yesterday) + ' 23:59:59'
yesterday = datetime.date.today() - datetime.timedelta(days=1)

#declare custom date variables
custom_start = ""
custom_end = ""

#declare selected date list
selected_date = []

#date range dictionary
date_ranges = {1: ['2018-01-01 00:00:00', '2018-12-31 23:59:59'], 2: ['2019-01-01 00:00:00', '2019-12-31 23:59:59'], 3: [current_year_string, yesterday_string]}

#print out choices
print("1: 2018")
print("2: 2019")
print("3: YTD")
print("4: Custom")

#ask user to select a rgba_values
entry = input("Select a date range : ")
entry = int(entry)

#if user selection is a custom date range, ask for values and append to selected_date list
if entry == 4:
    custom_start = input("Enter start date (example: 2019-04-01 year-month-day) : ")
    custom_end = input("Enter end date (example: 2019-04-30 year-month-day) :")
    selected_date.append(custom_start + ' 00:00:00')
    selected_date.append(custom_end + ' 23:59:59')
else:
    selected_date.append(date_ranges[entry][0])
    selected_date.append(date_ranges[entry][1])

#declare main function
def generate_heatmap():

    #read txt file, exported from web office. Delimited by tabs, and ignoring the first 4 rows
    df = pd.read_csv('storescan.txt', header=None, delimiter='\t', skiprows=(0,1,2,3), usecols=range(2))

    #counter for duplicate_upcs variable
    df_counter = 0

    #determine which upcs were scanned more than once, and copy them below each match
    duplicate_upcs = [df[1][df_counter] if df[1][df_counter] != 1 else 1 for df[1][df_counter] in df[1]]
    df = df.loc[np.repeat(df.index.values, duplicate_upcs)]

    #since the duplicate upcs have the same index, reset it
    df = df.reset_index()

    #drop unessecary columns
    df = df.drop(df.columns[[0,2]], axis=1)

    #name header
    df.columns = ['UPC']

    #declare columns for xciks abd yrows
    df['Yrows'] = 'Yrows'
    df['Xcols'] = 'XCols'

    #declare variables for following for loop.
    xcols = 1
    shelf_counter = 1

    #finds UPC 599999333348 and increments xcols and shelf_counter based off the results of the if statement
    for idx, val in enumerate(df.itertuples()):
        if df.loc[idx, 'UPC'] in shelf_breaks:
            #If 599999333348 is found, then we're on a new shelf. Set its x and y value to 0, 0
            shelf_counter += 1
            xcols = 1
            df.loc[idx, 'Yrows'] = 0
            df.loc[idx, 'Xcols'] = 0
        else:
            #use shelf_counter as the yrow value and xcols as the xcol, then increment xcols
            df.loc[idx, 'Yrows'] = shelf_counter
            df.loc[idx, 'Xcols'] = xcols
            xcols += 1

    #remove values with shelf indicator UPCs and reindex the dataframe. Because for some reason it skips the
    #index with tose UPCs. Example: 1, 2, 3, 4, 5, 6, 7, 9 (8 is missing)
    df = df[(df !=77985).all(axis=1)]
    df = df[(df !=77986).all(axis=1)]
    df = df[(df !=77987).all(axis=1)]
    df = df[(df !=77988).all(axis=1)]
    df = df[(df !=77989).all(axis=1)]
    df = df[(df !=77990).all(axis=1)]
    df = df[(df !=77991).all(axis=1)]
    df = df[(df !=77992).all(axis=1)]
    df = df[(df !=77993).all(axis=1)]
    df = df[(df !=77994).all(axis=1)]
    df = df[(df !=77995).all(axis=1)]
    df = df[(df !=77996).all(axis=1)]
    df = df[(df !=77997).all(axis=1)]
    df = df[(df !=77998).all(axis=1)]
    df = df[(df !=77999).all(axis=1)]

    df = df.reset_index()

    #establish sql connection
    conn = pyodbc.connect('DSN=Prototype')
    cursor = conn.cursor()

    #declare variable to hold segment of sql query containing list of upcs from df
    list_of_upcs = ""

    #itterate through upcs in df and append to list_of_upcs
    for x in df['UPC']:
        list_of_upcs += """OR (t1.INV_ScanCode LIKE '%{0}%' OR t2.ASC_ScanCode LIKE '%{0}%' ) """.format(x)

    #declare sql query, containing list_of_upcs in the middle
    #NOTE FOR SELF: AND INV_ScanCode LIKE '' might be slowing this down.
    sql_query = """
    SELECT INV_PK, INV_CPK, INV_ScanCode, Brd_Name, INV_Name, INV_Size, t2.ASC_ScanCode
    FROM v_InventoryMaster AS t1
    LEFT JOIN AdditionalScanCodes AS t2 ON ASC_INV_FK = INV_PK AND ASC_INV_CFK = INV_CPK
    WHERE t1.INV_STO_FK = 11
    AND INV_ScanCode LIKE '' """ + list_of_upcs + """
    GROUP BY INV_PK, INV_CPK, INV_ScanCode, Brd_Name, INV_Name, INV_Size, t2.ASC_ScanCode
    """

    #attach sql_query to the connection
    query = pd.read_sql_query(sql_query, conn)
    #assign the result to df2
    df2 = pd.DataFrame(query)
    #rename columns
    df2.columns = ['INV_PK', 'INV_CPK', 'UPC', 'Brand', 'Name', 'Size', 'Alternate_ID']

    #convert UPC from string to int64
    df2['UPC'] = df2['UPC'] = pd.to_numeric(df2['UPC'])
    df2['UPC'] = df2['UPC'].astype('int64')

    #set the index equal to the UPC column
    df2.set_index('UPC', inplace=True)
    #create new columns in df mapped to df2 on UPC
    df['INV_PK'] = df.UPC.map(df2.INV_PK)
    df['INV_CPK'] = df.UPC.map(df2.INV_CPK)
    df['Brand'] = df.UPC.map(df2.Brand)
    df['Name'] = df.UPC.map(df2.Name)
    df['Size'] = df.UPC.map(df2.Size)

    #determine non-null values in Alternate_ID in df2 and assign those to df3
    df3 = df2[df2.Alternate_ID.notnull()]
    #remove non-numeric characters from Alternate_ID, which would crash the script
    df3['Alternate_ID'] = df3['Alternate_ID'].str.extract('(\d+)', expand=False)
    #convert to int64
    df3['Alternate_ID'] = df3['Alternate_ID'] = pd.to_numeric(df3['Alternate_ID'])
    df3['Alternate_ID'] = df3['Alternate_ID'].astype('int64')
    #set index to alternate_id
    df3.set_index('Alternate_ID', inplace=True)

    #map missing values in a new column
    df['INV_PK2'] = df.UPC.map(df3.INV_PK)
    df['INV_CPK2'] = df.UPC.map(df3.INV_CPK)
    df['Brand2'] = df.UPC.map(df3.Brand)
    df['Name2'] = df.UPC.map(df3.Name)
    df['Size2'] = df.UPC.map(df3.Size)

    #combine into one column
    df['INV_PK'] = df['INV_PK'].fillna(df['INV_PK2'])
    df['INV_CPK'] = df['INV_CPK'].fillna(df['INV_CPK2'])
    df['Brand'] = df['Brand'].fillna(df['Brand2'])
    df['Name'] = df['Name'].fillna(df['Name2'])
    df['Size'] = df['Size'].fillna(df['Size2'])

    #fill NAs (if there are an)
    df['INV_PK'].fillna(99999, inplace=True)
    df['INV_CPK'].fillna(99999, inplace=True)

    #convert to int64
    df['INV_PK'] = df['INV_PK'].astype('int64')
    df['INV_CPK'] = df['INV_CPK'].astype('int64')

    #drop columns
    df = df.drop(columns=['INV_PK2', 'INV_CPK2', 'Brand2', 'Name2', 'Size2'])

    #declare combined_list, which will contain the string for each items INV_FK and INV_CFK
    combined_list = ""
    counter = 0
    for x in df['INV_PK']:
        combined_list += """OR (ITI_INV_FK = {0} AND ITI_INV_CFK = {1})""".format(df['INV_PK'][counter], df['INV_CPK'][counter])
        counter += 1

    #SQL query pulling sales data from v_TJTrans (V_Trans for individual stores)
    sql_query = """
    SELECT ITI_INV_FK, ITI_INV_CFK, SUM(TLI_Quantity) AS Quantity
    FROM v_TJTrans
    WHERE TRN_STO_FK = 11
    AND TRN_StartTime >= ?
    AND TRN_EndTime <= ?
    AND TLI_LIT_FK <> 4
    AND ITI_VOID = 0
    AND TRN_AllVoid = 0
    AND (

    (ITI_INV_FK = '' AND ITI_INV_CFK = '') """ + combined_list + """
    )
    GROUP BY ITI_INV_FK, ITI_INV_CFK
    """

    query = pd.read_sql_query(sql_query, conn, params =(selected_date[0], selected_date[1]))
    #assign the result to df4
    df4 = pd.DataFrame(query)
    #set the index to ITI_INF_FK, which is equal to INV_FK
    df4.set_index('ITI_INV_FK', inplace=True)
    #map df with new column, sales based off of df4
    df['Sales'] = df.INV_PK.map(df4.Quantity)
    df['Sales'].fillna(0, inplace=True)

    #declare numpy array with UPC and Sales column
    upc = np.array(df['UPC'])
    sold = np.array(df['Sales'])
    #pivot the result using Yrows and Xcols columns
    result = df.pivot(index='Yrows', columns='Xcols', values='Sales')
    #establish figure
    fig, ax = plt.subplots(figsize=(12,7))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    sns.heatmap(result, annot_kws={"size": 7}, fmt="", cmap='RdYlGn', linewidths=2, ax = ax, square=True)

    #now that the figure is generated, declare colour_data, which will hold the values for each colour
    colour_data = sns.heatmap(result)

    im = colour_data.collections[0]

    #pull colour data using cmap
    rgba_values = im.cmap(im.norm(im.get_array()))
    rgba_values = np.delete(rgba_values, np.s_[3], axis=1)

    #B is now equal to a numpy array containing the rgb values
    B = np.array(rgba_values*255, dtype=int)

    #declare html
    html = """
<!DOCTYPE html>
<html>
<head>
<title>POM Aisle - Heat Map </title>
<style>
body {
  background-color: white;
  font-family: Verdana;
}

a {
 color: black;
}

a:link {
  text-decoration: none;
}

a:visited {
  text-decoration: none;
}

a:hover {
  text-decoration: none;
  }

a:active {
  text-decoration: none;
}

.topnav {
  background-color: #32393f;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

.topnav a {
  float: left;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 16px;
}

.container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.grid {
  display: grid;
  grid-template-columns: repeat("""+str(df['Xcols'].max()) + """, 100px );
  grid-template-rows: repeat("""+ str(df['Yrows'].max()) + """, 85px);
  position: fixed;
  top: 60px;
}

.grid span {
  overflow: hidden;
  padding: 2px; 2px;
  margin: 2px;
  font-size: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  justify-content: space-evenly;
}

</style>
</head>
<body>

<div class="topnav">
<a>Calgary Shaganappi &nbsp&nbsp&nbsp&nbsp """ + selected_date[0].split(' ', 1)[0] + """  -  """ + selected_date[1].split(' ', 1)[0] + """</a>
</div>

<div class="container">
<div class="grid">
"""


    colour_list = []
    html_counter = 0

    for x in B:
        if x[0] == 0 and x[1] ==0 and x[2] == 0:

            html += """\
            <span style="background-color:rgba(160,173,173)"></span>"""

        else:

            html += """\
            <span style="background-color:rgba(""" + str(x[0]) + """,""" + str(x[1]) + """,""" + str(x[2]) + """)"><a href="https://23be5.catapultweboffice.com/weboffice/#Inventory:pk="""+ str(df['INV_PK'][html_counter])+"""%257C"""+str(df['INV_CPK'][html_counter])+""""><center>""" + str(df['Brand'][html_counter]) + """<br>""" + str(df['Name'][html_counter]) + """<br> """ + str(df['Size'][html_counter]) + """<br>""" + str(df['Sales'][html_counter]) + """</a></center></span>"""

            html_counter += 1

    html += """</div></div></body></html>"""
    html_file = open("heatmap.html", "w")
    html_file.write(html)
    html_file.close()


#call the function
generate_heatmap()
