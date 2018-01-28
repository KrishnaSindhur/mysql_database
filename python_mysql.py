import mysql.connector

'''
Connecting to the local mysql server and creating table called
customer_account where it keeps the count of amount of money
of customers who have to give money to the shopkeepers
'''

db = mysql.connector.connect(host='localhost',database='mysql',user='root',password='xxx')
cursor = db.cursor()


'''
Here we insert the customers details to database who have to give money
and duplicate values for Name will not be allowed it should be unique
'''

def insert_customer():
    print "----------------------------------------------------"
    print "Enter the user dertails to the table"
    name = raw_input("Enter the customer Name: ")
    moneys = raw_input("Enter the AMOUNT: ")
    dates = raw_input("Enter the date in format YYYY-MM-DD: ")
    gender = raw_input("Enter the gender like 'M- Male' or 'F- 'Female'' or 'O- Others': ")
    sql_query = "INSERT INTO CUSTOMER_ACCOUNT(NAME, \
                AMOUNT, LEND_DATE, SEX) \
                VALUES (%s, %s, %s, %s)"
    query_data = (name, moneys, dates, gender)
    try:
        cursor.execute(sql_query, query_data)
        db.commit()
    except Error as e:
        print(e)
    else:
        print"Query successfull executed"
'''
Here we update customer value like either we will delete his name if he pays his full ammount or
we will update value of AMOUNT if he pays elements which is less than his full amount
'''

def update_customer_value():
    print "----------------------------------------------------"
    print "Enter the details to update the customer information"
    name = raw_input("Enter the customer name: ")
    amount = int(raw_input("Enter the amount: "))
    try:
        cursor.execute("SELECT * FROM CUSTOMER_ACCOUNT")
    except:
        print"error in table"

    result_set = cursor.fetchall()
    cost = 0
    flag = 0
    for row in result_set:
        money = int(row[1])
        if row[0] == name and money > amount:
            cost = money - amount
            cost = str(cost)
            sql_query = "UPDATE CUSTOMER_ACCOUNT \
                        SET AMOUNT= %s \
                        WHERE NAME= %s "
            query_data =(cost, name)
            cursor.execute(sql_query, query_data)
            db.commit()
            flag = 1
        elif row[0] == name and money == amount:
            query = "DELETE FROM CUSTOMER_ACCOUNT WHERE NAME = '%s' " %name
            cursor.execute(query)
            db.commit()
            flag = 1
    if flag == 0:
        print "Invalid values"
    else:
        print "Values updated"


'''
Here we create table name CUSTOMER_ACCOUNT if it already exists then delete that
old table and creates new one
'''

def create_table():
    print"Creating table CUSTOMER_ACCOUNT IN mysql database"
    cursor.execute("DROP TABLE IF EXISTS CUSTOMER_ACCOUNT")
    sql = """CREATE TABLE CUSTOMER_ACCOUNT (
            NAME  CHAR(20) NOT NULL,
            AMOUNT  CHAR(20),
            LEND_DATE DATE,
            SEX CHAR(1),
            PRIMARY KEY ( NAME ))"""
    cursor.execute(sql)

# this function displays table entries
def display_table():
    print "----------------------------------------------------"
    print "Present details in the table"
    cursor.execute("SELECT * FROM CUSTOMER_ACCOUNT")
    result_set = cursor.fetchall()
    for row in result_set:
        print row

# selected user information will be displayed
def select_user():
    print "----------------------------------------------------"
    print "Enter the user name to search deatils for particular user"
    name = raw_input("Enter the customer name: ")
    try:
        query = "SELECT * FROM CUSTOMER_ACCOUNT WHERE NAME = '%s' " %name
        cursor.execute(query)
        result_set = cursor.fetchall()
        for row in result_set:
            print row
            db.commit()
    except:
        print "Error: unable to fetch data"
    if len(result_set) == 0:
        print "No data for cutomer %s"%(name)


create_table()
insert_customer()
insert_customer()
update_customer_value()
display_table()
select_user()
db.close()
