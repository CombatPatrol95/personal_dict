import tkinter as tk
from database_connect import *
from tkinter import IntVar
import pyglet
import os

pyglet.font.add_file('fonts/GOTHICB.TTF')
# pyglet.font.add_file('fonts/Base 02.ttf')

gothic = pyglet.font.load('Century Gothic')
# digital = pyglet.font.load('Digital-7 Mono')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# db_init()


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        theme_color = "#000000"
        self.geometry("800x600+150+50")
        self.title("English Dictionary")
        # self.overrideredirect(True)
        # self.attributes("-fullscreen", True)
        self.minsize(640, 400)
        # self.iconbitmap("images/cch_logo.ico")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for i in [StartPage]:
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky='nwes')

        self.showFrame(StartPage)

        # Frame for the main window bottom credit bar
        credit_frame = tk.Frame(self, bg=theme_color, relief='flat', bd=0)
        credit_frame.pack(fill='x')

        label = tk.Label(credit_frame, bg=theme_color, fg='#ffffff', text='Adidas Tri Poloski',
                         font=('Times New Roman', 12, 'italic'))
        label.pack(anchor='center')

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        theme_color = "#000000"
        self.config(bg=theme_color)
        font = ("Times New Roman", 26)
        # Frame for main title label and logo
        mainlabel_frame = tk.Frame(self, bg=theme_color, relief='flat', bd=1)
        mainlabel_frame.pack(anchor=tk.N)

        title_label = tk.Label(mainlabel_frame, text="Un Dictionnaire Anglais", font=font,
                               bg=theme_color,
                               fg='#ffffff')
        title_label.pack()

        def search(_=None):
            typed_word = search_entry.get()
            if dictionary_var.get() == 1 and len(typed_word) > 1:
                defination_box.config(state=tk.NORMAL)
                search_entry.delete(0, "end")
                defination_box.delete(1.0, tk.END)
                defination_box.insert(1.0, typed_word.capitalize() + "\n")
                defination_box.insert(2.0, "_" * 30 + "\n")
                defination_box.insert(4.0, search_word(typed_word))
                defination_box.config(state=tk.DISABLED)
        # def search(_=None):
        #     typed_word = search_entry.get()
        #     if dictionary_var.get() == 1 and len(typed_word) > 1:
        #         defination_box.config(state=tk.NORMAL)
        #         search_entry.delete(0, "end")
        #         defination_box.delete(1.0, tk.END)
        #         defination_box.insert(1.0, typed_word.capitalize() + "\n")
        #         defination_box.insert(2.0, "_" * 30 + "\n")
        #         defination_box.insert(4.0, search_word(typed_word))
        #         defination_box.config(state=tk.DISABLED)

        def insert_new(_=None):
            typed_word = insert_entry.get()
            typed_word = typed_word.split(',')
            if len(typed_word) == 6:
                insert_new_word(typed_word)
            else:
                print("Please provide all 6 fields.")
            # insert_new_word(typed_word)

            # if dictionary_var.get() == 1 and len(typed_word) > 1:
            #     defination_box.config(state=tk.NORMAL)
            #     search_entry.delete(0, "end")
            #     defination_box.delete(1.0, tk.END)
            #     defination_box.insert(1.0, typed_word.capitalize() + "\n")
            #     defination_box.insert(2.0, "_" * 30 + "\n")
            #     defination_box.insert(4.0, search_word(typed_word))
            #     defination_box.config(state=tk.DISABLED)

        def update(data_list):
            # list_box.delete(0, tk.END)
            words_list_box.delete(0, tk.END)
            # Add words to listbox
            for word_item in data_list:
                words_list_box.insert(tk.END, word_item)

        def what_selected(typed_from_keyboard):
            if typed_from_keyboard == "":
                data = []
            else:
                data = []
                for item in search_all_matching(typed_from_keyboard):
                    data.append(item)
                update(data)

        def check(_=None):
            # grab what is typed
            typed = search_entry.get()
            what_selected(typed)
            # self.update()

        def check_insert(_=None):
            # grab what is typed
            typed = insert_entry.get()
            insert_new_word(typed)
            # what_selected(typed)
            # self.update()

        def fill_out(_=None):
            # Delete whatever is in the entry box
            search_entry.delete(0, tk.END)

            # Add clicked list item to entry box
            search_entry.insert(0, words_list_box.get("anchor"))
            search(words_list_box.get("anchor"))

        search_widget_frame = tk.Frame(self, bg=theme_color)
        search_widget_frame.pack(anchor=tk.N)

        insert_widget_frame = tk.Frame(self, bg=theme_color)
        insert_widget_frame.pack(anchor=tk.S)

        def cut_text():
            copy_text()
            delete_text()

        def copy_text():
            selection = defination_box.tag_ranges(tk.SEL)
            if selection:
                self.clipboard_clear()
                self.clipboard_append(defination_box.get(*selection))

        def paste_text():
            defination_box.insert(tk.INSERT, self.clipboard_get())

        def paste_image():
            global img
            try:
                img = tk.PhotoImage(file=self.clipboard_get())
                position = defination_box.index(tk.INSERT)
                defination_box.image_create(position, image=img)
            except tk.TclError:
                pass

        def delete_text():
            selection = defination_box.tag_ranges(tk.SEL)
            if selection:
                defination_box.delete(*selection)

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="This is an English Dictionary")
        menu.add_command(label="Cut", command=cut_text)

        menu.add_command(label="Copy text", command=copy_text)
        menu.add_command(label="Paste text", command=paste_text)
        menu.add_command(label="Paste image", command=paste_image)
        menu.add_command(label="Delete", command=delete_text)

        def show_popup(event):
            menu.post(event.x_root, event.y_root)

        # checkbuttons_frame = tk.Frame(search_widget_frame)
        # checkbuttons_frame.pack(side=tk.LEFT)

        images = os.path.join(BASE_DIR, 'img')  # images directory path
        on_image = tk.PhotoImage(file=os.path.join(images, 'button_on.png'))
        off_image = tk.PhotoImage(file=os.path.join(images, 'button_off.png'))
        dictionary_var = IntVar()
        # dictionary_check = tk.Checkbutton(search_widget_frame, image=off_image, selectimage=on_image, indicatoron=False,
        #                                   variable=dictionary_var, onvalue=1, offvalue=0, bd=0,
        #                                   text="Dictionary", bg="#ffffff", command=check_me)
        # dictionary_check.image = (on_image, off_image)
        # dictionary_check.pack(side=tk.LEFT)
        # dictionary_check.select()

        search_text = tk.Label(search_widget_frame, bg="#ffffff", text="Search ", font=("Times New Roman", 14))
        search_text.pack(side=tk.LEFT)

        search_entry = tk.Entry(search_widget_frame, width=34, font=("Times New Roman", 18))
        search_entry.pack(pady=20, side=tk.RIGHT)
        search_entry.focus_set()
        search_entry.bind("<KeyRelease>", check)

        search_img = tk.PhotoImage(file=os.path.join(images, 'search.png'))
        search_btn = tk.Button(search_widget_frame, image=search_img, bg=theme_color, width=80,
                               activebackground='#6b5924', command=search)
        search_btn.image = search_img
        search_btn.pack(side=tk.RIGHT, padx=5)

        # below are insert new word related

        insert_text = tk.Label(insert_widget_frame, bg="#ffffff", text="New Word", font=("Times New Roman", 14))
        insert_text.pack(side=tk.LEFT)

        insert_entry = tk.Entry(insert_widget_frame, width=34, font=("Times New Roman", 18))
        insert_entry.pack(pady=20, side=tk.RIGHT)
        insert_entry.focus_set()
        insert_entry.bind("<KeyRelease>", insert_new)

        insert_img = tk.PhotoImage(file=os.path.join(images, 'search.png'))
        insert_btn = tk.Button(insert_widget_frame, image=insert_img, bg=theme_color, width=80,
                               activebackground='#6b5924', command=insert_new)
        insert_btn.image = insert_img
        insert_btn.pack(side=tk.LEFT, padx=5)
        # insert_text = tk.Label(insert_widget_frame, bg="#ffffff", text="New Word", font=("Times New Roman", 14))
        # insert_text.pack(side=tk.LEFT)
        #
        # insert_entry = tk.Entry(insert_widget_frame, width=34, font=("Times New Roman", 18))
        # insert_entry.pack(pady=20, side=tk.RIGHT)
        # insert_entry.focus_set()
        # insert_entry.bind("<KeyRelease>", check_insert)
        #
        # insert_img = tk.PhotoImage(file=os.path.join(images, 'search.png'))
        # insert_btn = tk.Button(insert_widget_frame, image=insert_img, bg=theme_color, width=80,
        #                        activebackground='#6b5924', command=insert_new)
        # insert_btn.image = search_img
        # insert_btn.pack(side=tk.LEFT, padx=5)

        defination_frame = tk.Frame(self)
        defination_frame.pack(fill=tk.BOTH, padx=10, expand=True)

        defination_box_scrbar = tk.Scrollbar(defination_frame)
        defination_box = tk.Text(defination_frame, width=40, height=20, font=("Verdana", 13),
                                 yscrollcommand=defination_box_scrbar.set)
        defination_box.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        defination_box_scrbar.pack(side=tk.LEFT, fill=tk.Y)
        defination_box_scrbar.config(command=defination_box.yview)

        words_listbox_scrbar = tk.Scrollbar(defination_frame)
        words_list_box = tk.Listbox(defination_frame, font=('Vedarna', 12), yscrollcommand=words_listbox_scrbar.set)
        words_list_box.pack(side=tk.LEFT, fill=tk.Y)
        words_listbox_scrbar.pack(side=tk.LEFT, fill=tk.Y)
        words_listbox_scrbar.config(command=words_list_box.yview)

        self.bind("<Return>", search)
        words_list_box.bind("<<ListboxSelect>>", fill_out)
        defination_box.bind("<Button-3>", show_popup)

        update(get_all_words())


app = Application()
app.mainloop()
