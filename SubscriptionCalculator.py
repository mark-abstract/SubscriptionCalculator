import os
import sys

# When running as a bundled app, set Tcl/Tk library paths
if getattr(sys, "frozen", False):
    # Get the path to the Resources folder inside the app bundle
    resources = os.path.join(os.path.dirname(sys.executable), "..", "Resources")
    os.environ["TCL_LIBRARY"] = os.path.join(resources, "tcl")
    os.environ["TK_LIBRARY"] = os.path.join(resources, "tk")

import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.font as tkfont
import csv

# --- Helper Functions ---

def parse_currency(value: str) -> float:
    """Remove any dollar signs and commas, then convert to float."""
    cleaned = value.replace("$", "").replace(",", "").strip()
    return float(cleaned) if cleaned else 0.0

def format_currency(value: float) -> str:
    """Format a number as USD currency."""
    return f"${value:,.2f}"

def clear_placeholder(event):
    """Clear the field if its current value is the placeholder '$0.00'."""
    if event.widget.get() == "$0.00":
        event.widget.delete(0, tk.END)

# --- Automatic Calculation Section (Read-Only) ---

def generate_auto_table():
    """Generate a read-only automatic table with Total and Average columns."""
    for widget in auto_table_frame.winfo_children():
        widget.destroy()
    
    try:
        base_value = parse_currency(auto_base_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid base subscription amount.")
        return
    try:
        start_pct = float(auto_start_pct_entry.get())
        end_pct = float(auto_end_pct_entry.get())
        step_pct = float(auto_step_pct_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid percentage fields.")
        return
    try:
        num_years = int(auto_years_entry.get())
        if num_years < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid number of years.")
        return
    if start_pct > end_pct:
        messagebox.showerror("Invalid Input", "Start percent must be ≤ end percent.")
        return
    if step_pct <= 0:
        messagebox.showerror("Invalid Input", "Step percent must be > 0.")
        return

    # Create header row.
    headers = (["Percent Increase"] +
               [f"Year {i}" for i in range(1, num_years + 1)] +
               ["Total", "Average"])
    for col, header in enumerate(headers):
        if header in ("Total", "Average"):
            lbl = tk.Label(auto_table_frame, text=header, borderwidth=1, relief="solid", width=15, font=bold_font)
        else:
            lbl = tk.Label(auto_table_frame, text=header, borderwidth=1, relief="solid", width=15)
        lbl.grid(row=0, column=col, padx=1, pady=1, sticky="nsew")
    
    row_index = 0
    current_pct = start_pct
    while current_pct <= end_pct + 1e-6:
        row_index += 1
        pct_str = f"{current_pct:.2f}%"
        # Calculate yearly values.
        values = []
        total = 0.0
        for year in range(1, num_years + 1):
            val = base_value * ((1 + current_pct / 100) ** year)
            values.append(format_currency(val))
            total += val
        average = total / num_years if num_years > 0 else 0.0
        total_str = format_currency(total)
        avg_str = format_currency(average)
        
        # Create row labels.
        lbl_pct = tk.Label(auto_table_frame, text=pct_str, borderwidth=1, relief="solid", width=15)
        lbl_pct.grid(row=row_index, column=0, padx=1, pady=1, sticky="nsew")
        for i, val in enumerate(values, start=1):
            lbl_val = tk.Label(auto_table_frame, text=val, borderwidth=1, relief="solid", width=15)
            lbl_val.grid(row=row_index, column=i, padx=1, pady=1, sticky="nsew")
        lbl_total = tk.Label(auto_table_frame, text=total_str, borderwidth=1, relief="solid", width=15, font=bold_font)
        lbl_total.grid(row=row_index, column=num_years + 1, padx=1, pady=1, sticky="nsew")
        lbl_avg = tk.Label(auto_table_frame, text=avg_str, borderwidth=1, relief="solid", width=15, font=bold_font)
        lbl_avg.grid(row=row_index, column=num_years + 2, padx=1, pady=1, sticky="nsew")
        
        current_pct += step_pct

# --- Manual Entry Section ---

manual_rows = []  # List of dicts for each manual row.
manual_total_label = None
manual_avg_label = None

def generate_manual_table():
    """Generate a manual entry table with one row per year plus Total and Average rows."""
    global manual_total_label, manual_avg_label
    for widget in manual_table_frame.winfo_children():
        widget.destroy()
    manual_rows.clear()
    manual_total_label = None
    manual_avg_label = None
    
    try:
        num_years = int(auto_years_entry.get())
        if num_years < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid number of years.")
        return
    
    headers = ["Year", "Subscription Value", "Percent Change"]
    for col, header in enumerate(headers):
        lbl = tk.Label(manual_table_frame, text=header, borderwidth=1, relief="solid", width=20)
        lbl.grid(row=0, column=col, padx=1, pady=1, sticky="nsew")
    
    for i in range(num_years):
        row_data = {}
        year_lbl = tk.Label(manual_table_frame, text=f"Year {i+1}", borderwidth=1, relief="solid", width=20)
        year_lbl.grid(row=i+1, column=0, padx=1, pady=1, sticky="nsew")
        row_data["year_label"] = year_lbl
        
        val_entry = tk.Entry(manual_table_frame, width=20, justify="center")
        val_entry.insert(0, "$0.00")
        val_entry.bind("<FocusIn>", clear_placeholder)
        val_entry.grid(row=i+1, column=1, padx=1, pady=1, sticky="nsew")
        val_entry.bind("<FocusOut>", lambda event: update_manual_table())
        row_data["value_entry"] = val_entry
        
        pct_lbl = tk.Label(manual_table_frame, text="", borderwidth=1, relief="solid", width=20)
        pct_lbl.grid(row=i+1, column=2, padx=1, pady=1, sticky="nsew")
        row_data["percent_label"] = pct_lbl
        
        manual_rows.append(row_data)
    
    total_row_index = num_years + 1
    avg_row_index = num_years + 2
    
    total_lbl = tk.Label(manual_table_frame, text="Total", borderwidth=1, relief="solid", width=20, font=bold_font)
    total_lbl.grid(row=total_row_index, column=0, padx=1, pady=1, sticky="nsew")
    total_value = tk.Label(manual_table_frame, text="", borderwidth=1, relief="solid", width=20, font=bold_font)
    total_value.grid(row=total_row_index, column=1, padx=1, pady=1, sticky="nsew")
    total_pct = tk.Label(manual_table_frame, text="", borderwidth=1, relief="solid", width=20, font=bold_font)
    total_pct.grid(row=total_row_index, column=2, padx=1, pady=1, sticky="nsew")
    
    avg_lbl = tk.Label(manual_table_frame, text="Average", borderwidth=1, relief="solid", width=20, font=bold_font)
    avg_lbl.grid(row=avg_row_index, column=0, padx=1, pady=1, sticky="nsew")
    avg_value = tk.Label(manual_table_frame, text="", borderwidth=1, relief="solid", width=20, font=bold_font)
    avg_value.grid(row=avg_row_index, column=1, padx=1, pady=1, sticky="nsew")
    avg_pct = tk.Label(manual_table_frame, text="", borderwidth=1, relief="solid", width=20, font=bold_font)
    avg_pct.grid(row=avg_row_index, column=2, padx=1, pady=1, sticky="nsew")
    
    manual_total_label = total_value
    manual_avg_label = avg_value
    
    update_manual_table()

def update_manual_table():
    """Update the Percent Change column for manual rows and compute Total and Average."""
    try:
        base_value = parse_currency(auto_base_entry.get())
    except ValueError:
        base_value = None
    
    for i, row in enumerate(manual_rows):
        try:
            current_value = parse_currency(row["value_entry"].get())
        except ValueError:
            current_value = None
        
        if i == 0:
            if current_value is not None and base_value and base_value != 0:
                pct = (current_value / base_value - 1) * 100
                row["percent_label"].config(text=f"{pct:.2f}%")
            else:
                row["percent_label"].config(text="")
        else:
            try:
                prev_value = parse_currency(manual_rows[i-1]["value_entry"].get())
            except ValueError:
                prev_value = None
            if current_value is not None and prev_value not in (None, 0):
                pct = (current_value / prev_value - 1) * 100
                row["percent_label"].config(text=f"{pct:.2f}%")
            else:
                row["percent_label"].config(text="")
    
    total = 0.0
    count = 0
    for row in manual_rows:
        try:
            val = parse_currency(row["value_entry"].get())
            total += val
            count += 1
        except:
            continue
    average = total / count if count > 0 else 0.0
    if manual_total_label:
        manual_total_label.config(text=format_currency(total))
    if manual_avg_label:
        manual_avg_label.config(text=format_currency(average))

# --- Download CSV (Both Tables) ---

def download_csv():
    """Open a file-save dialog (defaulting to 'increase.csv') and save both tables to CSV."""
    file_path = filedialog.asksaveasfilename(
        initialfile="increase.csv",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save CSV File"
    )
    if not file_path:
        return
    
    try:
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Automatic Calculation Table"])
            try:
                num_years = int(auto_years_entry.get())
            except ValueError:
                num_years = 0
            auto_header = (["Percent Increase"] +
                           [f"Year {i}" for i in range(1, num_years+1)] +
                           ["Total", "Average"])
            writer.writerow(auto_header)
            # Get rows based on grid_info.
            rows = []
            grid_info = auto_table_frame.grid_slaves()
            # grid_slaves returns widgets in reverse order; so we sort them by row and column.
            widget_positions = []
            for w in grid_info:
                info = w.grid_info()
                widget_positions.append((int(info["row"]), int(info["column"]), w))
            widget_positions.sort(key=lambda x: (x[0], x[1]))
            # Determine number of rows and columns from header.
            num_cols = len(auto_header)
            max_row = max([r for r, c, w in widget_positions])
            for r in range(0, max_row+1):
                row_values = []
                for c in range(num_cols):
                    # Find widget with matching row and column.
                    for rpos, cpos, w in widget_positions:
                        if rpos == r and cpos == c:
                            row_values.append(w.cget("text"))
                            break
                    else:
                        row_values.append("")
                rows.append(row_values)
            for row in rows:
                writer.writerow(row)
            writer.writerow([])  # Blank row.
            
            writer.writerow(["Manual Entry Table"])
            writer.writerow(["Year", "Subscription Value", "Percent Change"])
            for row in manual_rows:
                year = row["year_label"].cget("text")
                value = row["value_entry"].get()
                pct = row["percent_label"].cget("text")
                writer.writerow([year, value, pct])
            writer.writerow(["Total", manual_total_label.cget("text"), ""])
            writer.writerow(["Average", manual_avg_label.cget("text"), ""])
        messagebox.showinfo("CSV Downloaded", f"CSV file saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save CSV: {e}")

# --- Cancel Button Function ---

def cancel_app():
    """Cancel and close the application."""
    root.destroy()

# --- Main Window Setup ---

root = tk.Tk()
root.title("Subscription Cost Increase Calculator")
root.geometry("800x600")
root.minsize(600, 400)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a bold font for totals and averages.
default_font = tkfont.nametofont("TkDefaultFont")
bold_font = tkfont.Font(root, family=default_font.cget("family"), size=default_font.cget("size"), weight="bold")

# Settings Frame.
settings_frame = tk.LabelFrame(root, text="Settings", padx=10, pady=10)
settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

tk.Label(settings_frame, text="Last Period Subscription Amount:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
auto_base_entry = tk.Entry(settings_frame)
auto_base_entry.grid(row=0, column=1, padx=5, pady=5)
auto_base_entry.insert(0, "$0.00")
auto_base_entry.bind("<FocusIn>", clear_placeholder)

tk.Label(settings_frame, text="Start Percentage Increase (%):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
auto_start_pct_entry = tk.Entry(settings_frame)
auto_start_pct_entry.grid(row=1, column=1, padx=5, pady=5)
auto_start_pct_entry.insert(0, "0.5")

tk.Label(settings_frame, text="End Percentage Increase (%):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
auto_end_pct_entry = tk.Entry(settings_frame)
auto_end_pct_entry.grid(row=2, column=1, padx=5, pady=5)
auto_end_pct_entry.insert(0, "3.0")

tk.Label(settings_frame, text="Step Percentage Increase (%):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
auto_step_pct_entry = tk.Entry(settings_frame)
auto_step_pct_entry.grid(row=3, column=1, padx=5, pady=5)
auto_step_pct_entry.insert(0, "0.5")

tk.Label(settings_frame, text="Number of Years:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
auto_years_entry = tk.Entry(settings_frame)
auto_years_entry.grid(row=4, column=1, padx=5, pady=5)
auto_years_entry.insert(0, "3")

# Automatic Calculation Section with Scrollable Canvas (Read-Only).
auto_calc_frame = tk.LabelFrame(root, text="Automatic Calculation (Read-Only)", padx=10, pady=10)
auto_calc_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
auto_calc_frame.grid_rowconfigure(1, weight=1)
auto_calc_frame.grid_columnconfigure(0, weight=1)

gen_auto_btn = tk.Button(auto_calc_frame, text="Generate Automatic Table", command=generate_auto_table)
gen_auto_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

auto_container = tk.Frame(auto_calc_frame)
auto_container.grid(row=1, column=0, sticky="nsew")
auto_container.grid_rowconfigure(0, weight=1)
auto_container.grid_columnconfigure(0, weight=1)

auto_canvas = tk.Canvas(auto_container)
auto_canvas.grid(row=0, column=0, sticky="nsew")

auto_vscrollbar = tk.Scrollbar(auto_container, orient="vertical", command=auto_canvas.yview)
auto_vscrollbar.grid(row=0, column=1, sticky="ns")

auto_hscrollbar = tk.Scrollbar(auto_container, orient="horizontal", command=auto_canvas.xview)
auto_hscrollbar.grid(row=1, column=0, columnspan=2, sticky="ew")

auto_canvas.configure(yscrollcommand=auto_vscrollbar.set, xscrollcommand=auto_hscrollbar.set)

auto_table_frame = tk.Frame(auto_canvas)
auto_canvas.create_window((0, 0), window=auto_table_frame, anchor="nw")

def on_auto_frame_configure(event):
    auto_canvas.configure(scrollregion=auto_canvas.bbox("all"))
    bbox = auto_canvas.bbox("all")
    if bbox:
        content_width = bbox[2] - bbox[0]
        content_height = bbox[3] - bbox[1]
        canvas_width = auto_canvas.winfo_width()
        canvas_height = auto_canvas.winfo_height()
        if content_height > canvas_height:
            auto_vscrollbar.grid()
        else:
            auto_vscrollbar.grid_remove()
        if content_width > canvas_width:
            auto_hscrollbar.grid()
        else:
            auto_hscrollbar.grid_remove()
auto_table_frame.bind("<Configure>", on_auto_frame_configure)

# Manual Entry Section.
manual_frame = tk.LabelFrame(root, text="Manual Entry", padx=10, pady=10)
manual_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
manual_frame.grid_rowconfigure(0, weight=1)
manual_frame.grid_columnconfigure(0, weight=1)

gen_manual_btn = tk.Button(manual_frame, text="Generate Manual Table", command=generate_manual_table)
gen_manual_btn.pack(pady=5)

manual_table_frame = tk.Frame(manual_frame)
manual_table_frame.pack(fill="both", expand=True, padx=5, pady=5)

# Bottom Buttons Frame with Footnote.
bottom_frame = tk.Frame(root, padx=10, pady=10)
bottom_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
bottom_frame.grid_columnconfigure(0, weight=1)

footnote_label = tk.Label(bottom_frame, text="© 2025 Mark Wesolowski")
footnote_label.grid(row=0, column=0, sticky="w")

button_frame = tk.Frame(bottom_frame)
button_frame.grid(row=0, column=1, sticky="e")
download_btn = tk.Button(button_frame, text="Download CSV", command=download_csv)
download_btn.pack(side="left", padx=5)
cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_app)
cancel_btn.pack(side="left", padx=5)

root.mainloop()