import ctypes
import json
import os
import sys
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import ImageTk, Image

class WallpaperChange(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.json_name = self.resource_path("settings.json")
        with open(self.json_name, "r", encoding="utf-8") as f:
            self.settings = json.load(f)
        self.file = self.settings["wall_paper"]
        self.language = self.settings["language"]
        func_info = self.settings[self.language]["init"]
        
        self.master.geometry(func_info["geometry"])
        self.master.title("wallpaper change")
        self.master.resizable(False, False)
        self.create_widget()
    
    # jsonファイルの位置特定
    def resource_path(self, filename):
        base_path = os.path.dirname(sys.argv[0])
        return os.path.join(base_path, filename)
    
    # ウィジェットの作成
    def create_widget(self):
        func_info = self.settings[self.language]["create_widget"]
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        setting_menu = Menu(menubar, tearoff=0)
        language_menu = Menu(setting_menu, tearoff=0)
        menubar.add_cascade(label=func_info["setting"], menu=setting_menu)
        setting_menu.add_cascade(label=func_info["language"], menu=language_menu)
        language_menu.add_command(label="日本語", command=lambda:self.language_change("ja"))
        language_menu.add_command(label="English", command=lambda:self.language_change("en"))
        language_menu.add_command(label="한국어", command=lambda:self.language_change("kan"))
        language_menu.add_command(label="español", command=lambda:self.language_change("es"))
        setting_menu.add_command(label=func_info["end"], command=self.master.destroy)
        
        self.listbox = Listbox(self.master, height=15, width=31, selectmode="single", takefocus=0)
        self.listbox.place(x=func_info["listbox_x"], y=func_info["listbox_y"])
        self.listbox.bind("<Return>", self.change)
        self.listbox.bind("<BackSpace>", self.delete)
        self.listbox.bind("<ButtonRelease-1>", self.image_show)
        
        button = Button(self.master, text=func_info["button1"], command=self.select_file)
        button.place(x=func_info["button1_x"], y=func_info["button1_y"])
        
        button = Button(self.master, text=func_info["button2"], command=self.swap)
        button.place(x=func_info["button2_x"], y=func_info["button2_y"])
        
        self.var = BooleanVar(self.master)
        check = Checkbutton(self.master, text=func_info["check"], variable=self.var, command=self.image_base)
        check.place(x=func_info["check_x"], y=func_info["check_y"])
        
        for name in self.file.keys():
            self.listbox.insert(END, name)
    
    # 言語を変更する
    def language_change(self, language):
        if language == self.language:
            pass
        else:
            self.master.destroy()
            self.settings["language"] = language
            with open(self.json_name, "w", encoding="utf-8") as f:
                    json.dump(self.settings, f, indent=2, ensure_ascii=False)
            main()
    
    # 新しく壁紙を追加する
    def select_file(self):
        # select_fileを終了する
        def this_destroy(e = None):
            if entry.get() not in self.file.keys():
                self.file[entry.get()] = filename
                self.settings["wall_paper"] = self.file
                with open(self.json_name, "w", encoding="utf-8") as f:
                    json.dump(self.settings, f, indent=2, ensure_ascii=False)
                self.listbox.insert(END, entry.get())
                select_frame.destroy()
            else:
                messagebox.showerror(func_info["e_title"], func_info["e_text"])
        
        func_info = self.settings[self.language]["select_file"]
        filename = filedialog.askopenfilename(filetypes=[("Available file", ".png .jpg .jpeg .bmp .dib .tiff .wdp"), ("PNG", ".png"), ("JPEG", ".jpg .jpeg"), ("BITMAP", ".bmp .dib"), ("TIFF", ".tiff"), ("WDP", ".wdp")])
        if filename == "":
            return
        select_frame = Toplevel(self)
        select_frame.title(func_info["title"])
        select_frame.geometry(func_info["geometry"])
        select_frame.grab_set()
        select_frame.focus_set()
        select_frame.transient(self.master)
        
        label = Label(select_frame, text=func_info["label"])
        label.place(x=func_info["label_x"], y=func_info["label_y"])
        entry = Entry(select_frame)
        entry.insert(END, filename.split("/")[-1])
        entry.place(x=func_info["entry_x"], y=func_info["entry_y"])
        entry.bind("<Return>", this_destroy)
        button = Button(select_frame, text=func_info["button"], command=this_destroy)
        button.place(x=func_info["button_x"], y=func_info["button_y"])
    
    # 壁紙を入れ替える
    def swap(self):
        def this_destroy():
            k = [*self.file.keys()]
            v = [*self.file.values()]
            num = [k.index(combo1.get()), k.index(combo2.get())]
            if num[0] == num[1]:
                messagebox.showerror(func_info["e_title"], func_info["e_text"])
            else:
                k[num[0]], k[num[1]] = k[num[1]], k[num[0]]
                v[num[0]], v[num[1]] = v[num[1]], v[num[0]]
                self.file = {i:j for i, j in zip(k, v)}
                self.listbox.delete(0, END)
                for name in self.file.keys():
                    self.listbox.insert(END, name)
                self.settings["wall_paper"] = self.file
                with open(self.json_name, "w", encoding="utf-8") as f:
                    json.dump(self.settings, f, indent=2, ensure_ascii=False)
                swap_frame.destroy()
        if len(self.file) < 2:
            pass
        else:
            func_info = self.settings[self.language]["swap"]
            swap_frame = Toplevel(self)
            swap_frame.title(func_info["title"])
            swap_frame.geometry(func_info["geometry"])
            swap_frame.resizable(False, False)
            swap_frame.grab_set()
            swap_frame.focus_set()
            swap_frame.transient(self.master)
            
            label = Label(swap_frame, text=func_info["label"])
            label.place(x=func_info["label_x"], y=func_info["label_y"])
            combo1 = ttk.Combobox(swap_frame, state="readonly", values=[*self.file.keys()])
            combo1.current(0)
            combo1.place(x=func_info["combo1_x"], y=func_info["combo1_y"])
            combo2 = ttk.Combobox(swap_frame, state="readonly", values=[*self.file.keys()])
            combo2.current(1)
            combo2.place(x=func_info["combo2_x"], y=func_info["combo2_y"])
            button = Button(swap_frame, text=func_info["button"], command=this_destroy)
            button.place(x=func_info["button_x"], y=func_info["button_y"])
    
    # 画像表示の土台
    def image_base(self):
        if self.var.get():
            func_info = self.settings[self.language]["image_base"]
            self.base_frame = Toplevel(self)
            self.base_frame.title(func_info["title"])
            self.base_frame.geometry(func_info["geometry"])
            self.base_frame.resizable(False, False)
            self.base_frame.transient(self.master)
            self.base_frame.protocol("WM_DELETE_WINDOW", (lambda: "pass")())
            self.base_frame.focus_set()
            
            self.image_canvas = Canvas(self.base_frame, width=384, height=216, bg="skyblue")
            self.image_canvas.pack()
            self.image_canvas.create_text(192, 108, text=func_info["canvas_text"], font=("", func_info["font"]))
        else:
            self.base_frame.destroy()
    
    # 画像を確認できる
    def image_show(self, event):
        if self.var.get():
            try:
                image_path = self.file[event.widget.get(event.widget.curselection())]
            except:
                return
            self.img = Image.open(image_path)
            self.img = self.img.resize((384, 216))
            self.img = ImageTk.PhotoImage(self.img)
            self.image_canvas.create_image(192, 108, image=self.img)
            self.image_canvas.update()
        else:
            pass
    
    # Back Spaceを押下した時のイベント
    # 壁紙を削除する
    def delete(self, event):
        self.file.pop(event.widget.get(event.widget.curselection()))
        event.widget.delete(event.widget.curselection())
        self.settings["wall_paper"] = self.file
        with open(self.json_name, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)

    # Enterを押下した時のイベント
    # 壁紙を変更する
    def change(self, event):
        func_info = self.settings[self.language]["change"]
        image_path = self.file[event.widget.get(event.widget.curselection())]
        if os.path.isfile(image_path):
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            self.master.destroy()
        else:
            messagebox.showerror(func_info["e_title"], func_info["e_text"])
    

def main():
    root = Tk()
    app = WallpaperChange(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()