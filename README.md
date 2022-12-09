# CS6400
CS6400 DB Class Project. SIEM Mock Software

# Frontend
tkinter renders the GUI for this application. Main window displays the table of relevent records. The entirety of the application runs under Python with data requests being launched to the mySQL backend with SQL statements




# Backend
mySQL server hosts the tables/records and serves requests from the python application. 
If no additional configuration is desired, installing a server locally with the user `root` and password `root` will automatically connect with the default application. An export of the sample data is provided under databaseDump/. More info can be found under 'Data Import'

# Use
After installing the dependencies (tkinter, mysql connector), the application can be run simply with `python application.py`.
If the provided database was loaded, there are a few example tables. Use can be summarized in the four actions.
* Add
Creates a new record in the currently active table
* Remove
Deletes the selected record from the table (select a record by clicking on it in the table view)
* Update
Updates field values of the currently selected record. The dialogue box autofills the current information for easy editing.
* Pivot
Select a record that references another table of interest (ie alert's idhost), clicking pivot allows the user to select a foreign key that 
references a field in another table. This allows a user to pivot from one table to another based on a value in the selected record.
* Set Current Table
Text box that allows a user to specify a table to switch to. 

# Data Import


# REQUIREMENTS:
Python 3.* (Any Python 3)
tkinter library (pip install tk)
mysql-connector (pip install mysql-connector-python)