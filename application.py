from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from Database import Database

db = Database()
def populate_list(id: int = None):
    for i in tree_view.get_children():
        tree_view.delete(i)
    for row in db.fetch(table = currentTable, searchTerm=id if id else None, attribute='id' if id else None):
        tree_view.insert('', 'end', values=row)

currentTable = "alerts"
selected_item = None
createEntries = {}
createInputs = {}
createLabels = {}
createWindow = None
createFrame = None
def submitCreate():
    global createInputs, createEntries, createWindow, createFrame
    
    vals = {}
    for attribute in createEntries:
        print(createEntries[attribute].get())
        if createEntries[attribute].get() == "":
            print(attribute)
            print("Missing input")
            break
        vals[attribute] = createEntries[attribute].get()
    else:
        db.insert(table=currentTable, values=vals)
        clear_text()
        populate_list()


def create():
    global createWindow, createFrame
    createWindow = None
    createFrame = None
    createWindow = Tk()
    createWindow.title("Create Entry")
    createFrame = Frame(createWindow)
    createFrame.grid(row=0, column=0)
    columns = db.getColumns(currentTable)
    print(columns)
    columnNames = columns.keys()
    global createInputs, createEntries, createLabels
    createEntries = {}
    createInputs = {}
    createLabels = {}
    row = 1
    
    for attribute in columnNames:
        createInputs[attribute] = StringVar().set(columns[attribute])
        createLabels[attribute] = Label(
            createFrame, text=attribute, font=('bold', 12))
        createLabels[attribute].grid(row=row, column=1)
        createEntries[attribute] = Entry(createFrame, textvariable=createInputs[attribute])
        
        createEntries[attribute].grid(row=row, column=2)
        row+=1
    submitButton = Button(createFrame, text="Submit", command=submitCreate)
    submitButton.grid(row=row, column=2)
    row+=1
    return
    

updateEntries = {}
updateInputs = {}
updateLabels = {}
updateWindow = None
updateFrame = None
def submitUpdate():
    global updateInputs, updateEntries, updateWindow, updateFrame
    vals = {}
    for attribute in updateEntries:
        print(updateEntries[attribute].get())
        if updateEntries[attribute].get() == "":
            print(attribute)
            print("Missing input")
            break
        vals[attribute] = updateEntries[attribute].get()
    else:
        db.update(currentTable, vals['id'], values=vals)
        clear_text()
        populate_list()
def update():
    global updateWindow, updateFrame
    updateWindow = None
    updateFrame = None
    updateWindow = Tk()
    updateWindow.title("Update Entry")
    updateFrame = Frame(updateWindow)
    updateFrame.grid(row=0, column=0)
    columns = db.getColumns(currentTable)
    print(columns)
    columnNames = columns.keys()
    global updateInputs, updateEntries, updateLabels
    updateEntries = {}
    updateInputs = {}
    updateLabels = {}
    row = 1
    selectedItemIndex = 0
    for attribute in columnNames:
        updateInputs[attribute] = StringVar()
        
        updateLabels[attribute] = Label(
            updateFrame, text=attribute, font=('bold', 12))
        updateLabels[attribute].grid(row=row, column=1)
        updateEntries[attribute] = Entry(
            updateFrame, textvariable=updateInputs[attribute])
        if (selected_item):
            updateEntries[attribute].insert(END, selected_item[selectedItemIndex])
            selectedItemIndex += 1

        updateEntries[attribute].grid(row=row, column=2)
        row += 1
    submitButton = Button(updateFrame, text="Submit", command=submitUpdate)
    submitButton.grid(row=row, column=2)
    row += 1
    return


pivotRadios = {}
pivotLabels = {}
pivotWindow = None
pivotFrame = None
radioSelection = None
def pivotSubmit():
    global radioSelection, currentTable
    selection = radioSelection.get()
    pivotValue = selected_item[selection]
    if "id" not in selection:
        return
    pivotTable = selection[2:] + "s"
    print(selection, pivotValue, pivotTable)
    currentTable = pivotTable
    updateFrame(currentTable, id=pivotValue)
    pass
def pivot():
    global pivotWindow, pivotFrame
    pivotWindow = None
    pivotFrame = None
    pivotWindow = Tk()
    pivotWindow.title("Pivot Entry")
    pivotFrame = Frame(pivotWindow)
    pivotFrame.grid(row=0, column=0)
    columns = db.getColumns(currentTable)
    print(columns)
    columnNames = columns.keys()
    global pivotRadios, pivotLabels, radioSelection
    pivotRadios = {}
    pivotLabels = {}
    row = 0
    radioSelection = StringVar(pivotFrame)
    for attribute in columnNames:
            pivotRadios[attribute] = Radiobutton(pivotFrame, text=attribute, 
            variable=radioSelection, value=attribute)
            pivotRadios[attribute].grid(row=row, column=0, sticky=W)
            row+=1
    submitButton = Button(pivotFrame, text="Submit", command=pivotSubmit)
    submitButton.grid(row=row, column=0, sticky=W)

def select_record(event):
    try:
        global selected_item, currentTable
        selected_item = dict()
        index = tree_view.selection()[0]
        vals = tree_view.item(index)['values']
        i = 0
        for attribute in db.getColumns(currentTable):
            selected_item[attribute] = vals[i]
            i += 1
        
    except IndexError:
        pass


def remove():
    db.remove(currentTable, selected_item[0])
    clear_text()
    populate_list()




def clear_text():
    return
    shortDesc_entry.delete(0, END)
    alertID_entry.delete(0, END)
    host_entry.delete(0, END)
    flash_entry.delete(0, END)


def set_search_table():
    tableName = table_search.get()
    global currentTable
    currentTable = tableName
    updateFrame(tableName)


tree_view = None
frame_results = None
app = Tk()
frame_search = Frame(app)
frame_search.grid(row=0, column=0)
lbl_search = Label(frame_search, text="Set Search Table",
    font=('bold', 12), pady=20)
lbl_search.grid(row=0, column=0, sticky=W)
table_search = StringVar(value=currentTable)
table_search_entry = Entry(frame_search, textvariable=table_search)
table_search_entry.grid(row=0, column=1)
table_list_frame = Frame(app)
table_list_frame.grid(row=0, column=1)
table_list_header = Label(table_list_frame, text="TABLES:")
table_list_header.grid(row=0, column=0)
row = 1
for table in db.getTables():
    Label(table_list_frame, text=table).grid(row=row, column=0, sticky=W)
    row+=1


# ## FIELDS ##
# frame_fields = Frame(app)
# frame_fields.grid(row=1, column=0)
# # hostname
# alertID_text = StringVar()
# alertID_label = Label(frame_fields, text='Alert ID', font=('bold', 12))
# alertID_label.grid(row=0, column=0, sticky=E)
# alertID_entry = Entry(frame_fields, textvariable=alertID_text)
# alertID_entry.grid(row=0, column=1, sticky=W)
# # BRAND
# brand_text = StringVar()
# brand_label = Label(frame_fields, text='Brand', font=('bold', 12))
# brand_label.grid(row=0, column=2, sticky=E)
# shortDesc_entry = Entry(frame_fields, textvariable=brand_text)
# shortDesc_entry.grid(row=0, column=3, sticky=W)
# # RAM
# host_text = StringVar()
# ram_label = Label(frame_fields, text='RAM', font=('bold', 12))
# ram_label.grid(row=1, column=0, sticky=E)
# host_entry = Entry(frame_fields, textvariable=host_text)
# host_entry.grid(row=1, column=1, sticky=W)
# # FLASH
# flash_text = StringVar()
# flash_label = Label(frame_fields, text='Flash', font=('bold', 12), pady=20)
# flash_label.grid(row=1, column=2, sticky=E)
# flash_entry = Entry(frame_fields, textvariable=flash_text)
# flash_entry.grid(row=1, column=3, sticky=W)

## RESULTS ##

def resultsFrameBuild(columns=[]):
    frame_results = Frame(app)
    frame_results.grid(row=4, column=0, columnspan=4, rowspan=7, pady=20, padx=20)

    
    Hscrollbar = Scrollbar(frame_results, orient='horizontal')
    
    Hscrollbar.pack(side=BOTTOM, fill=X)
    tree_view = Treeview(frame_results, columns=columns, show="headings")
    for col in columns:
        tree_view.column(col, width=100)
        tree_view.heading(col, text=col)
    tree_view.bind('<<TreeviewSelect>>', select_record)
    tree_view.pack(side=LEFT, fill="y")
    tree_view.config(xscrollcommand=Hscrollbar.set)
    Hscrollbar.configure(command=tree_view.xview)
    scrollbar = Scrollbar(frame_results, orient='vertical')
    scrollbar.configure(command=tree_view.yview)
    scrollbar.pack(side=RIGHT, fill="y")
    tree_view.config(yscrollcommand=scrollbar.set)

    
    return tree_view, frame_results

def updateFrame(table, id:int = None):
    global tree_view
    global frame_results
    if(tree_view):
        tree_view.grid_forget()
        tree_view.destroy()
        frame_results.grid_forget()
        frame_results.destroy()
    tableColumns = db.getColumns(table)
    print(tableColumns)
    tree_view, frame_results = resultsFrameBuild(columns=list(tableColumns.keys()))
    populate_list(id)
    return tree_view, frame_results


tree_view, frame_results = updateFrame(currentTable)

## BUTTONS ##
frame_btns = Frame(app)
frame_btns.grid(row=3, column=0)

add_btn = Button(frame_btns, text='Add', width=12, command=create)
add_btn.grid(row=0, column=0, pady=20)

remove_btn = Button(frame_btns, text='Remove',
                    width=12, command=remove)
remove_btn.grid(row=0, column=1)

update_btn = Button(frame_btns, text='Update',
                    width=12, command=update)
update_btn.grid(row=0, column=2)

clear_btn = Button(frame_btns, text='Pivot',
                   width=12, command=pivot)
clear_btn.grid(row=0, column=3)

search_btn = Button(frame_search, text='Set',
                    width=12, command=set_search_table)
search_btn.grid(row=0, column=2)


##TITLE / GEOMETRY##
app.title("SIEM Manager")
app.geometry('700x550')


app.mainloop()
