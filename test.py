from pptx import Presentation
import win32com.client
import os


curPath = os.path.dirname(os.path.abspath(__file__))
folderPath = os.path.join(curPath,"Presentation")


Application = win32com.client.Dispatch("PowerPoint.Application")
Presentation = Application.Presentations.Open(os.path.join(folderPath,"MLT Project.pptx"))

for i in range(len(Presentation.slides)):
    Presentation.Slides[i].Export(os.path.join(folderPath,f"{i}.jpg"), "JPG")

Application.Quit()
Presentation =  None
Application = None
