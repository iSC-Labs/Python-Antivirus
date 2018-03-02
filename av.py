import os,sys,textwrap,time,io,easygui,gzip
arguments = False
autocompress = False
def virusdetected(viruspath, sha1):
    print("Virus detected")
    flavor = easygui.buttonbox("A virus has been detected: \n"+viruspath+"\nWith SHA1: "+sha1+"\nDo you want to move the virus to quarantine?",
                               choices = ['Yes', 'No'])
    if (flavor == "Yes"):
        try:
            virusname = viruspath.split("\\")
            virusname = virusname[-1].replace("\n","")
        except:
            virusname = viruspath
        os.system('taskkill /f /im '+virusname[-1])
        try:
            os.system('move "'+viruspath+'" "'+os.path.dirname(os.path.realpath(__file__))+'\\quarantine"')
            print('move "'+viruspath+'" "'+os.path.dirname(os.path.realpath(__file__))+'\\quarantine"')
            #compress
            #inF = file("quarantine\\"+virusname[-1], 'rb')
            inF = file("quarantine\\"+virusname, 'rb')
            s = inF.read()
            inF.close()

            #outF = gzip.GzipFile("quarantine\\"+virusname[-1]+".gz", 'wb')
            outF = gzip.GzipFile("quarantine\\"+virusname+".gz", 'wb')
            outF.write(s)
            outF.close()
            #os.remove("quarantine\\"+virusname[-1])
            os.remove("quarantine\\"+virusname)
            easygui.msgbox ("Virus was moved to quarantine")
        except Exception as err:
            easygui.msgbox ("Error:\n"+str(err))
        print(viruspath)
    #easygui.msgbox("A virus has been detected at: \n"+viruspath+"\nWith SHA1: "+sha1)
    
def Checkfile(filepath):
    print("Starting scan of file: "+filepath)
    #os.system('sigcheck.exe -w temp/signature -h "'+filepath)
    os.system('sigcheck.exe -w temp/signature -h "'+filepath+" -nobanner")
    #time.sleep(1)
    filename = io.open("temp/signature", mode="r", encoding="unicode_internal")
    sig = filename.readlines()
    filename.close()
    #time.sleep(0.1)
    signature = sig[11].replace("SHA1:", "")
    signature = textwrap.dedent(signature)
    print(signature)
    try:
        signature = signature.replace("\n","")
    except:
        pass
    #search database
    #time.sleep(0.1)
    db = open("filedb", "r").read().split(",")
    i = 0
    while i < len(db):
        #print(db[i])
        if (signature == db[i]):
            virusdetected(filepath.replace("\n",""), signature)
            break
        i += 1

def Checkfolder(folderpath):
    print("Starting scan of folder: "+folderpath)
    os.system('cd "'+folderpath+'" && dir /s /b /a-d >"'+os.path.dirname(os.path.realpath(__file__))+'\\temp\\folderscan"')
    print('cd "'+folderpath+'" && dir /s /b /a-d >"'+os.path.dirname(os.path.realpath(__file__))+'\\temp\\folderscan"')
    files = open("temp\\folderscan", "r").readlines()
    print(files)
    progress = 0
    progresspr = 100 / len(files)
    i = 0
    while i < len(files):
        progress += progresspr
        print("Progress: "+str(progress)+"%")
        try:
            Checkfile(files[i])
        except Exception as err:
            print(err)
        #progress += progresspr
        #print("Progress: "+str(progress)+"%")
        i += 1
    print("Finished with following results:")

def RealTimeProtection():
    print("Starting realtime protection")
    os.system("wmic process get ExecutablePath | more >temp/process")
    time.sleep(2)
    processes = open("temp/process", "r").readlines()
    print(processes)
    i = 0
    while i < len(processes):
        processes[i] = processes[i].replace("\r","\n")
        try:
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

        /aq - Auto Quarentines viruses found.
''')

    i = 0
    while i < len(sys.argv):
        if (sys.argv[i] == "/aq"):
            autocompress = True
        i += 1
    if (autocompress == True):
        print("Auto Compressing: Enabled")
    else:
        print("Auto Compressing: Disabled")
    if (arg1 == "/s"):
        Checkfile(sys.argv[2])
    if (arg1 == "/sf"):
        Checkfolder(sys.argv[2])
    if (arg1 == "/rtp"):
        RealTimeProtection()

    #Checkfile(sys.argv[1])
#Checkfile("temp/filesignature")
