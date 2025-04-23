import os
from tkinter import Tk, messagebox, Label, Text, Entry, Button, GROOVE, END, StringVar, OptionMenu
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import ollama
from pypdf import PdfReader

filename = ""

def basla():
    prompt = ent1.get()

    if len(prompt) == 0:
        messagebox.showwarning("Uyari", "Lütfen prompt giriniz.")
        return
    
    if filename != "":
        metin = ""
        if filename.endswith(".pdf"):
            reader = PdfReader(filename)
            for sayfa in range(len(reader.pages)):
                page = reader.pages[sayfa]
                metin += page.extract_text()
                metin += "\n"
    
        else:
            try:
                with open(filename,"r") as file:
                    metin = file.read()
            except:
                messagebox.showwarning("Uyari", "Dosya okunamadı farklı formatta dosya deneyiniz.")

        prompt += "\n" + metin

    if prompt == "clear" or prompt == "Clear" or prompt == "CLEAR":
        answer.delete("1.0", END)
        ent1.delete(0, "end")

    else:
        answer.delete("1.0", END)
        role = ent2.get()

        if len(role) == 0:
            messagebox.showwarning("Uyari", "Lütfen rolünüzü giriniz.")

        model = label_option.get()
        message = {'role': role, 'content': prompt}
        response = ollama.chat(model=model, messages=[message])
        response = response['message']['content']
        answer.insert(END, response)

def dosyasec():
    global filename

    filename = askopenfilename()

def cikis():
    model = label_option.get()
    os.system(f"ollama stop {model}")
    main.destroy()

main = Tk()
main.title("Ollama")
main.geometry(f"{main.winfo_screenwidth() - 50}x{main.winfo_screenheight() - 50}")
main.resizable(True, True)
main.bind("<Escape>", lambda event: cikis())
main.bind("<Return>", lambda event: basla())

if not(os.path.exists("models.txt")):
    os.system("ollama list > models.txt")

models = pd.read_fwf("models.txt")
models = models["NAME"].to_list()

Label(main, text="Lütfen model seciniz: ").place(x=40, y=10)
label_option = StringVar(main)
label_open_menu = OptionMenu(main, label_option, *models).place(x=200, y=10)
label_option.set(models[0])

Label(main, text="Lütfen role giriniz: ").place(x=400, y=10)

ent2 = Entry(main, width=20)
ent2.place(x=550, y=10)

Button(
    main,
    text="Dosya seçebilirsiniz",
    padx=5,
    pady=5,
    bd=5,
    activebackground="yellow",
    relief=GROOVE,
    command=dosyasec,
).place(x=900, y=5)

Label(main, text="Lütfen Prompt giriniz: ").place(x=40, y=50)

ent1 = Entry(main, width=120)
ent1.place(x=200, y=50)


Button(
    main,
    text="Cevapla",
    padx=5,
    pady=5,
    bd=5,
    activebackground="yellow",
    relief=GROOVE,
    command=basla,
).place(x=main.winfo_screenwidth() - 150, y=20)


Label(main, text="Cevap: ").place(x=50, y=80)
answer = Text(main, width=150, height=34)
answer.place(x=50, y=100)

main.mainloop()