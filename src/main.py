import json
import os
import inquirer
import getpass
import random
import string
import re
import smtplib 
import matplotlib.pyplot as plt
from tabulate import tabulate

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

DATA_DIR = "data"
ADMIN_FILE = os.path.join(DATA_DIR, "admin.json")
INSTRUCTORS_FILE = os.path.join(DATA_DIR, "instructors.json")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")

class System:
    @staticmethod
    def initialize_files():
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if not os.path.exists(ADMIN_FILE):
            with open(ADMIN_FILE, 'w') as f:
                json.dump({"username": "admin", "password": "admin"}, f)
        if not os.path.exists(INSTRUCTORS_FILE):
            with open(INSTRUCTORS_FILE, 'w') as f:
                json.dump({}, f)
        if not os.path.exists(STUDENTS_FILE):
            with open(STUDENTS_FILE, 'w') as f:
                json.dump({}, f)
        if not os.path.exists(COURSES_FILE):
            with open(COURSES_FILE, 'w') as f:
                json.dump({}, f)

    @staticmethod
    def load_json(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_json(file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def generate_id(data):
        return str(len(data) + 1)

    @staticmethod
    def generate_username(name, existing_usernames):
        base_username = name.lower().replace(" ", "_")
        chars = string.ascii_letters + string.digits
        suffix = ''.join(random.choice(chars) for _ in range(3))
        username = f"{base_username}@{suffix}"
        while username in existing_usernames:
            suffix = ''.join(random.choice(chars) for _ in range(3))
            username = f"{base_username}@{suffix}"
        return username

    @staticmethod
    def generate_password(length=8):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def authenticate_user(user_type):
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")

        if user_type == "Admin":
            admin_data = System.load_json(ADMIN_FILE)
            if admin_data["username"] == username and admin_data["password"] == password:
                return True
        elif user_type == "Instructor":
            instructors = System.load_json(INSTRUCTORS_FILE)
            for instructor in instructors.values():
                if instructor["username"] == username and instructor["password"] == password:
                    return True
        elif user_type == "Student":
            students = System.load_json(STUDENTS_FILE)
            for student in students.values():
                if student["username"] == username and student["password"] == password:
                    return True
        return False


class Admin:
    @staticmethod
    def menu():
        questions = [
            inquirer.List('choice',
                          message="Select from the menu",
                          choices=[
                              "Add Course",
                              "Add Instructor",
                              "Add Student",
                              "List Students",
                              "List Instructors",
                              "List Courses",
                              "Delete Student",
                              "Remove Instructor from Course",
                              "Delete Course",
                              "Exit"
                          ],
                          ),
        ]
        answers = inquirer.prompt(questions)
        return answers['choice']

    @staticmethod
    def send_account_info_to_email(receiver_email, message):

        try:
            sender_email = "test343py@gmail.com"

            supject = "Account information for login into Academy"

            text = f"subject : {supject}\n\n{message}"

            server = smtplib.SMTP("smtp.gmail.com",587)

            server.starttls()

            server.login(sender_email,"isyx xtlv erib guev")

            server.sendmail(sender_email,receiver_email,text)

        except Exception as e :
            print("Error: ",e)
        else:
            print(f"Account information sent successfully to {receiver_email}")

    @staticmethod
    def add_course():
        courses = System.load_json(COURSES_FILE)
        course_id = System.generate_id(courses)
        course_name = input("Enter course name: ")
        courses[course_id] = {"name": course_name, "instructors": []}
        System.save_json(COURSES_FILE, courses)
        print(f"Course '{course_name}' added with ID: {course_id}")

    @staticmethod
    def add_instructor_to_course(instructor_id, course_id):
        courses = System.load_json(COURSES_FILE)
        if course_id not in courses:
            raise Exception(f"Course ID '{course_id}' not found in the database")
        else:
            courses[course_id]["instructors"].append(instructor_id)
            System.save_json(COURSES_FILE, courses)
            instructors = System.load_json(INSTRUCTORS_FILE)
            instructor_name = instructors[instructor_id]["name"]
            print(f"Instructor: {instructor_name} added to course: {courses[course_id]['name']} successfully")
    @staticmethod
    def add_student_to_course(student_id, course_id):
        courses = System.load_json(COURSES_FILE)
        if course_id not in courses:
            raise Exception(f"Course ID '{course_id}' not found in the database")
        else:
            courses[course_id][student_id] = {"grade":None}
            System.save_json(COURSES_FILE, courses)
            students = System.load_json(STUDENTS_FILE)
            student_name = students[student_id]["name"]
            print(f"Student: {student_name} added to course: {courses[course_id]['name']} successfully")

    @staticmethod 
    def is_valid_email(email):

        personal_email_domains = [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", 
            "live.com", "aol.com", "icloud.com","luravel.com"
        ]
        email_regex = re.compile(
            r"^[a-zA-Z0-9_.+-]+@(" + "|".join(personal_email_domains) + r")$"
        )
        return re.match(email_regex, email) is not None

    @staticmethod
    def add_instructor():
        instructors = System.load_json(INSTRUCTORS_FILE)
        students = System.load_json(STUDENTS_FILE)
        existing_usernames = {user["username"] for user in instructors.values()}.union({user["username"] for user in students.values()})
        instructor_id = System.generate_id(instructors)
        instructor_name = input("Enter instructor name: ")
        instructor_email = input("Enter instructor email: ")
        while not Admin.is_valid_email(instructor_email):
            instructor_email = input("Please Enter valid instructor email: ")    
        instructor_username = System.generate_username(instructor_name, existing_usernames)
        instructor_password = System.generate_password()
        instructors[instructor_id] = {"name": instructor_name, "email": instructor_email, "username": instructor_username, "password": instructor_password}
        System.save_json(INSTRUCTORS_FILE, instructors)
        print(f"Instructor '{instructor_name}' added with ID: {instructor_id}")
        Admin.list_courses()
        course_id = input(f"Enter Course ID To assign To {instructor_name} : ")
        Admin.add_instructor_to_course(instructor_id, course_id) 
        message = f"instructor username : {instructor_username} \n instructor password : {instructor_password}"
        Admin.send_account_info_to_email(instructor_email,message)   
        # should account info send to email

    @staticmethod
    def add_student():
        instructors = System.load_json(INSTRUCTORS_FILE)
        students = System.load_json(STUDENTS_FILE)
        existing_usernames = {user["username"] for user in instructors.values()}.union({user["username"] for user in students.values()})
        student_id = System.generate_id(students)
        student_name = input("Enter student name: ")
        student_email = input("Enter student email: ")
        while not Admin.is_valid_email(student_email):
            student_email = input("Please Enter valid Student email: ")   
        student_username = System.generate_username(student_name, existing_usernames)
        student_password = System.generate_password()
        students[student_id] = {"name": student_name, "email": student_email, "username": student_username, "password": student_password}
        System.save_json(STUDENTS_FILE, students)
        print(f"Student '{student_name}' added with ID: {student_id}")
        Admin.list_courses()
        course_id = input(f"Enter Course ID To assign To {student_name} : ")
        Admin.add_student_to_course(student_id, course_id)
        message = f"student username : {student_username} \n student password : {student_password}"
        Admin.send_account_info_to_email(student_email,message)  
        # should account info send to email

    @staticmethod
    def list_students():
        students = System.load_json(STUDENTS_FILE)
        student_list = [[student_id, student_info['name'], student_info['email']] for student_id, student_info in students.items()]
        print(tabulate(student_list, headers=["Student ID", "Student Name", "Email"], tablefmt="grid"))

    @staticmethod
    def list_instructors():
        instructors = System.load_json(INSTRUCTORS_FILE)
        instructor_list = [[instructor_id, instructor_info['name'], instructor_info['email']] for instructor_id, instructor_info in instructors.items()]
        print(tabulate(instructor_list, headers=["Instructor ID", "Instructor Name", "Email"], tablefmt="grid"))

    @staticmethod
    def list_courses():
        courses = System.load_json(COURSES_FILE)
        course_list = [[course_id, course_info['name']] for course_id, course_info in courses.items()]
        print(tabulate(course_list, headers=["Course ID", "Course Name"], tablefmt="grid"))

    @staticmethod
    def delete_student():
        students = System.load_json(STUDENTS_FILE)
        student_id = input("Enter student ID to delete: ")
        if student_id in students:
            del students[student_id]
            System.save_json(STUDENTS_FILE, students)
            print("Student deleted successfully")
        else:
            print("Student not found")

    @staticmethod
    def remove_instructor_from_course():
        courses = System.load_json(COURSES_FILE)
        course_id = input("Enter course ID: ")
        instructor_id = input("Enter instructor ID to remove from course: ")
        if course_id in courses and instructor_id in courses[course_id]["instructors"]:
            courses[course_id]["instructors"].remove(instructor_id)
            System.save_json(COURSES_FILE, courses)
            print("Instructor removed from course successfully")
        else:
            print("Instructor not found in course")

    @staticmethod
    def delete_course():
        courses = System.load_json(COURSES_FILE)
        course_id = input("Enter course ID to delete: ")
        if course_id in courses:
            del courses[course_id]
            System.save_json(COURSES_FILE, courses)
            print("Course deleted successfully")
        else:
            print("Course not found")


class Instructor:
    @staticmethod
    def menu():
        questions = [
            inquirer.List('choice',
                          message="Select from the menu",
                          choices=[
                              "Assign Grade",
                              "View Grade Statistics",
                              "Exit"
                          ],
                          ),
        ]
        answers = inquirer.prompt(questions)
        return answers['choice']
    
    @staticmethod
    def list_courses():
        courses = System.load_json(COURSES_FILE)
        course_list = [[course_id, course_info['name']] for course_id, course_info in courses.items()]
        print(tabulate(course_list, headers=["Course ID", "Course Name"], tablefmt="grid"))

    @staticmethod
    def list_students():
        students = System.load_json(STUDENTS_FILE)
        student_list = [[student_id, student_info['name'], student_info['email']] for student_id, student_info in students.items()]
        print(tabulate(student_list, headers=["Student ID", "Student Name", "Email"], tablefmt="grid"))

    @staticmethod
    def assign_grade():
        courses = System.load_json(COURSES_FILE)
        students = System.load_json(STUDENTS_FILE)
        Instructor.list_courses()
        course_id = input("Enter course ID: ")
        if course_id not in courses:
            print("Course not found")
            return
        Instructor.list_students()
        student_id = input("Enter student ID: ")
        if student_id not in students:
            print("Student not found")
            return
        
        grade = input("Enter grade: ")
        courses[course_id][student_id]["grade"] = grade
        System.save_json(COURSES_FILE, courses)
        print(f"Grade {grade} assigned to student ID: {student_id} in course ID: {course_id}")

    @staticmethod
    def view_grade_statistics():
        courses = System.load_json(COURSES_FILE)
        Instructor.list_courses()
        course_id = input("Enter course ID: ")
        if course_id not in courses:
            print("Course not found")
            return

        course = courses[course_id]
        grade_list = [int(info["grade"]) for key, info in course.items() if key.isdigit()]

        if not grade_list:
            print("No grades found for this course")
            return

        average_grade = sum(grade_list) / len(grade_list)
        
        plt.figure(figsize=(10, 6))
        plt.hist(grade_list, bins=10, alpha=0.75, color='blue', edgecolor='black')
        plt.title(f'Grade Distribution for Course ID: {course_id}')
        plt.xlabel('Grades')
        plt.ylabel('Number of Students')
        plt.axvline(average_grade, color='red', linestyle='dashed', linewidth=1)
        min_ylim, max_ylim = plt.ylim()
        plt.text(average_grade*1.1, max_ylim*0.9, f'Average: {average_grade:.2f}')

        plt.show()

        print(f"Grade statistics for course ID: {course_id}")
        print(f"Average grade: {average_grade:.2f}")


class Student:
    @staticmethod
    def menu():
        questions = [
            inquirer.List('choice',
                          message="Select from the menu",
                          choices=[
                              "View My Grades",
                              "Exit"
                          ],
                          ),
        ]
        answers = inquirer.prompt(questions)
        return answers['choice']

    @staticmethod
    def view_my_grades(student_id): # edit for good output
        courses = System.load_json(COURSES_FILE)
        Instructor.list_courses()
        course_id = input("Enter course id: ")
        
        if course_id in courses and student_id in courses[course_id]:
            grade_list = [[course_id, courses[course_id]["name"], courses[course_id][student_id]["grade"]]]
            print(tabulate(grade_list, headers=["Course ID", "Course Name", "Grade"], tablefmt="grid"))
        else:
            print("No records found for the given course ID and student ID")


class Main:
    def run(self):
        System.initialize_files()
        while True:
            questions = [
                inquirer.List('choice',
                              message="Login as",
                              choices=[
                                  "Admin",
                                  "Instructor",
                                  "Student",
                                  "Exit"
                              ],
                              ),
            ]
            answers = inquirer.prompt(questions)
            choice = answers['choice']

            if choice in ['Admin', 'Instructor', 'Student']:
                if System.authenticate_user(choice):
                    print(f"{choice} authenticated successfully.")
                    if choice == 'Admin':
                        self.admin_flow()
                    elif choice == 'Instructor':
                        self.instructor_flow()
                    elif choice == 'Student':
                        self.student_flow()
                else:
                    print("Authentication failed. Please try again.")
            elif choice == 'Exit':
                break
            else:
                print("Invalid choice")

    def admin_flow(self):
        while True:
            admin_choice = Admin.menu()
            if admin_choice == "Add Course":
                Admin.add_course()
            elif admin_choice == "Add Instructor":
                Admin.add_instructor()
            elif admin_choice == "Add Student":
                Admin.add_student()
            elif admin_choice == "List Students":
                Admin.list_students()
            elif admin_choice == "List Instructors":
                Admin.list_instructors()
            elif admin_choice == "List Courses":
                Admin.list_courses()
            elif admin_choice == "Delete Student":
                Admin.delete_student()
            elif admin_choice == "Remove Instructor from Course":
                Admin.remove_instructor_from_course()
            elif admin_choice == "Delete Course":
                Admin.delete_course()
            elif admin_choice == "Exit":
                break
            input("Press Enter to Continue...")

    def instructor_flow(self):
        while True:
            instructor_choice = Instructor.menu()
            if instructor_choice == "Assign Grade":
                Instructor.assign_grade()
            elif instructor_choice == "View Grade Statistics":
                Instructor.view_grade_statistics()
            elif instructor_choice == "Exit":
                break
            input("Press Enter to Continue...")

    def student_flow(self):
        while True:
            student_choice = Student.menu()
            if student_choice == "View My Grades":
                student_id = input("Enter your student ID: ")
                Student.view_my_grades(student_id)
            elif student_choice == "Exit":
                break
            input("Press Enter to Continue...")


if __name__ == "__main__":
    Main().run()
