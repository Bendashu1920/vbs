import os
import re

vbs = "button.vbs"
remove_line1 = 'obj1.Run "cmd /c python element.py",0'
remove_line2 = 'obj1.Run "cmd /k mkdir .\PageElement && mkdir .\vbs",0'
name_list = ["Basic", "Form", "Data", "Notice", "Navigation", "Others"]
element_addr = "./PageElement/button.txt"
reserve_list = ["Layout Container", "InputNumber", "TimePicker", "DatePicker", "DateTimePicker",
                "ColorPicker", "MessageBox", "NavMenu", "PageHeader", "InfiniteScroll"]

abs_dir = os.path.dirname(os.path.abspath(__file__))
vbs_dir = abs_dir + "\\vbs"

def check():

    valid_list = []
    status = False

    while 1:
        if os.path.exists(element_addr):
            # 文件格式比较特殊
            fr = open(element_addr, "r", encoding="utf-16-le")
            for line in fr.readlines():
                if line.strip() == "Basic":
                    status = True
                if status > 0:
                    if len(name_list) > 0:
                        if line.find(name_list[0]) == -1:
                            valid_list.append(line.strip())
                        else:
                            name_list.pop(0)
                    else:
                        valid_list.append(line.strip())
                        if line.strip() == "Drawer":
                            break
            break

    return valid_list

def transform(name):
    if name in reserve_list:
        if name == "Layout Container":
            return "container"
        elif name == "DateTimePicker":
            return "datetime-picker"
        elif name == "NavMenu":
            return "menu"
        elif name == "InfiniteScroll":
            return "infiniteScroll"
        else:
            pattern = re.compile(r"[A-Z]+[a-z]+")
            matches = pattern.findall(name)
            return "-".join(list(map(lambda string:string[0].lower()+string[1:], matches)))
    else:
        return name[0].lower() + name[1:]

vbs_read = open("button.vbs", "r")
valid_list = check()
vbs_n = open(os.path.join(vbs_dir, "new.vbs"), "w")
vbs_n.write('Dim obj1\n')
vbs_n.write('Set obj1 = Wscript.CreateObject("Wscript.Shell")\n')

for name in sorted(list(map(transform,valid_list))):
    if name != "button":
        op1 = 'obj1.Run "cmd /c c: && cd %ProgramFiles(x86)%\Google\Chrome\Application && .\chrome.exe --new-window https://element.eleme.io/#/en-US/component/button",0\n'
        op1 = op1.replace("/button", "/"+name)
        vbs_n.write(op1)
        vbs_n.write('Wscript.Sleep 1000\n')
        vbs_n.write('obj1.SendKeys "{F11}"\n')
        vbs_n.write('Wscript.Sleep 1000\n')
        vbs_n.write('obj1.SendKeys "^a"\n')
        vbs_n.write('Wscript.Sleep 1000\n')
        vbs_n.write('obj1.SendKeys "^c"\n')
        vbs_n.write('Wscript.Sleep 1000\n')
        op2 = 'obj1.Run "powershell.exe get-clipboard > .\PageElement\\button.txt",0\n'
        op2 = op2.replace("button", name.replace("-", "_"))
        vbs_n.write(op2)
        vbs_n.write('Wscript.Sleep 1000\n')
        vbs_n.write('obj1.SendKeys "%{F4}"\n')
        vbs_n.write('Wscript.Sleep 3000\n')

vbs_n.close()

for file in list(os.listdir(vbs_dir)):
    os.system("wscript "+os.path.join(vbs_dir, file))
    # while 1:
    #     if os.path.exists(abs_path+"/PathElement/"+file.replace(".vbs", ".txt")):
    #         break