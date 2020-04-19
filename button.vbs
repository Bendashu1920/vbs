Dim obj1
Set obj1 = Wscript.CreateObject("Wscript.Shell")
Wscript.Sleep 1000
obj1.Run "cmd /k mkdir .\PageElement && mkdir .\vbs",0
Wscript.Sleep 1000
obj1.Run "cmd /c c: && cd %ProgramFiles(x86)%\Google\Chrome\Application && .\chrome.exe --new-window https://element.eleme.io/#/en-US/component/button",0
Wscript.Sleep 1000
obj1.SendKeys "{F11}"
Wscript.Sleep 1000
obj1.SendKeys "^a"
Wscript.Sleep 1000
obj1.SendKeys "^c"
Wscript.Sleep 1000
obj1.Run "powershell.exe get-clipboard > .\PageElement\button.txt",0
Wscript.Sleep 1000
obj1.SendKeys "%{F4}"
Wscript.Sleep 3000
obj1.Run "cmd /c python element.py",0