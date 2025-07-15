
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from db_connection import connect_db


import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from db_connection import connect_db

def insert_student():
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    if not name or not email:
        messagebox.showerror("Missing Information", "Please enter both the student's name and email.")
        return
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO cmps_schema.student (sname, semail) VALUES (%s, %s);", (name, email))
            conn.commit()
            messagebox.showinfo("Success", "Student Added!")
            entry_name.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            view_students()
        except psycopg2.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cur.close()
            conn.close()

def view_students():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT sno, sname, semail FROM cmps_schema.student;")
        records = cur.fetchall()
        student_list.delete(0, tk.END)
        for record in records:
            student_list.insert(tk.END, f"ID: {record[0]} | {record[1]} | {record[2]}")
        cur.close()
        conn.close()

def delete_student():
    selected = student_list.curselection()
    if not selected:
        messagebox.showerror("Selection Required", "Please select a student from the list to delete.")
        return
    student_info = student_list.get(selected[0])
    sno = student_info.split("|")[0].split(":")[1].strip()
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM cmps_schema.student WHERE sno = %s;", (sno,))
        conn.commit()
        messagebox.showinfo("Success", "Student Deleted!")
        view_students()
        cur.close()
        conn.close()

def insert_exam():
    excode = entry_excode.get().strip()
    extitle = entry_extitle.get().strip()
    exlocation = entry_exlocation.get().strip()
    exdate = entry_exdate.get().strip()
    extime = entry_extime.get().strip()
    if not all([excode, extitle, exlocation, exdate, extime]):
        messagebox.showerror("Missing Information", "Please enter all exam details (code, title, location, date, time).")
        return
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO cmps_schema.exam (excode, extitle, exlocation, exdate, extime) VALUES (%s, %s, %s, %s, %s);", (excode, extitle, exlocation, exdate, extime))
        conn.commit()
        messagebox.showinfo("Success", "Exam Added!")
        view_exams()
        cur.close()
        conn.close()

def view_exams():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT excode, extitle, exlocation, exdate, extime FROM cmps_schema.exam;")
        records = cur.fetchall()
        exam_list.delete(0, tk.END)
        for record in records:
            exam_list.insert(tk.END, f"Code: {record[0]} | {record[1]} | {record[2]} | {record[3]} | {record[4]}")
        cur.close()
        conn.close()

def delete_exam():
    selected = exam_list.curselection()
    if not selected:
        messagebox.showerror("Selection Required", "Please select an exam from the list to delete.")
        return
    exam_info = exam_list.get(selected[0])
    excode = exam_info.split("|")[0].split(":")[1].strip()
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM cmps_schema.exam WHERE excode = %s;", (excode,))
            if cur.rowcount == 0:
                messagebox.showerror("Error", "Cannot delete exam if students are scheduled to sit.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Exam Deleted!")
                view_exams()
        except psycopg2.errors.ForeignKeyViolation:
            messagebox.showerror("Error", "Cannot delete exam if students are scheduled to sit.")
            conn.rollback()
        except psycopg2.Error as e:
            messagebox.showerror("Database Error", str(e))
            conn.rollback()
        finally:
            cur.close()
            conn.close()

def register_exam():
    sno = entry_sno.get().strip()
    excode = entry_excode_reg.get().strip()
    if not sno or not excode:
        messagebox.showerror("Missing Information", "Please enter both Student ID and Exam Code to register.")
        return
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO cmps_schema.entry (sno, excode) VALUES (%s, %s);", (sno, excode))
            conn.commit()
            messagebox.showinfo("Success", "Student Registered for Exam!")
            view_exam_registrations()
        except psycopg2.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cur.close()
            conn.close()

def view_exam_registrations():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT e.eno, s.sname, ex.extitle, ex.exdate FROM cmps_schema.entry e JOIN cmps_schema.student s ON e.sno = s.sno JOIN cmps_schema.exam ex ON e.excode = ex.excode ORDER BY ex.exdate;")
        records = cur.fetchall()
        reg_list.delete(0, tk.END)
        for record in records:
            reg_list.insert(tk.END, f"Entry ID: {record[0]} | {record[1]} | {record[2]} | {record[3]}")
        cur.close()
        conn.close()

def update_grade():
    eno = entry_eno.get().strip()
    grade = entry_grade.get().strip()
    if not eno or not grade:
        messagebox.showerror("Missing Information", "Please enter both Entry ID and Grade to update the record.")
        return
    try:
        grade_val = float(grade)
        if not (0 <= grade_val <= 100):
            raise ValueError("Invalid grade range")
    except ValueError:
        messagebox.showerror("Invalid Grade", "Grade must be a number between 0 and 100.")
        return
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("UPDATE cmps_schema.entry SET egrade = %s WHERE eno = %s;", (grade, eno))
        conn.commit()
        messagebox.showinfo("Success", "Grade Updated!")
        cur.close()
        conn.close()

def view_results():
    exam_filter = entry_examcode_result.get().strip()
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        if exam_filter:
            cur.execute("""
                SELECT ex.excode, ex.extitle, s.sname,
                    CASE WHEN e.egrade >= 70 THEN 'Distinction'
                         WHEN e.egrade >= 50 THEN 'Pass'
                         WHEN e.egrade < 50 THEN 'Fail'
                         ELSE 'Not Taken'
                    END AS result
                FROM cmps_schema.entry e
                JOIN cmps_schema.student s ON e.sno = s.sno
                JOIN cmps_schema.exam ex ON e.excode = ex.excode
                WHERE ex.excode = %s
                ORDER BY s.sname;
            """, (exam_filter,))
        else:
            cur.execute("""
                SELECT ex.excode, ex.extitle, s.sname,
                    CASE WHEN e.egrade >= 70 THEN 'Distinction'
                         WHEN e.egrade >= 50 THEN 'Pass'
                         WHEN e.egrade < 50 THEN 'Fail'
                         ELSE 'Not Taken'
                    END AS result
                FROM cmps_schema.entry e
                JOIN cmps_schema.student s ON e.sno = s.sno
                JOIN cmps_schema.exam ex ON e.excode = ex.excode
                ORDER BY ex.excode, s.sname;
            """)
        records = cur.fetchall()
        results_list.delete(0, tk.END)
        for record in records:
            results_list.insert(tk.END, f"{record[0]} | {record[1]} | {record[2]} | {record[3]}")
        cur.close()
        conn.close()




def view_timetable():
    sno = entry_timetable_sno.get().strip()
    sname = entry_timetable_sname.get().strip()

    if not sno or not sname:
        messagebox.showerror("Missing Information", "Please enter both Student ID and Student Name to view timetable.")
        return

    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT ex.exlocation, ex.excode, ex.extitle, ex.exdate, ex.extime
            FROM cmps_schema.entry e
            JOIN cmps_schema.student s ON e.sno = s.sno
            JOIN cmps_schema.exam ex ON e.excode = ex.excode
            WHERE s.sno = %s
            ORDER BY ex.exdate, ex.extime;
        """, (sno,))
        records = cur.fetchall()
        timetable_list.delete(0, tk.END)
        if records:
            timetable_list.insert(tk.END, f"Exams for {sname}:")
            for record in records:
                timetable_list.insert(tk.END, f"{record[0]} | {record[1]} | {record[2]} | {record[3]} | {record[4]}")
        else:
            timetable_list.insert(tk.END, "You have no upcoming exams.")
        cur.close()
        conn.close()


root = tk.Tk()
root.title("University Management System")
root.geometry("900x1200")

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Student Management
student_frame = ttk.LabelFrame(scrollable_frame, text="Student Management", padding=(10, 10))
student_frame.pack(padx=20, pady=10, fill="both", expand=True)

ttk.Label(student_frame, text="Name").pack(anchor="w")
entry_name = ttk.Entry(student_frame)
entry_name.pack(fill="x")

ttk.Label(student_frame, text="Email").pack(anchor="w")
entry_email = ttk.Entry(student_frame)
entry_email.pack(fill="x")

ttk.Button(student_frame, text="Add Student", command=insert_student).pack(pady=5)
ttk.Button(student_frame, text="View Students", command=view_students).pack(pady=5)
ttk.Button(student_frame, text="Delete Student", command=delete_student).pack(pady=5)

student_list = tk.Listbox(student_frame, width=70)
student_list.pack()

# Exam Management
exam_frame = ttk.LabelFrame(scrollable_frame, text="Exam Management", padding=(10, 10))
exam_frame.pack(padx=20, pady=10, fill="both", expand=True)

ttk.Label(exam_frame, text="Exam Code").pack(anchor="w")
entry_excode = ttk.Entry(exam_frame)
entry_excode.pack(fill="x")

ttk.Label(exam_frame, text="Exam Title").pack(anchor="w")
entry_extitle = ttk.Entry(exam_frame)
entry_extitle.pack(fill="x")

ttk.Label(exam_frame, text="Location").pack(anchor="w")
entry_exlocation = ttk.Entry(exam_frame)
entry_exlocation.pack(fill="x")

ttk.Label(exam_frame, text="Date (YYYY-MM-DD)").pack(anchor="w")
entry_exdate = ttk.Entry(exam_frame)
entry_exdate.pack(fill="x")

ttk.Label(exam_frame, text="Time (HH:MM)").pack(anchor="w")
entry_extime = ttk.Entry(exam_frame)
entry_extime.pack(fill="x")

ttk.Button(exam_frame, text="Add Exam", command=insert_exam).pack(pady=5)
ttk.Button(exam_frame, text="View Exams", command=view_exams).pack(pady=5)
ttk.Button(exam_frame, text="Delete Exam", command=delete_exam).pack(pady=5)

exam_list = tk.Listbox(exam_frame, width=70)
exam_list.pack()

# Exam Registration
reg_frame = ttk.LabelFrame(scrollable_frame, text="Exam Registration", padding=(10, 10))
reg_frame.pack(padx=20, pady=10, fill="both", expand=True)

ttk.Label(reg_frame, text="Student ID").pack(anchor="w")
entry_sno = ttk.Entry(reg_frame)
entry_sno.pack(fill="x")

ttk.Label(reg_frame, text="Exam Code").pack(anchor="w")
entry_excode_reg = ttk.Entry(reg_frame)
entry_excode_reg.pack(fill="x")

ttk.Button(reg_frame, text="Register Student for Exam", command=register_exam).pack(pady=5)
ttk.Button(reg_frame, text="View Registrations", command=view_exam_registrations).pack(pady=5)

reg_list = tk.Listbox(reg_frame, width=70)
reg_list.pack()

# Grade Management
grade_frame = ttk.LabelFrame(scrollable_frame, text="Grade Management", padding=(10, 10))
grade_frame.pack(padx=20, pady=10, fill="both", expand=True)

ttk.Label(grade_frame, text="Entry ID").pack(anchor="w")
entry_eno = ttk.Entry(grade_frame)
entry_eno.pack(fill="x")

ttk.Label(grade_frame, text="Grade").pack(anchor="w")
entry_grade = ttk.Entry(grade_frame)
entry_grade.pack(fill="x")

ttk.Button(grade_frame, text="Update Grade", command=update_grade).pack(pady=5)

# Results Viewer
results_frame = ttk.LabelFrame(scrollable_frame, text="Results Viewer", padding=(10, 10))
results_frame.pack(padx=20, pady=10, fill="both", expand=True)

ttk.Label(results_frame, text="Filter by Exam Code (optional)").pack(anchor="w")
entry_examcode_result = ttk.Entry(results_frame)
entry_examcode_result.pack(fill="x")

ttk.Button(results_frame, text="View Results", command=view_results).pack(pady=5)

results_list = tk.Listbox(results_frame, width=70)
results_list.pack()


# Timetable Viewer
timetable_frame = ttk.LabelFrame(scrollable_frame, text="Student Exam Timetable Viewer", padding=(10, 10))
timetable_frame.pack(padx=20, pady=10, fill="both", expand=True)

ttk.Label(timetable_frame, text="Student ID").pack(anchor="w")
entry_timetable_sno = ttk.Entry(timetable_frame)
entry_timetable_sno.pack(fill="x")

ttk.Label(timetable_frame, text="Student Name").pack(anchor="w")
entry_timetable_sname = ttk.Entry(timetable_frame)
entry_timetable_sname.pack(fill="x")

ttk.Button(timetable_frame, text="View Timetable", command=view_timetable).pack(pady=5)

timetable_list = tk.Listbox(timetable_frame, width=70)
timetable_list.pack()

root.mainloop()
