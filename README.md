# Toronto Rental ETL Project
<img src="Toronto_Rental_ETL_Project/Images/toronto.jpg" alt="Headline" width="1000"/>

While Toronto is a beautiful place to live, no one would claim it is easy to find a place to rent in Toronto. To help current and potenial Toronto residents better understand rental options available to them, we create a database containing the most recent rental listings as well other indicators of it what might be like to live at each address. 

The following outlines the process for extracting, tranforming and loading data into the database. 

<h2>Extract</h2>
<hr>

<h4>Rental Data</h4>

<p>INTRO<p>
<h5>Craigslist</h5>
<p>Description<p>
<h5>kijji</h5>
<p>Description<p>

<h4>Toronto Police Services Open Data</h4>

<p>INTRO <p>

<h5>Major Crime Indicators</h5>
<p>Toronto Police Services provides a <a href="https://data.torontopolice.on.ca/pages/catalogue">catalogue of data sources</a> that includes incidence of crime.

Crimes are tracked in a number of categories and availabe in consolidated dataset - Major Crime Indicators (MCI). TPS provides an <ahref="https://data.torontopolice.on.ca/datasets/mci-metadata/geoservice">API</a>to easily access the MCI. 

<p>
<h5>Community Assets</h5>
<p> The TPS data catalogue includes <ahref="https://torontops.maps.arcgis.com/home/item.html?id=077c19d8628b44c7ab9f0fff75a55211&view=list&sortOrder=true&sortField=defaultFSOrder#data">data tables</a> identifying organizations providing services to Toronto communities. Unfortunately, this data source is not accessible via an API. Web scrapping was used to extract the community asset data.<p>

The website is dynamic, meaning it needs to be interacted with inorder for the data of interest to be accessed from back-end server then displayed on the webpage. 

The Selenium and BeautifulSoup libraries were used to interact with and extract the data table rows (see PATH TO "Community_Assets.ipynb"). 

The webpage provides access to different tables via drop-down menu. Selenium's Select function was used to move between tables. 

The static HTML only contains a subset of the data tables rows at a given time. In order to access all the data rows, the code iteratively scrolls through the data tables and scrapes the staic HTML. Scrolling was achieved by the last row in the static HTML and clicking on it via Selenium's click() function. This triggered teh Javascript to view that row as the beginning of new top row thus updating the staic HTML.    

<h4>Government of Canada 2015 Income Data</h4>

<hr>
<p>INTRO<p>

<h2> Extract</h2>
<hr>

<h4>Rental Data</h4>

<p>INTRO<p>
<h5>Craigslist</h5>
<p>Description<p>
<h5>kijji</h5>
<p>Description<p>

<h4>Toronto Police Services Open Data</h4>

<p>INTRO<p>
<h5>Major Crime Indicators</h5>
<p>Description<p>
  
<h5>Community Assets</h5>
<p>Each data table was transformed into a dataframe. Once duplicates were removed, the individual dataframes were incorparated into a master dataframe.

Further transformations then included removing rows without postal information; normalizing how fees for services are described; and updating headers to reflect best practices for SQL databases<p>

<h4>Government of Canada 2015 Income Data</h4>

<hr>
<p>INTRO<p>

<h2>Load</h2>
<hr>
<p>INTRO<p>
<img src="Toronto_Rental_ETL_Project/Images/ERD.jpg" alt="ERD" width="1000"/>

