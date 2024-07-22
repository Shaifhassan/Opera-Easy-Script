Function Json(keysRange As Range, valuesRange As Range) As String
    Dim jsonString As String
    Dim i As Integer
    
    ' Check if the ranges have the same number of columns
    If keysRange.Columns.Count <> valuesRange.Columns.Count Then
        Json = "Error: Ranges must have the same number of columns"
        Exit Function
    End If
    
    ' Initialize the JSON string
    jsonString = "{"
    
    ' Loop through each column in the ranges
    For i = 1 To keysRange.Columns.Count
        ' Add the key and value to the JSON string
        jsonString = jsonString & """" & keysRange.Cells(1, i).Value & """: """ & valuesRange.Cells(1, i).Value & """"
        
        ' Add a comma if it's not the last item
        If i < keysRange.Columns.Count Then
            jsonString = jsonString & ", "
        End If
    Next i
    
    ' Close the JSON string
    jsonString = jsonString & "}"
    
    ' Return the JSON string
    Json = jsonString
End Function