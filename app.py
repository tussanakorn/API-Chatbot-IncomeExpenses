## google sheet
import geopy.distance as ps
import pandas as pd
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Income-Expenses").sheet1
sheet2 = client.open("Income-Expenses").get_worksheet(1)


# data = sheet.get_all_records()
# listdata = pd.DataFrame(data)
# employee = listdata['Customer_ID']
# print(employee)


### web service
from flask import Flask , jsonify, request
app = Flask(__name__)

def loadCustomerSheet():
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    return listdata

def ShowAllExpense(customer_id):
    data = sheet.get_all_records()
    listdata1 = pd.DataFrame(data)
    customer = listdata1[ listdata1['customer_id'] == customer_id ]
    check_expense = customer['expense']
    expense_list = ", ".join(str(x) for x in check_expense)

    if expense_list == "":
        return "ยังไม่มีบันทึก"
    else:
        return expense_list


def searchExpense(customer_id):
    data = sheet.get_all_records()
    listdata1 = pd.DataFrame(data)
    customer = listdata1[ listdata1['customer_id'] == customer_id ]
    check_expense = customer['expense']
    list_expense = []
    for i in check_expense:
        x = re.findall("[0-9]+", i)
        list_expense.append(x)
    list_int_expense = sum(list_expense, [])
    list_int_expense = [int(i) for i in list_int_expense]
    sum_expense = sum(list_int_expense)
    return sum_expense

def showExpense(customer_id):
    data = sheet.get_all_records()
    listdata1 = pd.DataFrame(data)
    customer = listdata1[ listdata1['customer_id'] == customer_id ]
    show_expense = customer['expense']
    # for i in show_expense:
    # x = re.split(r"([\u0E00-\u0E7F]+)\s+(\d+)\s+([\u0E00-\u0E7F]+)", show_expense)
    return show_expense

#-------------------------Income---------------------------------------------------------------------
def loadCustomerSheet2():
    data = sheet2.get_all_records()
    listdata1 = pd.DataFrame(data)
    return listdata1

def ShowAllIncome(customer_id):
    data = sheet2.get_all_records()
    listdata1 = pd.DataFrame(data)
    customer = listdata1[ listdata1['customer_id'] == customer_id ]
    check_income = customer['income']
    income_list = ", ".join(str(x) for x in check_income)

    if income_list == "":
        return "ยังไม่มีบันทึก"
    else:
        return income_list

def searchIncome(customer_id):
    data = sheet2.get_all_records()
    listdata2 = pd.DataFrame(data)
    customer = listdata2[ listdata2['customer_id'] == customer_id ]
    check_income = customer['income']
    list_income = []
    for i in check_income:
        x = re.findall("[0-9]+", i)
        list_income.append(x)
    list_int_income = sum(list_income, [])
    list_int_income = [int(i) for i in list_int_income]
    sum_income = sum(list_int_income)
    return sum_income

def showIncome(customer_id):
    data = sheet2.get_all_records()
    listdata2 = pd.DataFrame(data)
    customer = listdata2[ listdata2['customer_id'] == customer_id ]
    show_income = customer['income']
    return show_income

#---------------------------------------------------------------------------------------------

@app.route('/ShowallExpense' , methods=['GET'])
def ShowallExpense():
    try:
        customer = request.args.get('customer_id')
        display_name = request.args.get('p_display_name')
        profile_img_url = request.args.get('p_profile_img_url')
        res = ShowAllExpense(customer)

        return jsonify({'message' : res })
    except Exception as e:
        return jsonify({'message' : 'ยังไม่มีบันทึกรายจ่าย',
                        "name" : display_name,
                        "profile_img"  : profile_img_url
                        })

@app.route('/getExpense' , methods=['GET'])
def getExpense():
    try:
        customer = request.args.get('customer_id')
        showEx = searchExpense(customer)        
        msg = "รายจ่ายรวม "+str(showEx)+" บาท"


        return jsonify({'message' : msg })
    except Exception as e:
        return jsonify({'message' : 'รายจ่ายรวม 0 บาท'})


@app.route('/insertExpense' , methods=['GET'])
def insertExpense():
    try:
        customer = request.args.get('customer_id')
        display_name = request.args.get('p_display_name')
        profile_img_url = request.args.get('p_profile_img_url')
        expense = request.args.get('expense')
        res = loadCustomerSheet()
        row = [ customer , display_name , profile_img_url , expense ]
        index = int(len(res)+2)
        sheet.insert_row(row, index)
        return jsonify({'message' : "เพิ่มรายจ่ายสำเร็จ",
                        "name" : display_name,
                        "profile_img"  : profile_img_url,
                        "expense"  : expense
                        })
    except Exception as e:
        return jsonify({'message' : 'error นะดูใหม่อีกที'})



#--------------------------------Income---------------------------------------------

@app.route('/ShowallIncome' , methods=['GET'])
def ShowallIncome():
    try:
        customer = request.args.get('customer_id')
        display_name = request.args.get('p_display_name')
        profile_img_url = request.args.get('p_profile_img_url')
        res = ShowAllIncome(customer)

        return jsonify({'message' : res,
                        "name" : display_name,
                        "profile_img"  : profile_img_url
                        })
    except Exception as e:
        return jsonify({'message' : 'ยังไม่มีบันทึกรายรับ'})

@app.route('/getIncome' , methods=['GET'])
def getIncome():
    try:
        customer = request.args.get('customer_id')
        showEx = searchIncome(customer)        
        msg = "รายรับรวม "+str(showEx)+" บาท"


        return jsonify({'message' : msg })
    except Exception as e:
        return jsonify({'message' : 'รายรับรวม 0 บาท'})


@app.route('/insertIncome' , methods=['GET'])
def insertIncome():
    try:
        customer = request.args.get('customer_id')
        display_name = request.args.get('p_display_name')
        profile_img_url = request.args.get('p_profile_img_url')
        income = request.args.get('income')
        res1 = loadCustomerSheet2()
        row = [ customer , display_name , profile_img_url , income ]
        index = int(len(res1)+2)
        sheet2.insert_row(row, index)
        return jsonify({'message' : "เพิ่มรายรับสำเร็จ",
                        "name" : display_name,
                        "profile_img"  : profile_img_url,
                        "income"  : income
                        })
    except Exception as e:
        return jsonify({'message' : 'error นะดูใหม่อีกที'})


if __name__ == '__main__':
    app.run(debug=True)