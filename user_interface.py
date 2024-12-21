import xml.etree.ElementTree as ET
from tkinter import messagebox, filedialog
import tkinter as tk
import argparse
import os



MAX_NUM_KITS = 5
generated_xml = False

def validate_kits(icu_kits, emergency_kits, pediatrics_kits):
    """
    Validates the user input for kit selection.
    """
    if not icu_kits or not emergency_kits or not pediatrics_kits:
        messagebox.showwarning("Warning", "Must fill all fields!")
        return False

    try:
        kits = [int(icu_kits), int(emergency_kits), int(pediatrics_kits)]
    except ValueError:
        messagebox.showerror("Error", "Insert numbers only!")
        return False

    if sum(kits) > MAX_NUM_KITS:
        messagebox.showwarning("Warning", f"Maximum number of kits cannot exceed {MAX_NUM_KITS}!")
        return False

    return kits

def submit_kits():
    """
    Handles user input and calls update_uppaal_model to generate a new XML.
    """
    global generated_xml

    icu_kits = icu_entry.get()
    emergency_kits = emergency_entry.get()
    pediatrics_kits = pediatrics_entry.get()
    
    kits = validate_kits(icu_kits, emergency_kits, pediatrics_kits)
    if not kits:
        return

    messagebox.showinfo("Success", f"Kits to be mounted: {kits}")
    print(f"Kits: {kits}")  
    update_uppaal_model(args.input_file, args.output_file, kits)
    submit_button.config(state=tk.DISABLED)
    download_button.config(state=tk.NORMAL)
    generated_xml = True
    messagebox.showinfo("Success", "XML updated successfully! Click 'Download' to save this XML and use in UPPAAL.")

def update_uppaal_model(input_xml, output_xml, kit_map_values):
    """
    Receive a xml then generate a new xml with kit_map_values passed.
    """
    tree = ET.parse(input_xml)
    root = tree.getroot()

    for declaration in root.findall(".//declaration"):
        text = declaration.text

        if "kit_map" in text:
            new_kit_map = f"kit_map[3] = {{{','.join(map(str, kit_map_values))}}};"
            text = text.replace(
                "kit_map[3];",
                new_kit_map
            )
        declaration.text = text
    tree.write(output_xml, encoding="utf-8", xml_declaration=True)

def create_ui():
    """
    Create user interface.
    """    
    global icu_entry, emergency_entry, pediatrics_entry, download_button, submit_button

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
    submit_button.grid(row=4, column=0, columnspan=2, pady=5)

    download_button = tk.Button(root, text="Download", command=download_xml, state=tk.DISABLED)
    download_button.grid(row=4, column=1, columnspan=2, pady=5, padx=100)

def bind_submit_event():
    """
    Binds the Enter key to the submit function.
    """
    root.bind("<Return>", lambda event: submit_kits() if not generated_xml else '')

def download_xml():
    """
    Download xml generated.
    """    
    save_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
    if save_path:
        with open(args.output_file, "r") as file:
            content = file.read()
        with open(save_path, "w") as file:
            file.write(content)
        messagebox.showinfo("Success", f"XML saved to {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI for selecting kits for UPPAAL automation.")
    parser.add_argument("input_file", help="Path to the input XML file.")
    parser.add_argument("-o", "--output_file", default="updated_automaton.xml",
                        help="Path to save the updated XML file. Default is 'updated_automaton.xml'.")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        exit(1)

    root = tk.Tk()
    root.title("Seleção de Kits")
    root.geometry('300x200')

    create_ui()
    bind_submit_event()
    root.mainloop()
