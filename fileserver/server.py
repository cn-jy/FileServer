from flask import Flask,render_template,request,send_from_directory
import os,hashlib
with open("filelist.txt","r") as f:
    filel=f.read().split("\n")
flist=[]
for i in filel:
    flist.append(i.split(":"))
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=1024*1024
@app.route("/")
def index():
    return render_template("index.html",fl=flist)
@app.route("/upload",methods=["GET","POST"])
def upload():
    os.system("del /q temp")
    if request.method=="GET":
        return render_template("upload.html")
    file=request.files["file"]
    fileid=request.form["fname"]
    pwd=request.form["pwd"]
    if len(fileid)>9 or len(pwd)>9:
        return "先看一眼使用须知!"
    if ':' in fileid:
        return "先看一眼使用须知!"
    for i in flist:
        if fileid==i[0]:
            return "先看一眼使用须知!"
    pwd=hashlib.md5(pwd.encode()).hexdigest()
    flist.append([fileid,file.filename,pwd])
    file.save("./files/{}.bin".format(fileid))
    with open("filelist.txt","a") as f:
        f.write("{}:{}:{}\n".format(fileid,file.filename,pwd))
    return render_template("index1.html",fileid=fileid)
@app.route("/download",methods=["GET","POST"])
def download():
    if request.method=="GET":
        return render_template("download.html")
    fileid=request.form["id"]
    pwd=hashlib.md5(request.form["pwd"].encode()).hexdigest()
    for i in flist:
        if i[0]==fileid and i[2]==pwd:
            os.system("copy .\\files\\{}.bin .\\temp\\{}".format(fileid,i[1]))
            return send_from_directory(".\\temp",i[1])
    return render_template("download1.html")
app.run("0.0.0.0",80)
