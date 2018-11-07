import c4d, os
from c4d import gui 
from c4d import documents, plugins

ID_OCTANE_LIVEPLUGIN = 1029499
ID_OCTANE_VIDEOPOST_RENDERER = 1029525
ID_OCTANE_VIDEOPOST = 1005172

#Function to set 'Render Settings - Frame Range' to 'Current Frame'

def setCurrentFrame():
    def tool():
        return plugins.FindPlugin(doc.GetAction(), c4d.PLUGINTYPE_TOOL)

    def object():
        return doc.GetActiveObject()

    def tag():
        return doc.GetActiveTag()

    def renderdata():
        return doc.GetActiveRenderData()

    def prefs(id):
        return plugins.FindPlugin(id, c4d.PLUGINTYPE_PREFS)

    renderdata()[c4d.RDATA_FRAMESEQUENCE]=1
    
def setTexturesPaths():    
    path1 = c4d.GetGlobalTexturePath(0)
    ActiveDocument = documents.GetActiveDocument()
    texPath = ActiveDocument.GetDocumentPath()
    if not path1:
        c4d.SetGlobalTexturePath(0, texPath)

#Main Function, this gets executed on start
def main():
    #Get Active Document
    ActiveDocument = documents.GetActiveDocument()
    
    #Get Document Path & Name
    increment = 0
    DocPathBase = ActiveDocument.GetDocumentPath()    
    DocName = ActiveDocument.GetDocumentName()    
    DocNameLength = len(DocName)-4
    DocNameShort = DocName[0:DocNameLength] 
    DocPathBase += "\\" + "Render" + "\\" + DocNameShort + "_" 
    DocPath = DocPathBase + str(increment)
            
    fps = doc.GetFps() 
    
    ###
    helpMessage = """Enter the first frame, enter the second frame. (There is an extra pop up window for the first and last frame, respectively.)

Now the Script will run and automatically set your 'Setting, Frame-Range' to 'Current Frame'.

Sets yor 'Preferences, Texture Paths' to your working Directory (The Directory of your current C4D working File).

Checks if a 'Render' Folder exists in the same Directory, and creates it if necessary.

Checks if a Folder inside 'Render' with the name of your current C4D File exists and then create an incremented Folder.

Saves a new C4D File inside this Folder for every Frame."""
###

    #Get User Framerange input   
    startFrameIn = c4d.gui.InputDialog("Enter Start Frame - or type 'help'")
    if startFrameIn.lower() == "help":
        c4d.gui.MessageDialog(helpMessage)
    endFrameIn = c4d.gui.InputDialog("Enter End Frame - or type 'help'")
    if endFrameIn.lower() == "help":
        c4d.gui.MessageDialog(helpMessage)
    
    #Check User Input
    if not startFrameIn or not endFrameIn: #Is there any User Onput?
        c4d.gui.MessageDialog("No valid Framerange was given. Script cancelled without Effect.")
        return        
    else: #if there is User Input
        try: #Is the User Input an Integer?
            startFrame = int(startFrameIn)
            endFrame = int(endFrameIn)
        except ValueError:
            c4d.gui.MessageDialog("Only Integer values allowed. Script cancelled without Effect.")
            return
    
    setTexturesPaths()
    
    setCurrentFrame() #Rendersettings current Frame

    fps = doc[c4d.DOCUMENT_FPS]
    frame = startFrame
    Time = c4d.BaseTime(frame,fps)
    doc.SetTime(Time)
    c4d.EventAdd()
    rDat = doc.GetActiveRenderData()
    octane = rDat.GetFirstVideoPost()
    rDatIncr = rDat[c4d.RDATA_PATH]
    rOctIncr = octane[c4d.SET_PASSES_SAVEPATH]
    print(rOctIncr)
    rvalue = True
    folderExists = False

    if not os.path.exists(DocPath):
          os.makedirs(DocPath)                  
    else:
        while not folderExists: # if the folder already exists, increment and create a new one
            increment += 1
            DocPath = DocPathBase + str(increment)
            if not os.path.exists(DocPath):
                os.makedirs(DocPath)
                folderExists = True
            if increment > 500: #To prevent infinite loop if something goes wrong
                rvalue = gui.QuestionDialog("A Folder with the name " + DocName + " already exists. Overwirte frames with the same name? This message appears, if more than 500 Folder exist inside the Render Folder.")
                break    
                
    if rvalue:
        if startFrame <= endFrame: # Loop from StartFrame to EndFrame
            for curFrame in xrange(startFrame, endFrame+1):
                CreateC4DDocs(DocPath, DocNameShort, curFrame, rDat, rDatIncr, rOctIncr, octane)    
        else: # Loop from EndFrame to StartFrame
            for curFrame in xrange(startFrame, endFrame-1, -1):
                print(curFrame)
                CreateC4DDocs(DocPath, DocNameShort, curFrame, rDat, rDatIncr, rOctIncr, octane, False)   
    else:
        exit = gui.MessageDialog("Please save the project with a different name, or choose a new frame range")

def CreateC4DDocs(DocPath, DocNameShort, curFrame, rDat, rDatIncr, rOctIncr, octane, forward = True):
    saveAs = DocPath + "\\" + DocNameShort + "_r" + str(curFrame) + ".c4d"     

    #Save every Frame Functionality------------------------------------------------------
    
    #Change RenderPath
    rDatIncr += "_r" + str(curFrame)
    rOctIncr += "_r" + str(curFrame)
    rDat[c4d.RDATA_PATH] = rDatIncr
    octane[c4d.SET_PASSES_SAVEPATH] = rOctIncr
    c4d.EventAdd()

    c4d.documents.SaveDocument(doc, saveAs, c4d.SAVEDOCUMENTFLAGS_0, c4d.FORMAT_C4DEXPORT)  

    #FrameForward
    if forward:
        c4d.CallCommand(12414)   
    else:
        c4d.CallCommand(12413)  


if __name__=='__main__':
    main()

