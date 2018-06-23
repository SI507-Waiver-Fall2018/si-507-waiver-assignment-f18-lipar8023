# Name: Linya Li
# Uniq Id:linyal

import sqlite3 as sqlite
import sys


con = sqlite.connect('Northwind_small.sqlite')
cur = con.cursor()

#----- Show all customer names from the Customer table
def print_cust_names():
    q1 = '''
    SELECT Id, CompanyName FROM Customer
    '''
    result1 = cur.execute(q1)
    print('ID       Customer Name')
    for row in result1:
        print(*row, sep='    ')

#----- Show all employee names from the Employee table
def print_emp_names():
    q2 = '''
    SELECT Id, FirstName, LastName FROM Employee
    '''
    result2 = cur.execute(q2)
    print('ID     Employee Name')
    for row in result2:
        print(row[0],'    ',row[1],row[2])


#----- Show order dates from a certain customer
def print_date_cust(cust_name):
    q3 = '''
    SELECT OrderDate FROM [Order]
    WHERE CustomerId = ?
    '''
    params = (cust_name,)
    result3 = cur.execute(q3,params).fetchall()
    print('Order Dates')
    for row in result3:
        print(*row, sep='    ')

#----- Show order dates from a certain employee
def print_date_emp(emp_name):
    q4 = '''
    SELECT OrderDate
    FROM [Order] As O
    JOIN Employee As E
    	ON O.EmployeeId = E.Id
    WHERE E.LastName = ?
    '''
    params = (emp_name,)
    result4 = cur.execute(q4, params).fetchall()
    print('Order Dates')
    for row in result4:
        print(*row, sep=', ')

command = sys.argv[1]
if command == 'customers':
    print_cust_names()
elif command == 'employees':
    print_emp_names()
elif command == 'orders':
    sec_command = sys.argv[2][0]
    if sec_command == 'c':
        cust_name = sys.argv[2][5:]
        print_date_cust(cust_name)
    elif sec_command == 'e':
        emp_name = sys.argv[2][4:]
        print_date_emp(emp_name)
else:
    print('Invalid Command.')
