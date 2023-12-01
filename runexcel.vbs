Dim objExcel, sourceWorkbook, targetWorkbook, sourceSheet, newSheet

' Create an Excel Application object
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False

' Set the source workbook (Dropin_Tracker_F23_for_John)
Set sourceWorkbook = objExcel.Workbooks.Open("C:\Path\To\Your\Dropin_Tracker_F23_for_John.xlsx")

' Set the source sheet (Overall)
Set sourceSheet = sourceWorkbook.Sheets("Overall")

' Create a new workbook (frontdeskdata)
Set targetWorkbook = objExcel.Workbooks.Add

' Copy the sheet to the new workbook
sourceSheet.Copy Before:=targetWorkbook.Sheets(1)

' Rename the copied sheet to match the original sheet name
Set newSheet = targetWorkbook.Sheets(1)
newSheet.Name = "Overall"

' Save the new workbook
targetWorkbook.SaveAs "C:\Path\To\Your\frontdeskdata.xlsx"

' Optionally, close the new workbook without saving changes to the original template
targetWorkbook.Close False

' Clean up
sourceWorkbook.Close False
objExcel.Quit

' Release the objects from memory
Set newSheet = Nothing
Set sourceSheet = Nothing
Set targetWorkbook = Nothing
Set sourceWorkbook = Nothing
Set objExcel = Nothing
