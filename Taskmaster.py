import tkinter as tk
import sqlite3

#set variables for GUI
root = tk.Tk()
root.title("Taskmaster")
top_left_x = root.winfo_screenwidth()-420
top_left_y = root.winfo_screenheight()*0.2
root.geometry('%dx%d+%d+%d' % (400, 500, top_left_x, top_left_y))
bgcolor="#52965d"
root.config(bg=bgcolor)

#creating frames in grid to layout GUI
first_section = tk.Frame(root, bg=bgcolor)
first_section. grid(row=0,column=0, padx=2,pady=2)

description_section = tk.Frame(root, bg=bgcolor)
description_section. grid(row=1,column=0, padx=2,pady=2)

third_section = tk.Frame(root, bg=bgcolor)
third_section. grid(row=2,column=0, padx=2,pady=2)

button_section = tk.Frame(root, bg=bgcolor)
button_section. grid(row=3,column=0, padx=2,pady=2)

fifth_section = tk.Frame(root, bg=bgcolor)
fifth_section. grid(row=4,column=0, padx=2,pady=2)

taskgraph_section = tk.Frame(root, width=380, height=300, bg='white')
taskgraph_section.grid(row=5, column=0, padx=2,pady=2)  # Grid placement for the taskgraph frame

#initialize starting screen widgets
def start_screen():
    global task_id_input, title_input, description_input, length_input, date_input  # Declare the variables as global

    #task id title
    tk.Label(
        first_section,
        text="Task ID",
        width=7,
        bg=bgcolor,
        fg="black",
        font=("TkHeadingFont",12)). grid(row=0,column=0, padx=2,pady=2)

    #task id input box
    task_id_input = tk.Entry(
        first_section,
        width=5,
        fg="black",
        font=("TkHeadingFont",12))
    task_id_input. grid(row=0,column=1, padx=2,pady=2)

    #title title
    tk.Label(
        first_section,
        width=7,
        text="Title",
        bg=bgcolor,
        fg="black",
        font=("TkHeadingFont",12)). grid(row=0,column=2, padx=2,pady=2)
    
    #title input
    title_input = tk.Entry(
        first_section,
        width=20,
        fg="black",
        font=("TkHeadingFont",12))
    title_input. grid(row=0,column=3, padx=2,pady=2)
    
    #description title
    tk.Label(
        description_section,
        width=10,
        text="Description",
        bg=bgcolor,
        fg="black",
        font=("TkHeadingFont",12)). grid(row=0,column=0, padx=2,pady=2)
    
    #description box
    description_input = tk.Entry(
        description_section,
        width=31,
        fg="black",
        font=("TkHeadingFont",12))
    description_input. grid(row=0,column=1, padx=2,pady=2)
    
    #length title
    tk.Label(
        third_section,
        width=7,
        text="Length",
        bg=bgcolor,
        fg="black",
        font=("TkHeadingFont",12)). grid(row=0,column=0, padx=2,pady=2)
    
    #length input box
    length_input = tk.Entry(
        third_section,
        width=5,
        fg="black",
        font=("TkHeadingFont",12))
    length_input. grid(row=0,column=1, padx=2,pady=2)
    
    #date title
    tk.Label(
        third_section,
        width=7,
        text="Deadline",
        bg=bgcolor,
        fg="black",
        font=("TkHeadingFont",12)). grid(row=0,column=2, padx=2,pady=2)
    
    #date input box
    date_input = tk.Entry(
        third_section,
        width=20,
        fg="black",
        font=("TkHeadingFont",12))
    date_input. grid(row=0,column=3, padx=2,pady=2)

    #add task button
    add_button = tk.Button(
        button_section,
        text="ADD TASK",
        font=("TkHeadingFont", 12),
        bg="#16865d",
        fg='black',
        cursor='hand2',
        activebackground='#321163',
        activeforeground='black')
    add_button. grid(row=0,column=0, padx=4,pady=2)
    add_button.bind('<Button-1>', add_entry)

        #update task button
    update_button = tk.Button(
        button_section,
        text="UPDATE TASK",
        font=("TkHeadingFont", 12),
        bg="#16865d",
        fg='black',
        cursor='hand2',
        activebackground='#321163',
        activeforeground='black')
    update_button. grid(row=0,column=1, padx=4,pady=2)
    update_button.bind('<Button-1>', update_entry)
    
        #delete task button
    delete_button = tk.Button(
        button_section,
        text="DELETE TASK",
        font=("TkHeadingFont", 12),
        bg="#16865d",
        fg='black',
        cursor='hand2',
        activebackground='#321163',
        activeforeground='black')
    delete_button. grid(row=0,column=2, padx=4,pady=2)
    delete_button.bind('<Button-1>', delete_entry)

    #title for table display
    tk.Label(
        fifth_section,
        text="Current Tasks:",
        bg=bgcolor,
        fg="black",
        font=("TkHeadingFont",12)). grid(row=0,column=0, padx=2,pady=2)

#create table and fill if blank
def initialize_table():
    #connect to database
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
        #create table if does not exist, insert example
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks
        (task_id INTEGER PRIMARY KEY, title text NON NULL, description text, length int, due_date text);''')
    try:
        cur.execute('''INSERT INTO tasks(task_id, title, description, length, due_date)
            VALUES (1, 'Example Task','add tasks to test!',15,'2023-07-18');''')
    except:
        pass
    conn.commit()
    conn.close()

#fucntion to display table
def fetch_table():
    #connect to database
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()

    #select and print table values
    tentasks = conn.execute('''SELECT * FROM tasks ORDER BY CASE when due_date is '' then 1 else 0 end, due_date, task_id LIMIT 0,10;''')
    i = 0  # row value inside the loop
    for student in tentasks:
        for j in range(len(student)):
            if j==0 or j==3:
                column_width=3
            elif j==1 or j==4:
                column_width = 10
            else:
                column_width=22
            e = tk.Label(taskgraph_section, width=column_width, fg='#023020', text=student[j], anchor='w')
            e.grid(row=i, column=j, padx=2,pady=2)  # Grid placement for the labels in taskgraph frame
        i = i + 1
    conn.commit()
    conn.close()

#inserts row into database
def add_entry(event):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    task_id = task_id_input.get()
    title = title_input.get()
    description = description_input.get()
    length = length_input.get()
    date = date_input.get()
    if len(title) > 0:
        if task_id == '':
            cur.execute(f'''INSERT INTO tasks(title, description, length, due_date)
                VALUES ('{title}', '{description}', '{length}', '{date}');''')
        else:
            cur.execute(f'''INSERT INTO tasks(task_id, title, description, length, due_date)
                VALUES ({task_id}, '{title}', '{description}', {length}, '{date}');''')
    else:
        print('enter a title')
    conn.commit()
    conn.close()
    fetch_table()

#updates row in database
def update_entry(event):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    task_id = task_id_input.get()
    title = title_input.get()
    description = description_input.get()
    length = length_input.get()
    date = date_input.get()
    if len(task_id) > 0:
        if len(title) > 0:
            cur.execute(f'''UPDATE tasks
                SET title = '{title}'
                WHERE task_id = {task_id};''')
        if len(description) > 0:
            cur.execute(f'''UPDATE tasks
                SET description = '{description}'
                WHERE task_id = {task_id};''')
        if len(length) > 0:
            cur.execute(f'''UPDATE tasks
                SET length = '{length}'
                WHERE task_id = {task_id};''')
        if len(date) > 0:
            cur.execute(f'''UPDATE tasks
                SET due date = '{date}'
                WHERE task_id = {task_id};''')
    else:
        print('enter an id')
    conn.commit()
    conn.close()
    fetch_table()

#deletes row in database
def delete_entry(event):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    task_id = task_id_input.get()
    cur.execute(f'''DELETE FROM tasks WHERE task_id = {task_id};''')
    conn.commit()
    conn.close()
    for label in taskgraph_section.winfo_children():
        label.destroy()
    fetch_table()


#run hte program  
start_screen()
initialize_table()
fetch_table()
root.mainloop()

