import c4d, os
from c4d import gui 
from c4d import documents, plugins


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
    
    #Get User Framerange input   
    startFrameIn = c4d.gui.InputDialog("Start Frame")
    endFrameIn = c4d.gui.InputDialog("End Frame")
    
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
                CreateC4DDocs(DocPath, DocNameShort, curFrame)    
        else: # Loop from EndFrame to StartFrame
            for curFrame in xrange(startFrame, endFrame-1, -1):
                print(curFrame)
                CreateC4DDocs(DocPath, DocNameShort, curFrame, False)   
    else:
        exit = gui.MessageDialog("Please save the project with a different name, or choose a new frame range")

def CreateC4DDocs(DocPath, DocNameShort, curFrame, forward = True):
    saveAs = DocPath + "\\" + DocNameShort + "_r" + str(curFrame) + ".c4d"       


    #Save every Frame Functionality------------------------------------------------------

    c4d.documents.SaveDocument(doc, saveAs, c4d.SAVEDOCUMENTFLAGS_0, c4d.FORMAT_C4DEXPORT)

    #FrameForward
    if forward:
        c4d.CallCommand(12414)   
    else:
        c4d.CallCommand(12413)  


if __name__=='__main__':
    main()

