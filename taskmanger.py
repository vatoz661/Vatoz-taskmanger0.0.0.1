import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_CPU_usage():
    return psutil.cpu_percent()

def get_disk_usage():
    return psutil.disk_usage('/').percent

def get_running_processes():
    return [(proc.name(), proc.pid) for proc in psutil.process_iter()]

def update_ram_usage():
    ram_usage = get_ram_usage()
    ram_label.config(text=f"RAM Kullanımı: {ram_usage}%")
    ram_progressbar["value"] = ram_usage
    root.after(1000, update_ram_usage)

def update_CPU_usage():
    CPU_usage = get_CPU_usage()
    CPU_label.config(text=f"CPU Kullanımı: {CPU_usage}%")
    CPU_progressbar["value"] = CPU_usage
    root.after(1000, update_CPU_usage)

def update_disk_usage():
    disk_usage = get_disk_usage()
    disk_label.config(text=f"Disk Kullanımı: {disk_usage}%")
    root.after(1000, update_disk_usage)

def update_running_processes():
    running_processes = get_running_processes()
    process_list.delete(0, tk.END)
    for proc_name, proc_pid in running_processes:
        process_list.insert(tk.END, f"{proc_name} - PID: {proc_pid}")
        # Eğer işlem bir Windows hizmeti ise, yeşil renkte göster
        if '.exe' not in proc_name:
            process_list.itemconfig(tk.END, {'bg': 'green'})
    root.after(10000, update_running_processes)

def terminate_selected_process():
    selected_index = process_list.curselection()
    if selected_index:
        selected_pid = process_list.get(selected_index).split(" - PID: ")[1]
        # Seçilen işlemi sonlandır
        try:
            psutil.Process(int(selected_pid)).terminate()
            print(f"{selected_pid} PID'li işlem sonlandırıldı.")
        except psutil.NoSuchProcess:
            print(f"{selected_pid} PID'li işlem zaten sonlandırılmış.")
    else:
        print("Lütfen sonlandırmak istediğiniz bir işlemi seçin.")

root = tk.Tk()
root.title("görev yöneticisi")

frame = ttk.Frame(root, padding="20")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ram_label = ttk.Label(frame, text="RAM Kullanımı: ")
ram_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")

ram_progressbar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate" )
ram_progressbar.grid(column=1, row=0, padx=5, pady=5, sticky="ew")

CPU_label = ttk.Label(frame, text="CPU Kullanımı: ")
CPU_label.grid(column=0, row=1, padx=5, pady=5, sticky="w")

CPU_progressbar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate" )
CPU_progressbar.grid(column=1, row=1, padx=5, pady=5, sticky="ew")

disk_label = ttk.Label(frame, text="Disk Kullanımı: ")
disk_label.grid(column=0, row=2, padx=5, pady=5, sticky="w")

# Matplotlib figürünü oluşturma
fig = Figure(figsize=(4, 4))
ax = fig.add_subplot(111)
ax.pie([get_disk_usage(), 100-get_disk_usage()], labels=['Dolu', 'Boş'], autopct='%1.1f%%', startangle=90)
ax.set_title('Disk', fontsize=12)

# Matplotlib figürünü Tkinter penceresine entegre etme
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=1, row=2, padx=5, pady=5)

# Çalışan uygulamalar listesi
process_frame = ttk.Frame(root, padding="20")
process_frame.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))

process_label = ttk.Label(process_frame, text="Çalışan Uygulamalar: ")
process_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")

process_list = tk.Listbox(process_frame, width=88, height=10)
process_list.grid(column=0, row=1, padx=5, pady=5, sticky="ew")

# Sağ tık menüsü oluşturma
process_menu = tk.Menu(root, tearoff=0)
process_menu.add_command(label="İşlemi Sonlandır", command=terminate_selected_process)

# Liste öğesine sağ tık menüsünü bağlama
process_list.bind("<Button-3>", lambda event: process_menu.tk_popup(event.x_root, event.y_root))

update_ram_usage()
update_CPU_usage()
update_disk_usage()
update_running_processes()

root.mainloop()
