import os, re
import requests
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import askdirectory

usedefault = True

def main():
    global usedefault
    
    win = Tk()
    win.title("图片抓取器 V0.3.1 -- By lanlan2_")
    win.resizable(0, 0)

    def settings():
        top1 = Toplevel()
        top1.title("设置（没做完请见谅）")
        #TODO: add default values

    def about_thanks():
        top2 = Toplevel()
        top2.title("关于&致谢")
        text2 = Text(top2, width=50, height=15, relief=FLAT)
        text2.insert(INSERT, "一个简单的图片抓取器，仅支持百度图片的抓取\n\n")
        text2.insert(INSERT, "特别致谢：\n\n")
        text2.insert(INSERT, "知乎的CoderMan，TA提供了下载文件的核心逻辑。\n\n")
        text2.insert(INSERT, "CSDN的PainfulEye，TA提供了文件大小转换算法。\n")
        text2["state"] = "disabled"
        text2.pack()
    
    menubar = Menu(win)
    menubar.add_command(label="设置", command=settings)
    menubar.add_command(label="关于&致谢", command=about_thanks)
    menubar.add_command(label="关闭", command=win.destroy)
    win.config(menu=menubar)

    fm1 = Frame(win)
    fm2 = Frame(win)
    sep = Separator(win, orient=HORIZONTAL)
    fm3 = Frame(win)
    fm1.pack()
    fm2.pack()
    sep.pack(fill=X, pady=5, padx=5)
    fm3.pack(fill=X)

    labfm1 = LabelFrame(fm1, text="下载设置")
    labfm1.pack(fill=X)
    labfm2 = LabelFrame(fm1, text="状态")
    labfm2.pack(fill=X)

    fmin1 = Frame(labfm1)
    fmin2 = Frame(labfm1)
    fmin3 = Frame(labfm1)
    fmin1.pack(fill=X, pady=5)
    fmin2.pack(fill=X, pady=5)
    fmin3.pack(fill=X, pady=5)

    lab1 = Label(fmin1, text="关键词:")
    lab1.grid(row=0, column=0)

    var1 = StringVar()
    ent1 = Entry(fmin1, textvariable=var1)
    ent1.grid(row=0, column=1)

    lab2 = Label(fmin2, text="搜索页数:")
    lab2.grid(row=0, column=0)
    ent2 = Entry(fmin2)
    ent2.insert(0, "2")
    ent2.grid(row=0, column=1)

    lab3 = Label(fmin3, text="保存目录:")
    lab3.grid(row=0, column=0)

    var2 = StringVar()
    ent3 = Entry(fmin3, width=50, textvariable=var2)
    var2.set(os.getcwd())
    ent3.grid(row=0, column=1)

    def callback1(*args):
        global usedefault
        
        if usedefault == True:
            var2.set(os.path.join(os.getcwd(), var1.get()))
            usedefault = True

    def callback2(*args):
        global usedefault
        
        usedefault = False

    var1.trace("w", callback1)
    var2.trace("w", callback2)

    def choosedir():
        dire = askdirectory()
        if dire != "":
            ent3.delete(0, END)
            ent3.insert(0, dire)

    butt = Button(fmin3, width=4, text="...", command=choosedir)
    butt.grid(row=0, column=2, padx=5)

    text = Text(labfm2, height=10, width=50, state="disabled")
    text.pack(fill=X)
    lab4 = Label(labfm2, text="等待中......")
    lab4.pack(anchor=W)

    def get_images_from_baidu(keyword, page_num, save_dir):
        def convert_size(text):
            units = ["B", "KB", "MB", "GB", "TB", "PB"]
            size = 1024
            for i in range(len(units)):
                if (text/ size) < 1:
                    return "%.2f%s" % (text, units[i])  # 返回值保留小数点后两位
                text = text/ size

        # UA 伪装：当前爬取信息伪装成浏览器
        # 将 User-Agent 封装到一个字典中
        # 【（网页右键 → 审查元素）或者 F12】 → 【Network】 → 【Ctrl+R】 → 左边选一项，右边在 【Response Hearders】 里查找
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        # 请求的 url
        url = 'https://image.baidu.com/search/acjson?'
        n = 0
        size = 0
        for pn in range(0, 30 * page_num, 30):
            # 请求参数
            param = {'tn': 'resultjson_com',
                     # 'logid': '7603311155072595725',
                     'ipn': 'rj',
                     'ct': 201326592,
                     'is': '',
                     'fp': 'result',
                     'queryWord': keyword,
                     'cl': 2,
                     'lm': -1,
                     'ie': 'utf-8',
                     'oe': 'utf-8',
                     'adpicid': '',
                     'st': -1,
                     'z': '',
                     'ic': '',
                     'hd': '',
                     'latest': '',
                     'copyright': '',
                     'word': keyword,
                     's': '',
                     'se': '',
                     'tab': '',
                     'width': '',
                     'height': '',
                     'face': 0,
                     'istype': 2,
                     'qc': '',
                     'nc': '1',
                     'fr': '',
                     'expermode': '',
                     'force': '',
                     'cg': '',    # 这个参数没公开，但是不可少
                     'pn': pn,    # 显示：30-60-90
                     'rn': '30',  # 每页显示 30 条
                     'gsm': '1e',
                     '1618827096642': ''
                     }
            request = requests.get(url=url, headers=header, params=param)
            if request.status_code == 200:
                text["state"] = "normal"
                text.insert(END, f'开始下载第{pn//30+1}页的图片......\n')
                text["state"] = "disabled"
            request.encoding = 'utf-8'
            # 正则方式提取图片链接
            html = request.text
            image_url_list = re.findall('"thumbURL":"(.*?)",', html, re.S)
            #print(image_url_list)
            # # 换一种方式
            # request_dict = request.json()
            # info_list = request_dict['data']
            # # 看它的值最后多了一个，删除掉
            # info_list.pop()
            # image_url_list = []
            # for info in info_list:
            #     image_url_list.append(info['thumbURL'])

            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            for image_url in image_url_list:
                image_data = requests.get(url=image_url, headers=header).content
                with open(os.path.join(save_dir, f'{n:06d}.jpg'), 'wb') as fp:
                    fp.write(image_data)
                text["state"] = "normal"
                text.insert(END, f'{os.path.join(save_dir, f"{n:06d}.jpg")}保存成功！\n')
                text["state"] = "disabled"
                text.see(END)
                size += os.path.getsize(os.path.join(save_dir, f"{n:06d}.jpg"))
                lab4["text"] = f"已下载{n+1}个文件，总体积为{convert_size(size)}"
                n = n + 1
                win.update()

        text["state"] = "normal"
        text.insert(END, '大功告成！')
        text["state"] = "disabled"

    def start():
        keyword = ent1.get()
        if keyword.strip() == "":
            showwarning("警告", "关键词不能为空！")
            return

        page_num = ent2.get()
        if page_num.strip() == "":
            showwarning("警告", "搜索页数不能为空！")
            return
        try:
            page_num = int(page_num)
        except Exception:
            showwarning("警告", "搜索页数只能是数字！")
            return
        
        save_dir = ent3.get()
        if not os.path.exists(save_dir):
            try:
                os.mkdir(save_dir)
            except Exception:
                showwarning("警告", "保存路径错误！")
                return

        text["state"] = "normal"
        text.delete(1.0, END)
        text["state"] = "disabled"

        but1["state"] = "disabled"

        get_images_from_baidu(keyword, page_num, save_dir)
        
        but1["state"] = "normal"

    def opendir():
        save_dir = ent3.get()
        if not os.path.exists(save_dir):
            showwarning("警告", "预览路径不存在！")
            return
        os.startfile(save_dir)

    #pwd = PanedWindow(fm3, orient=HORIZONTAL)
    #pwd.pack(fill=X, expand=True)

    but1 = Button(fm3, text="开始", command=start)
    but1.pack(side=LEFT, padx=20, pady=5)
    #pwd.add(but1, weight=1)
    but2 = Button(fm3, text="预览", command=opendir)
    but2.pack(side=RIGHT, padx=20, pady=5)
    #pwd.add(but2, weight=1)

    win.mainloop()

if __name__ == "__main__":
    main()
