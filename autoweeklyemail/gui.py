import tkinter as tk
import webbrowser
import traceback
import utils

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.error_messages = tk.Label(self, text="If there is an error message it will show up here")
        self.error_messages.pack(side="bottom")

        self.make_email = tk.Button(self, text="Generate Weekly Email", fg="red",
                                    command=self.generate_email)
        self.make_email.pack(side="bottom")

    def generate_email(self):
        try:
            webbrowser.open("file://" + utils.generate_email())
        except Exception as e:
            self.error_messages["text"] = str(traceback.format_exc())
            self.error_messages["font"] = ("Courier", 13)
            raise e


def show_gui():
    root = tk.Tk()
    root.title("Weekly Email Generator")
    root.minsize()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    show_gui()
