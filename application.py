from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from Database import Database

db = Database()
def populate_list(hostname=''):
    for i in tree_view.get_children():
        tree_view.delete(i)
    hostname = "%"+hostname+"%"
    for row in db.fetch(table = "hosts", attribute="hostname", searchTerm=hostname):
        tree_view.insert('', 'end', values=row)


def populate_list2(query='select * from routers'):
    for i in tree_view.get_children():
        tree_view.delete(i)
    for row in db.query(query):
        tree_view.insert('', 'end', values=row)


def add_alert():
    if brand_text.get() == '' or alertID_text.get() == '' or host_text.get() == '' or flash_text.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    db.insert(alertID_text.get(), brand_text.get(),
              host_text.get(), flash_text.get())
    clear_text()
    populate_list()


def select_record(event):
    try:
        global selected_item
        index = tree_view.selection()[0]
        selected_item = tree_view.item(index)['values']
        alertID_entry.delete(0, END)
        alertID_entry.insert(END, selected_item[1])
        shortDesc_entry.delete(0, END)
        shortDesc_entry.insert(END, selected_item[2])
        host_entry.delete(0, END)
        host_entry.insert(END, selected_item[3])
        flash_entry.delete(0, END)
        flash_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_alert():
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_alert():
    db.update(selected_item[0], alertID_text.get(), brand_text.get(),
              host_text.get(), flash_text.get())
    populate_list()


def clear_text():
    shortDesc_entry.delete(0, END)
    alertID_entry.delete(0, END)
    host_entry.delete(0, END)
    flash_entry.delete(0, END)


def search_table():
    tableName = table_search.get()
    updateFrame(tableName)


def execute_query():
    query = query_search.get()
    populate_list2(query)


app = Tk()
frame_search = Frame(app)
frame_search.grid(row=0, column=0)
lbl_search = Label(frame_search, text="Search table",
    font=('bold', 12), pady=20)
lbl_search.grid(row=0, column=0, sticky=W)
table_search = StringVar()
table_search_entry = Entry(frame_search, textvariable=table_search)
table_search_entry.grid(row=0, column=1)
lbl_search = Label(frame_search, text="Search by Query",
    font=('bold', 12), pady=20)
lbl_search.grid(row=1, column=0, sticky=W)
query_search = StringVar()
query_search.set("Select * from alerts")
query_search_entry = Entry(frame_search, textvariable=query_search, width=40)
query_search_entry.grid(row=1, column=1)

## FIELDS ##
frame_fields = Frame(app)
frame_fields.grid(row=1, column=0)
# hostname
alertID_text = StringVar()
alertID_label = Label(frame_fields, text='Alert ID', font=('bold', 12))
alertID_label.grid(row=0, column=0, sticky=E)
alertID_entry = Entry(frame_fields, textvariable=alertID_text)
alertID_entry.grid(row=0, column=1, sticky=W)
# BRAND
brand_text = StringVar()
brand_label = Label(frame_fields, text='Brand', font=('bold', 12))
brand_label.grid(row=0, column=2, sticky=E)
shortDesc_entry = Entry(frame_fields, textvariable=brand_text)
shortDesc_entry.grid(row=0, column=3, sticky=W)
# RAM
host_text = StringVar()
ram_label = Label(frame_fields, text='RAM', font=('bold', 12))
ram_label.grid(row=1, column=0, sticky=E)
host_entry = Entry(frame_fields, textvariable=host_text)
host_entry.grid(row=1, column=1, sticky=W)
# FLASH
flash_text = StringVar()
flash_label = Label(frame_fields, text='Flash', font=('bold', 12), pady=20)
flash_label.grid(row=1, column=2, sticky=E)
flash_entry = Entry(frame_fields, textvariable=flash_text)
flash_entry.grid(row=1, column=3, sticky=W)

## RESULTS ##
tree_view = None
frame_results = None
def resultsFrameBuild(columns=[]):
    frame_results = Frame(app)
    frame_results.grid(row=4, column=0, columnspan=4, rowspan=7, pady=20, padx=20)

    tree_view = Treeview(frame_results, columns=columns, show="headings")
    for col in columns[:]:
        tree_view.column(col, width=100)
        tree_view.heading(col, text=col)
    tree_view.bind('<<TreeviewSelect>>', select_record)
    tree_view.pack(side=LEFT, fill="y")
    Hscrollbar = Scrollbar(frame_results, orient='horizontal')
    Hscrollbar.configure(command=tree_view.xview)
    Hscrollbar.pack(side=BOTTOM, fill="x")
    tree_view.config(xscrollcommand=Hscrollbar.set)
    scrollbar = Scrollbar(frame_results, orient='vertical')
    scrollbar.configure(command=tree_view.yview)
    scrollbar.pack(side=RIGHT, fill="y")
    tree_view.config(yscrollcommand=scrollbar.set)

    
    return tree_view, frame_results

def updateFrame(table):
    global tree_view
    global frame_results
    if(tree_view):
        tree_view.grid_forget()
        tree_view.destroy()
        frame_results.grid_forget()
        frame_results.destroy()
    tableColumns = db.getColumns(table)
    print(tableColumns)
    tree_view, frame_results = resultsFrameBuild(columns=tableColumns)
    return tree_view, frame_results


tree_view, frame_results = updateFrame("alerts")

## BUTTONS ##
frame_btns = Frame(app)
frame_btns.grid(row=3, column=0)

add_btn = Button(frame_btns, text='Add Alert', width=12, command=add_alert)
add_btn.grid(row=0, column=0, pady=20)

remove_btn = Button(frame_btns, text='Remove Alert',
                    width=12, command=remove_alert)
remove_btn.grid(row=0, column=1)

update_btn = Button(frame_btns, text='Update Alert',
                    width=12, command=update_alert)
update_btn.grid(row=0, column=2)

clear_btn = Button(frame_btns, text='Clear Input',
                   width=12, command=clear_text)
clear_btn.grid(row=0, column=3)

search_btn = Button(frame_search, text='Search',
                    width=12, command=search_table)
search_btn.grid(row=0, column=2)

search_query_btn = Button(frame_search, text='Search Query',
                          width=12, command=execute_query)
search_query_btn.grid(row=1, column=2)

##TITLE / GEOMETRY##
app.title("SIEM Manager")
app.geometry('700x550')


app.mainloop()
