# CS6400
CS6400 DB Class Project. SIEM Mock Software

# REQUIREMENTS:
Python 3.* (Any Python 3)
tkinter library (pip install tk)
mysql-connector (pip install mysql-connector-python)
mySQL Server 8.*
mySQL Workbench 8.*

# mySQL Server Install
Following default settings, create a user 'root' with password 'root'. This can be changed, but keep in mind that the Database.py file must be updated to reflect the new credentials.

# mySQL Workbench Install

# Data Import
After the mySQL server and workbench are installed, the sample data can be imported. Provided at /databaseDump/, the tables can be imported through mySQL workbench (provided it is already connected to the mySQL Server). Under Server->Data Import, you will select the .sql files from the previously mentioned directory, and the data will then be populated.

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

# Frontend
tkinter renders the GUI for this application. Main window displays the table of relevent records. The entirety of the application runs under Python with data requests being launched to the mySQL backend with SQL statements


# Backend
mySQL server hosts the tables/records and serves requests from the python application. 
If no additional configuration is desired, installing a server locally with the user `root` and password `root` will automatically connect with the default application. An export of the sample data is provided under databaseDump/. More info can be found under 'Data Import'

# References
I referenced this resource detailing how to make a tkinter GUI (https://www.python4networkengineers.com/posts/python-intermediate/create_a_tkinter_gui_with_sqlite_backend/). I modified it to only show GUI elements relevent to my use case, broadened the scope of the interface to view multiple tables, and expanded the item entry to a separate window.
I wrote the following files:
* application.py (heavily modified from tkinter guide)
* Database.py (lightly modified from tkinter guide)
* dbConnection.py (original work, creates sample data)




