# emic-crawler

EMIC.py
--
自己在電腦上試做的版本，成功執行後與課程範例結合修改

emic-crawler.py 
--
複製網頁內容下來  
遇到亂碼的問題把res.text改成res.content再改回去就可以了  
res.text跟res.content都可以用只是res.content會有報錯  

emic-writer.py
--
解決囉爽啦  
把檢查用的print留著  
遇到的問題是gcp不讓覆寫檔案，只讓寫新東西在指定路徑裡  
原本那樣會找不到路徑所以出錯，因此新增tempdes="/tmp/"+filename
  
另外亂碼的問題把utf-8改成utf_8或utf_8_sig都可以試試，反正有用
