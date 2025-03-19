import os
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from PIL import Image
import gc

class KwaliteitenPage(ctk.CTkFrame):
    def __init__(self, parent, base_dir):
        super().__init__(parent, fg_color="white")
        self.base_dir = base_dir
        self.configure(fg_color="white")

        greenmark_path = os.path.join(self.base_dir, "resources", "images", "greenmark.png")
        redmark_path   = os.path.join(self.base_dir, "resources", "images", "redmark.png")

        self.img_greenmark = ctk.CTkImage(
            dark_image=Image.open(greenmark_path),
            light_image=Image.open(greenmark_path),
            size=(12, 12)
        )
        self.img_redmark = ctk.CTkImage(
            dark_image=Image.open(redmark_path),
            light_image=Image.open(redmark_path),
            size=(12, 12)
        )

        # Title
        title_label = ctk.CTkLabel(
            self, text="Kwaliteiten", font=ctk.CTkFont("Calibri", size=20, weight="bold"), text_color="#327bc3"
        )
        title_label.pack(pady=20)

        # Create a container for all input fields (so they always remain above the Run button)
        self.inputs_container = ctk.CTkFrame(self, fg_color="white")
        self.inputs_container.pack(side="top", fill="x")

        # Checkbox for combined test results, inside the inputs container.
        self.combined_var = tk.BooleanVar(value=False)
        combined_checkbox = ctk.CTkCheckBox(
            self.inputs_container,
            text="Gecombineerde toetsresultaten gebruiken?",
            variable=self.combined_var,
            font=ctk.CTkFont("Calibri", size=14),
            command=self.toggle_input_fields
        )
        combined_checkbox.pack(side="top", pady=10)

        # Frame for separate SOR and PFAS inputs (default visible) inside the container.
        self.sor_frame = ctk.CTkFrame(self.inputs_container, fg_color="transparent")
        self.sor_frame.pack(side="top", pady=10, padx=20, fill="x")
        sor_label = ctk.CTkLabel(self.sor_frame, text="SOR Excel File:", font=ctk.CTkFont("Calibri", size=14))
        sor_label.pack(side="left", padx=5)
        self.sor_entry = ctk.CTkEntry(self.sor_frame, placeholder_text="Selecteer SOR Excel bestand")
        self.sor_entry.pack(side="left", fill="x", expand=True, padx=5)
        sor_button = ctk.CTkButton(self.sor_frame, text="Browse", command=self.browse_sor)
        sor_button.pack(side="left", padx=5)

        self.pfas_frame = ctk.CTkFrame(self.inputs_container, fg_color="transparent")
        self.pfas_frame.pack(side="top", pady=10, padx=20, fill="x")
        pfas_label = ctk.CTkLabel(self.pfas_frame, text="PFAS Excel File:", font=ctk.CTkFont("Calibri", size=14))
        pfas_label.pack(side="left", padx=5)
        self.pfas_entry = ctk.CTkEntry(self.pfas_frame, placeholder_text="Selecteer PFAS Excel bestand")
        self.pfas_entry.pack(side="left", fill="x", expand=True, padx=5)
        pfas_button = ctk.CTkButton(self.pfas_frame, text="Browse", command=self.browse_pfas)
        pfas_button.pack(side="left", padx=5)

        # Frame for combined file input (hidden by default), also inside the container.
        self.combined_frame = ctk.CTkFrame(self.inputs_container, fg_color="transparent")
        # Do not pack it here; it will be packed when needed.
        combined_label = ctk.CTkLabel(self.combined_frame, text="Gecombineerde Excel File:", font=ctk.CTkFont("Calibri", size=14))
        combined_label.pack(side="left", padx=5)
        self.combined_entry = ctk.CTkEntry(self.combined_frame, placeholder_text="Selecteer gecombineerd Excel bestand")
        self.combined_entry.pack(side="left", fill="x", expand=True, padx=5)
        combined_button = ctk.CTkButton(self.combined_frame, text="Browse", command=self.browse_combined)
        combined_button.pack(side="left", padx=5)

        # Output CSV file selection (always visible, outside the inputs container)
        output_frame = ctk.CTkFrame(self, fg_color="transparent")
        output_frame.pack(side="top", pady=10, padx=20, fill="x")
        output_label = ctk.CTkLabel(output_frame, text="Output CSV File:", font=ctk.CTkFont("Calibri", size=14))
        output_label.pack(side="left", padx=5)
        self.output_entry = ctk.CTkEntry(output_frame, placeholder_text="Selecteer output CSV bestand")
        self.output_entry.pack(side="left", fill="x", expand=True, padx=5)
        output_button = ctk.CTkButton(output_frame, text="Browse", command=self.browse_output)
        output_button.pack(side="left", padx=5)

        # Run button: always packed after the inputs container, so it remains below all inputs.
        run_button = ctk.CTkButton(self, text="Run", command=self.run_merge, font=ctk.CTkFont("Calibri", size=14))
        run_button.pack(pady=20)

        # Status label for feedback.
        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont("Calibri", size=14))
        self.status_label.pack(pady=10)

    def toggle_input_fields(self):
        if self.combined_var.get():
            # Hide the separate input frames and show the combined frame.
            self.sor_frame.pack_forget()
            self.pfas_frame.pack_forget()
            self.combined_frame.pack(side="top", pady=10, padx=20, fill="x")
        else:
            # Hide the combined input and show the separate input frames.
            self.combined_frame.pack_forget()
            self.sor_frame.pack(side="top", pady=10, padx=20, fill="x")
            self.pfas_frame.pack(side="top", pady=10, padx=20, fill="x")

    def browse_sor(self):
        file_path = filedialog.askopenfilename(
            title="Selecteer SOR Excel bestand", filetypes=[("Excel Files", "*.xls *.xlsx")]
        )
        if file_path:
            self.sor_entry.delete(0, tk.END)
            self.sor_entry.insert(0, file_path)

    def browse_pfas(self):
        file_path = filedialog.askopenfilename(
            title="Selecteer PFAS Excel bestand", filetypes=[("Excel Files", "*.xls *.xlsx")]
        )
        if file_path:
            self.pfas_entry.delete(0, tk.END)
            self.pfas_entry.insert(0, file_path)

    def browse_combined(self):
        file_path = filedialog.askopenfilename(
            title="Selecteer gecombineerd Excel bestand", filetypes=[("Excel Files", "*.xls *.xlsx")]
        )
        if file_path:
            self.combined_entry.delete(0, tk.END)
            self.combined_entry.insert(0, file_path)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", title="Selecteer output CSV bestand", filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)

    def run_merge(self):
        output_csv = self.output_entry.get().strip()
        if self.combined_var.get():
            combined_file = self.combined_entry.get().strip()
            if not combined_file or not output_csv:
                messagebox.showerror("Error", "Zorg ervoor dat het gecombineerde Excel bestand en output CSV bestand ingevuld zijn!")
                return
        else:
            sor_file = self.sor_entry.get().strip()
            pfas_file = self.pfas_entry.get().strip()
            if not sor_file or not pfas_file or not output_csv:
                messagebox.showerror("Error", "Alle velden moeten ingevuld worden!")
                return

        self.status_label.configure(text="Processing...")
        self.update_idletasks()

        try:
            if self.combined_var.get():
                self.merge_combined_excel_file(self.combined_entry.get().strip(), output_csv)
            else:
                self.merge_excel_files(self.sor_entry.get().strip(), self.pfas_entry.get().strip(), output_csv)
            self.status_label.configure(
                text="Succesvol CSV gegenereerd",
                image=self.img_greenmark,
                compound="left"
            )
        except Exception as e:
            self.status_label.configure(
                text=f"Error: {e}",
                image=self.img_redmark,
                compound="left"
            )

    def merge_combined_excel_file(self, combined_excel, output_csv):
        # For combined files: skip the first 5 rows and select columns:
        # A, B, C, D, F, G, H, I, J, P, Q, R, S.
        # Zero-indexed these are: 0, 1, 2, 3, 5, 6, 7, 8, 9, 15, 16, 17, 18.
        usecols = [0, 1, 2, 3, 5, 6, 7, 8, 9, 15, 16, 17, 18]
        df = pd.read_excel(combined_excel, header=None, skiprows=5, usecols=usecols, engine="openpyxl")
        
        # Rename columns as specified.
        df.columns = [
            "ID", "TOL", "TOW", "VOL", 
            "4.1 G&B Landb/natuur", "4.1 G&B W/I", 
            "4.9.1 G&B Diepe plas niet-vrij", "4.9.2 G&B Diepe plas andere", 
            "4.2 B Verspreiden perceel", "TOLCOMBI", "TOW491COMBI", "TOW492COMBI", "VOLCOMBI"
        ]
        
        # Drop rows with no valid ID.
        df = df.dropna(subset=["ID"])
        
        # Clean specified columns: fill empty values and replace '--' or 'nm'.
        cols_to_clean = ["TOW", "4.9.1 G&B Diepe plas niet-vrij", "4.9.2 G&B Diepe plas andere"]
        df[cols_to_clean] = df[cols_to_clean].fillna("Niet onderzocht").replace({"nm": "Niet onderzocht", "--": "Niet onderzocht"})
        
        # Remove trailing asterisk from these columns.
        for col in cols_to_clean:
            df[col] = df[col].astype(str).str.replace(r'\*$', '', regex=True)
        
        df.to_csv(output_csv, index=False, encoding="utf-8")
        del df
        gc.collect()

    def merge_excel_files(self, sor_excel, pfas_excel, output_csv):
        SOR_SKIPROWS = 20
        PFAS_SKIPROWS = 23

        # Read SOR Excel file using only required columns.
        sor_df = pd.read_excel(
            sor_excel, header=None, skiprows=SOR_SKIPROWS, usecols=[2, 7, 8, 9, 12], engine="openpyxl"
        )
        sor_df.columns = ["ID", "TOL", "TOW", "VOL", "Emissie"]
        sor_df = sor_df.dropna(subset=["ID"])
        
        # Read PFAS Excel file.
        pfas_df = pd.read_excel(
            pfas_excel, header=None, skiprows=PFAS_SKIPROWS, usecols=[2, 7, 8, 9, 16, 17], engine="openpyxl"
        )
        pfas_df.columns = [
            "ID",
            "4.1 G&B Landb/natuur",
            "4.1 G&B W/I",
            "4.2 B Verspreiden perceel",
            "4.9.1 G&B Diepe plas niet-vrij",
            "4.9.2 G&B Diepe plas andere"
        ]
        pfas_df = pfas_df.dropna(subset=["ID"])
        
        # Merge the DataFrames on "ID" using a left join.
        merged_df = pd.merge(sor_df, pfas_df, on="ID", how="left")
        
        # Clean specific columns: fill empty values and replace 'nm' or '--' with "Niet onderzocht".
        cols_to_clean = ["TOW", "4.9.1 G&B Diepe plas niet-vrij", "4.9.2 G&B Diepe plas andere"]
        merged_df[cols_to_clean] = merged_df[cols_to_clean].fillna("Niet onderzocht").replace({"nm": "Niet onderzocht", "--": "Niet onderzocht"})
        
        # Remove trailing asterisk from these columns.
        for col in cols_to_clean:
            merged_df[col] = merged_df[col].astype(str).str.replace(r'\*$', '', regex=True)
        
        merged_df.to_csv(output_csv, index=False, encoding="utf-8")
        del sor_df, pfas_df, merged_df
        gc.collect()
