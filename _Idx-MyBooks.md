# _Idx-MyBooks
[[header |Main]] | [[_Idx-AA_Journal|_Idx-AA_Journal]]


```dataview
TABLE WITHOUT ID file.link as "MyBookList" 
from "AA_Journal/MyBooks" 
WHERE file.name != this.file.name
sort file.name asc
```