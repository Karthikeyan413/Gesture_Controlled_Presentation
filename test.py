from pptx import Presentation
import win32com.client
Application = win32com.client.Dispatch("PowerPoint.Application")
Presentation = Application.Presentations.Open(r"C:\Users\Oomkara\Documents\DAA NQueens project.pptx")
Presentation.Slides[0].Export(r"D:\projects\PPT_opencv\Presentation\1.jpg", "JPG")
Application.Quit()
Presentation =  None
Application = None
