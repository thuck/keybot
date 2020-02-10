from tkinter import Tk
from tkinter import simpledialog
from tkinter import messagebox
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify


def get_pin(title):
    root = Tk()
    root.withdraw()
    pin = simpledialog.askstring(title, 'Enter pin', show='*')
    root.destroy()
    root.quit()

    return pin

def show_error(result):
    Notify.init("skm")
    Notify.Notification.new("Error", result).show()
