import os,sys,textwrap,time,io
arguments = False
def Checkfile(filepath):
    print("Starting scan of file: "+filepath)
    os.system('sigcheck.exe -w temp/signature -h "'+filepath)
    time.sleep(1)
    #filename = open("C:\Users\kress\Documents\Programmer\Python-AntiVirus\temp", "r")
    #filename = open(r"temp/signature", "r")
    filename = io.open("temp/signature", mode="r", encoding="unicode_internal")
    sig = filename.readlines()
    #print(sig)
    filename.close()
    time.sleep(1)
    signature = sig[11].replace("SHA1:", "")
    signature = textwrap.dedent(signature)
    print(signature)
    try:
        signature = signature.replace("\n","")
    except:
        pass
    #search database
    time.sleep(0.1)
    db = open("filedb", "r").read().split(",")
    #print("Info: DB length: "+len(db)+" Signature: "+signature)
    i = 0
    while i < len(db):
        print(db[i])
        if (signature == db[i]):
            print("Virus detected.")
            break
        i += 1
    print("Done!")

def Checkfolder(folderpath):
    print("Starting scan of folder: "+folderpath)
    files = os.listdir(folderpath)
    #files = sorted([os.path.join(folderpath, file) for file in os.listdir(folderpath)], key=os.path.getctime)
    print(files)
    i = 0
    while i < len(files):
        print(files[i])
        Checkfile(files[i])
        i += 1

def RealTimeProtection():
    print("Starting realtime protection")
    #os.system("wmic process get ExecutablePath | more >temp/process")
    time.sleep(2)
    processes = open("temp/process", "r").readlines()
    #processes = processes.replace("\r","\n")
    print(processes)
    i = 0
    while i < len(processes):
        processes[i] = processes[i].replace("\r","\n")
        #print("Path: "+processes[i])
        try:
            #os.system('sigcheck.exe -h "'+processes[i]+'" > temp/signature')
            #os.system('sigcheck.exe -w temp/signature -h "'+processes[i]+'"')
            Checkfile(processes[i])
        except Exception as err:
            print(err)
        i += 1
    
try:
    sys.argv[1]
    arguments = True
except:
    pass
if (arguments == True):
    arg1 = sys.argv[1].lower()
    if (arg1 == "/h"):
        print('''
    /h - Displays this help print.

    /s <full file path> - Scans the selected file.

    /sf <full folder path> - Scans a folder.

    /rtp - Scans running processes.

''')
    if (arg1 == "/s"):
        Checkfile(sys.argv[2])
    if (arg1 == "/sf"):
        Checkfolder(sys.argv[2])
    if (arg1 == "/rtp"):
        RealTimeProtection()
        
    #Checkfile(sys.argv[1])
#Checkfile("temp/filesignature")
