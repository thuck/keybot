from tkinter import Tk
from tkinter import simpledialog
from tkinter import messagebox
import gi

gi.require_version("Notify", "0.7")
from gi.repository import Notify


class GUI:
    def __init__(self):
        Notify.init("keybot")

    def get_pin(self, title):
        root = Tk()
        root.withdraw()
        pin = simpledialog.askstring(title, "Enter pin", show="*")
        root.destroy()
        root.quit()

        return pin

    def show_error(self, result):
        Notify.Notification.new("Error", result).show()
