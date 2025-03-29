import ctypes
import json
import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import ImageTk, Image

class WallpaperChange(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        
        self.file = {}
        try:
            with open("wallpaper_list.json", "r", encoding="utf-8") as f:
                self.file = json.load(f)
        except:
            pass
        
        self.master.geometry("200x280")
        self.master.title("wallpaper change")
        self.master.resizable(False, False)
        self.create_widget()
    
    # ウィジェットの作成
    def create_widget(self):
        self.listbox = Listbox(self.master, height=15, width=31, selectmode="single", takefocus=0)
        self.listbox.place(x=5, y=5)
        self.listbox.bind("<Return>", self.change)
        self.listbox.bind("<BackSpace>", self.delete)
        self.listbox.bind("<ButtonRelease-1>", self.image_show)
        
        button = Button(self.master, text="壁紙追加", command=self.select_file)
        button.place(x=140, y=252)
        
        button = Button(self.master, text="入れ替え", command=self.swap)
        button.place(x=80, y=252)
        
        self.var = BooleanVar(self.master)
        check = Checkbutton(self.master, text="画像確認", variable=self.var, command=self.image_base)
        check.place(x=5, y=252)
        
        for name in self.file.keys():
            self.listbox.insert(END, name)
    
    # 新しく壁紙を追加する
    def select_file(self):
        # select_fileを終了する
        def this_destroy():
            if entry.get() not in self.file.keys():
                self.file[entry.get()] = filename
                with open("wallpaper_list.json", "w", encoding="utf-8") as f:
                    json.dump(self.file, f, indent=2, ensure_ascii=False)
                self.listbox.insert(END, entry.get())
                select_frame.destroy()
            else:
                messagebox.showerror("エラー", "この名前はすでに使用されています")
        
        filename = filedialog.askopenfilename(filetypes=[("Available file", ".png .jpg .jpeg .bmp .dib .tiff .wdp"), ("PNG", ".png"), ("JPEG", ".jpg .jpeg"), ("BITMAP", ".bmp .dib"), ("TIFF", ".tiff"), ("WDP", ".wdp")])
        if filename == "":
            return
        select_frame = Toplevel(self)
        select_frame.title("選択")
        select_frame.geometry("200x100")
        select_frame.grab_set()
        select_frame.focus_set()
        select_frame.transient(self.master)
        
        label = Label(select_frame, text="表示時のニックネームを決めてください")
        label.place(x=10, y=10)
        entry = Entry(select_frame)
        entry.insert(END, filename.split("/")[-1])
        entry.place(x=12, y=32)
        button = Button(select_frame, text="決定", command=this_destroy)
        button.place(x=160, y=30)
    
    # 壁紙を入れ替える
    def swap(self):
        def this_destroy():
            k = [*self.file.keys()]
            v = [*self.file.values()]
            num = [k.index(combo1.get()), k.index(combo2.get())]
            if num[0] == num[1]:
                messagebox.showerror("エラー", "同じ壁紙は選択できません\nもう一度選びなおしてください")
            else:
                k[num[0]], k[num[1]] = k[num[1]], k[num[0]]
                v[num[0]], v[num[1]] = v[num[1]], v[num[0]]
                self.file = {i:j for i, j in zip(k, v)}
                self.listbox.delete(0, END)
                for name in self.file.keys():
                    self.listbox.insert(END, name)
                with open("wallpaper_list.json", "w", encoding="utf-8") as f:
                    json.dump(self.file, f, indent=2, ensure_ascii=False)
                swap_frame.destroy()
        if len(self.file) < 2:
            pass
        else:
            swap_frame = Toplevel(self)
            swap_frame.title("交換")
            swap_frame.geometry("190x85")
            swap_frame.resizable(False, False)
            swap_frame.grab_set()
            swap_frame.focus_set()
            swap_frame.transient(self.master)
            
            label = Label(swap_frame, text="入れ替える壁紙を選択してください")
            label.place(x=5, y=5)
            combo1 = ttk.Combobox(swap_frame, state="readonly", values=[*self.file.keys()])
            combo1.current(0)
            combo1.place(x=5, y=30)
            combo2 = ttk.Combobox(swap_frame, state="readonly", values=[*self.file.keys()])
            combo2.current(1)
            combo2.place(x=5, y=55)
            button = Button(swap_frame, text="決定", command=this_destroy)
            button.place(x=151, y=52)
    
    # 画像表示の土台
    def image_base(self):
        if self.var.get():
            self.base_frame = Toplevel(self)
            self.base_frame.title("画像表示")
            self.base_frame.geometry("384x216")
            self.base_frame.resizable(False, False)
            self.base_frame.transient(self.master)
            self.base_frame.protocol("WM_DELETE_WINDOW", (lambda: "pass")())
            self.base_frame.focus_set()
            
            self.image_canvas = Canvas(self.base_frame, width=384, height=216, bg="skyblue")
            self.image_canvas.pack()
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
        with open("wallpaper_list.json", "w", encoding="utf-8") as f:
            json.dump(self.file, f, indent=2, ensure_ascii=False)

    # Enterを押下した時のイベント
    # 壁紙を変更する
    def change(self, event):
        image_path = self.file[event.widget.get(event.widget.curselection())]
        if os.path.isfile(image_path):
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            self.master.destroy()
        else:
            messagebox.showerror("エラー", "対象ファイルが存在しないか参照出来ません。\n一度削除してもう一度壁紙を設定し直してください")

def main():
    root = Tk()
    app = WallpaperChange(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()