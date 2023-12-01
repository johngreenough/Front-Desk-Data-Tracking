Dim objFSO, objFile
Dim oldFileName, newFileName

' Specify the old and new file names
oldFileName = "C:\Path\To\Your\OldFileName.xlsx"
newFileName = "C:\Path\To\Your\NewFileName.xlsx"

' Create a File System Object
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Check if the old file exists
If objFSO.FileExists(oldFileName) Then
    ' Rename the file
    objFSO.MoveFile oldFileName, newFileName
    WScript.Echo "File renamed successfully."
Else
    WScript.Echo "Old file not found."
End If

' Clean up
Set objFSO = Nothing
