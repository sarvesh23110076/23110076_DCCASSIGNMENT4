from flask import Flask, redirect, url_for, request, Response, render_template
from flask_mysqldb import MySQL
import pandas as pd

app = Flask(__name__,template_folder="template")
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 's@@@rvesh@@@123'
app.config['MYSQL_DB'] = 'dccassign'

mysql = MySQL(app)

def create(userdetails1,L):
    data={}
    for i in L:
        data[i]=[]
    for i in userdetails1:
        for j in range(len(i)):
            data[L[j]].append(i[j])
    data=pd.DataFrame(data)
    data=data.set_index("Sr_No")
    return data

@app.route('/')
def main_page():
    return render_template("index0.html")

@app.route('/link1', methods = ["POST"])
def link1():
    return render_template("index.html")

@app.route('/link2', methods = ["POST"])
def link2():
    return render_template("index3.html")

@app.route('/user1', methods = ["POST"])
def user1():
    ps=["Date_of_Encashment","Name_of_the_Political_Party","Prefix","Bond_Number","Pay_Branch_Code","Pay_Teller"]
    date=request.form["date"]
    name=request.form["party"]
    prefix=request.form["prefix"]
    bnumber=request.form["bondnumber"]
    pcode=request.form["branchcode"]
    pteller=request.form["payteller"]
    check=[date,name,prefix,bnumber,pcode,pteller]
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from data1")
    userdetails=cursor.fetchall()
    L1=["Sr_No","Date_of_Encashment","Name_of_the_Political_Party","Account_no_of_Political_Party","Prefix","Bond_Number","Denominations","Pay_Branch_Code","Pay_Teller"]
    data1=create(userdetails,L1)
    for i in range(len(ps)):
        if check[i]!="":
            if len(data1)!=0:
                data1=data1[data1[ps[i]]==check[i]]
    return data1.to_html()

@app.route('/user2', methods = ["POST"])
def user2():
    ps=["Reference_No_URN","Journal_Date","Date_of_Purchase","Date_of_Expiry","Name_of_the_Purchaser","Prefix","Bond_Number","Issue_Branch_Code","Issue_Teller"]
    refer=request.form["refer"]
    date1=request.form["date1"]
    date2=request.form["date2"]
    date3=request.form["date3"]
    name=request.form["company"]
    prefix=request.form["prefix"]
    bnumber=request.form["bondnumber"]
    pcode=request.form["branchcode"]
    pteller=request.form["teller"]
    check=[f"{refer}",date1,date2,date3,name,prefix,bnumber,pcode,pteller]
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from data2")
    userdetails=cursor.fetchall()
    L1=["Sr_No","Reference_No_URN","Journal_Date","Date_of_Purchase","Date_of_Expiry","Name_of_the_Purchaser","Prefix","Bond_Number","Denominations","Issue_Branch_Code","Issue_Teller","Status"]
    data1=create(userdetails,L1)
    for i in range(len(ps)):
        if check[i]!="":
            if len(data1)!=0:
                data1=data1[data1[ps[i]]==check[i]]
    return data1.to_html(escape=True)

@app.route('/user3', methods = ["POST"])
def user3():
    name=request.form["company"]
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from data2")
    userdetails=cursor.fetchall()
    L1=["Sr_No","Reference_No_URN","Journal_Date","Date_of_Purchase","Date_of_Expiry","Name_of_the_Purchaser","Prefix","Bond_Number","Denominations","Issue_Branch_Code","Issue_Teller","Status"]
    data1=create(userdetails,L1)
    year=list(data1[data1["Name_of_the_Purchaser"]==f"{name}"]["Date_of_Purchase"])
    don=list(data1[data1["Name_of_the_Purchaser"]==f"{name}"]["Denominations"])
    for i in range(len(year)):
        year[i]=year[i][:4]
    years=list(pd.Series(year).unique())
    donate=[]
    count=[]
    for i in range(len(years)):
        don1=[]
        count1=0
        for j in range(len(year)):
            if years[i]==year[j]:
                count1=count1+1
                don1.append(don[i])
        sum=0
        for i in range(len(don1)):
            don1[i]=int(don1[i])
            sum=sum+don1[i]
        donate.append(sum)
        count.append(count1)
    dic={}
    dic["Name of Purchaser"]=[name for i in range(len(count))]
    dic["Year"]=years
    dic["Number of bonds"]=count
    dic["Total value of bonds"]=donate
    dic=pd.DataFrame(dic)
    dic=dic.set_index("Name of Purchaser")
    return render_template('new1.html', page_data=dic.to_html().split("\n"), key=dic["Year"], val=dic["Number of bonds"])


@app.route('/user4', methods = ["POST"])
def user4():
    name=request.form["party"]
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from data1")
    userdetails=cursor.fetchall()
    L1=["Sr_No","Date_of_Encashment","Name_of_the_Political_Party","Account_no_of_Political_Party","Prefix","Bond_Number","Denominations","Pay_Branch_Code","Pay_Teller"]
    data1=create(userdetails,L1)
    year=list(data1[data1["Name_of_the_Political_Party"]==f"{name}"]["Date_of_Encashment"])
    don=list(data1[data1["Name_of_the_Political_Party"]==f"{name}"]["Denominations"])
    for i in range(len(year)):
        year[i]=year[i][:4]
    years=list(pd.Series(year).unique())
    donate=[]
    count=[]
    for i in range(len(years)):
        don1=[]
        count1=0
        for j in range(len(year)):
            if years[i]==year[j]:
                count1=count1+1
                don1.append(don[i])
        sum=0
        for i in range(len(don1)):
            don1[i]=int(don1[i])
            sum=sum+don1[i]
        donate.append(sum)
        count.append(count1)
    dic={}
    dic["Name of the Political Party"]=[name for i in range(len(count))]
    dic["Year"]=years
    dic["Number of bonds"]=count
    dic["Total value of bonds"]=donate
    dic=pd.DataFrame(dic)
    dic=dic.set_index("Name of the Political Party")
    return render_template('new1.html', page_data=dic.to_html().split("\n"), key=dic["Year"], val=dic["Number of bonds"])

@app.route('/user5', methods = ["POST"])
def user5():
    name=request.form["party"]
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from data1")
    userdetails=cursor.fetchall()
    L1=["Sr_No","Date_of_Encashment","Name_of_the_Political_Party","Account_no_of_Political_Party","Prefix","Bond_Number","Denominations","Pay_Branch_Code","Pay_Teller"]
    data1=create(userdetails,L1)
    cursor.execute(f"select * from data2")
    userdetails=cursor.fetchall()
    L1=["Sr_No","Reference_No_URN","Journal_Date","Date_of_Purchase","Date_of_Expiry","Name_of_the_Purchaser","Prefix","Bond_Number","Denominations","Issue_Branch_Code","Issue_Teller","Status"]
    data2=create(userdetails,L1)
    data1=data1[data1["Name_of_the_Political_Party"]==name]
    bond=list(data1["Bond_Number"])
    f=[]
    g=[]
    for i in range(len(bond)):
        data1=list(data2[data2["Bond_Number"]==bond[i]]["Name_of_the_Purchaser"])
        data11=list(data2[data2["Bond_Number"]==bond[i]]["Denominations"])
        f.append(data1)
        g.append(data11)
    newbond,newd,newf=[],[],[]
    for i in range(len(f)):
        if f[i]!=[]:
            for j in range(len(f[i])):
                newbond.append(bond[i])
                newf.append(f[i][j])
                newd.append(g[i][j])
    
    k=[name for i in range(len(newbond))]
    dic={}
    dic["Name_of_the_Political_Party"]=k
    dic["Name_of_the_Purchaser"]=newf
    dic["Bond_Number"]=newbond
    dic["Denominations"]=newd
    dic=pd.DataFrame(dic)

    purchaser=dic["Name_of_the_Purchaser"].unique()
    donate=[]
    for i in range(len(purchaser)):
        dic1=list(dic[dic["Name_of_the_Purchaser"]==purchaser[i]]["Denominations"])
        sum=0
        for i in range(len(dic1)):
            dic1[i]=int(dic1[i])
            sum=sum+dic1[i]
        donate.append(sum)
    display={}
    display["Name_of_the_Political_Party"]=[name for i in range(len(purchaser))]
    display["Name_of_the_Purchaser"]=purchaser
    display["Denominations"]=donate
    display=pd.DataFrame(display)
    display=display.set_index("Name_of_the_Political_Party")
    return render_template('new2.html', page_data=display.to_html().split("\n"), key=display["Name_of_the_Purchaser"], val=display["Denominations"])


@app.route('/user6', methods = ["POST"])
def user6():
    name=request.form["company"]
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from data1")
    userdetails=cursor.fetchall()
    L1=["Sr_No","Date_of_Encashment","Name_of_the_Political_Party","Account_no_of_Political_Party","Prefix","Bond_Number","Denominations","Pay_Branch_Code","Pay_Teller"]
    data1=create(userdetails,L1)
    cursor.execute(f"select * from data2")
    userdetails=cursor.fetchall()
    L1=["Sr_No","Reference_No_URN","Journal_Date","Date_of_Purchase","Date_of_Expiry","Name_of_the_Purchaser","Prefix","Bond_Number","Denominations","Issue_Branch_Code","Issue_Teller","Status"]
    data2=create(userdetails,L1)
    data2=data2[data2["Name_of_the_Purchaser"]==name]
    bond=list(data2["Bond_Number"])
    f=[]
    g=[]
    for i in range(len(bond)):
        data2=list(data1[data1["Bond_Number"]==bond[i]]["Name_of_the_Political_Party"])
        data11=list(data1[data1["Bond_Number"]==bond[i]]["Denominations"])
        f.append(data2)
        g.append(data11)
    newbond,newd,newf=[],[],[]
    for i in range(len(f)):
        if f[i]!=[]:
            for j in range(len(f[i])):
                newbond.append(bond[i])
                newf.append(f[i][j])
                newd.append(g[i][j])
    k=[name for i in range(len(newbond))]
    dic={}
    dic["Name_of_the_Purchaser"]=k
    dic["Name_of_the_Political_Party"]=newf
    dic["Bond_Number"]=newbond
    dic["Denominations"]=newd
    dic=pd.DataFrame(dic)
    purchaser=dic["Name_of_the_Political_Party"].unique()
    donate=[]
    for i in range(len(purchaser)):
        dic1=list(dic[dic["Name_of_the_Political_Party"]==purchaser[i]]["Denominations"])
        sum=0
        for i in range(len(dic1)):
            dic1[i]=int(dic1[i])
            sum=sum+dic1[i]
        donate.append(sum)
    display={}
    display["Name_of_the_Purchaser"]=[name for i in range(len(purchaser))]
    display["Name_of_the_Political_Party"]=purchaser
    display["Denominations"]=donate
    display=pd.DataFrame(display)
    display=display.set_index("Name_of_the_Purchaser")
    return render_template('new2.html', page_data=display.to_html().split("\n"), key=display["Name_of_the_Political_Party"], val=display["Denominations"])

if __name__ == '__main__':
   app.run(debug = True) 
