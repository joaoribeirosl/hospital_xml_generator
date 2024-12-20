import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox

MAX_NUM_KITS = 5

def submit_kits():
    icu_kits = icu_entry.get()
    emergency_kits = emergency_entry.get()
    pediatrics_kits = pediatrics_entry.get()
    
    if not icu_kits or not emergency_kits or not pediatrics_kits:
        messagebox.showwarning("Warning", "Must fill all fields!")
        return
    
    if (int(icu_kits) + int(emergency_kits) + int(pediatrics_kits)) > MAX_NUM_KITS:
        messagebox.showwarning("Warning", f"Maximum number of kits cannot exceed {MAX_NUM_KITS}!")
        return
        
    try:
        kits = [int(icu_kits), int(emergency_kits), int(pediatrics_kits)]
    except ValueError:
        messagebox.showerror("Error", "Insert numbers only!")
        return

    messagebox.showinfo("Success", f"Kits to be mounted: {kits}")
    print(f"Kits: {kits}")  
    update_uppaal_model(input_file, output_file, kits)
    root.destroy()
    

def update_uppaal_model(input_xml, output_xml, kit_map_values):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    for declaration in root.findall(".//declaration"):
        text = declaration.text

        if "kit_map" in text:
            new_kit_map = f"kit_map[3] = {{{','.join(map(str, kit_map_values))}}};"
            text = text.replace(
                "kit_map[3] = {1,1,1};",  # change to kit_map[3];
                new_kit_map
            )
        declaration.text = text

    tree.write(output_xml, encoding="utf-8", xml_declaration=True)

def create_ui():
    global icu_entry, emergency_entry, pediatrics_entry

    tk.Label(root, text="Inform kits for each sector").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(root, text="UTI:").grid(row=1, column=0, sticky="e")
    icu_entry = tk.Entry(root)
    icu_entry.grid(row=1, column=1)

    tk.Label(root, text="Emergency:").grid(row=2, column=0, sticky="e")
    emergency_entry = tk.Entry(root)
    emergency_entry.grid(row=2, column=1)

    tk.Label(root, text="Pediatrics:").grid(row=3, column=0, sticky="e")
    pediatrics_entry = tk.Entry(root)
    pediatrics_entry.grid(row=3, column=1)

    submit_button = tk.Button(root, text="Confirm", command=submit_kits)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    input_file = "hcl_example.xml" #put yours
    output_file = "hcl_updated.xml"

    root = tk.Tk()
    root.title("Seleção de Kits")
    root.geometry('300x150')
    create_ui()
    root.mainloop()
