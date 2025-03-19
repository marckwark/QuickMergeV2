import customtkinter as ctk
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import filedialog, messagebox
import os, threading, time, shutil
from datetime import datetime
from PIL import Image
import re
import fitz  # PyMuPDF for PDF operations

class AnalysisPage(ctk.CTkFrame):
    def __init__(self, parent, base_dir):
        super().__init__(parent, fg_color="white")
        self.base_dir = base_dir

        # Load images as CTkImage
        folder_img_path = os.path.join(self.base_dir, "resources", "images", "folder.png")
        run_img_path = os.path.join(self.base_dir, "resources", "images", "run.png")
        greenmark_path = os.path.join(self.base_dir, "resources", "images", "greenmark.png")
        redmark_path   = os.path.join(self.base_dir, "resources", "images", "redmark.png")

        self.img_folder = ctk.CTkImage(
            dark_image=Image.open(folder_img_path),
            light_image=Image.open(folder_img_path),
            size=(24, 24)
        )
        self.img_run = ctk.CTkImage(
            dark_image=Image.open(run_img_path),
            light_image=Image.open(run_img_path),
            size=(24, 24)
        )
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

        # =============== LEFT Info Frame ===============
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(side="left", padx=10, pady=(20,10), fill="both", expand=True)

        label_title = ctk.CTkLabel(
            info_frame,
            text="Analysecertificaten",
            fg_color="transparent",
            text_color="#327bc3",
            font=ctk.CTkFont("Bahnschrift SemiLight SemiConde", size=20, weight="bold")
        )
        label_title.pack(padx=10, pady=(20,10), anchor="w")

        instructions = (
            "Gebruiksaanwijzing:\n"
            "1) Vul de monstervakcode (bv. 'W24YR07').\n"
            "2) Vul het OMS nummer (bv. '24-314') in.\n"
            "3) Selecteer de input folder waarin de PDF's staan.\n"
            "4) Vink aan of je de gevonden PDF's wilt kopiëren, samenvoegen, of beide.\n"
            "   → De PDF's worden automatisch in progressieve volgorde gezet\n"
            "5) Selecteer de output folder.\n"
            "   → Als je wilt samenvoegen, geef je ook een bestandsnaam op.\n"
            "6) Kies een datumbereik waartussen de PDF's gegenereerd zijn.\n"
            "7) Klik op Run om de code te runnen!\n"
            "\n"
            "Waterschap\tFile path\n"
            "WSRL\tY:\\Gegevens_uitwisseling\\Rapportage\\WSRL\\WSRL_BAG\\PROD\n"
            "WSHD\tY:\\Gegevens_uitwisseling\\Rapportage\\WSHD\\WSHD_GEO\\PROD\n"
            "WSAM\tY:\\Gegevens_uitwisseling\\Rapportage\\AAMAAS\\Toetsing WaBo\n"
            "HDSR\tY:\\Gegevens_uitwisseling\\Rapportage\\HDSR\\HDSR_WaBo\\PROD\n"
            "HHRL\tY:\\Gegevens_uitwisseling\\Rapportage\\HHVR\\HHVR_OW\\PROD\n"
            "HHDL\tY:\\Gegevens_uitwisseling\\Rapportage\\HHVD\\HHVD_WaBo\\PROD\n"
            "WSBD\tY:\\Gegevens_uitwisseling\\Rapportage\\WSBD\\WSBD_KA\\PROD\n"
            "HHSK\tY:\\Gegevens_uitwisseling\\Rapportage\\HHSK\\HHSK_WaBo\\PROD\n"
            "WSDD\tY:\\Gegevens_uitwisseling\\Rapportage\\DOMMEL\\DOMMEL_OW\\PROD\n"
        )

        textbox = ctk.CTkTextbox(
            info_frame,
            height=450,
            fg_color="transparent",
            text_color="#201E43",
            font=ctk.CTkFont("Calibri", size=15)
        )
        textbox.insert("0.0", instructions)
        textbox.configure(state="disabled")
        textbox.pack(fill="x", padx=10, pady=10)

        # =============== RIGHT Form Frame ===============
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.pack(side="right", padx=10, pady=(90,20), fill="both", expand=True)

        # Row 1: Monstervakcode
        seq_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        seq_frame.pack(pady=(5,5), padx=15, fill="x")
        ctk.CTkLabel(seq_frame, text="Monstervakcode", font=ctk.CTkFont("Calibri", weight="bold")).pack(side="left", padx=5)
        self.sequence_entry = ctk.CTkEntry(
            seq_frame, placeholder_text="bijv. 'W24YR07'",
            fg_color="white", border_width=1, border_color="black"
        )
        self.sequence_entry.pack(side="left", fill="x", expand=True)

        # Row 2: OMS nummer
        proj_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        proj_frame.pack(pady=(5,5), padx=15, fill="x")
        ctk.CTkLabel(proj_frame, text="OMS nummer", font=ctk.CTkFont("Calibri", weight="bold")).pack(side="left", padx=5)
        self.project_entry = ctk.CTkEntry(
            proj_frame, placeholder_text="bijv. '24-314'",
            fg_color="white", border_width=1, border_color="black"
        )
        self.project_entry.pack(side="left", fill="x", expand=True)

        # Row 3: Input folder
        input_folder_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        input_folder_frame.pack(pady=(5,5), padx=15, fill="x")
        ctk.CTkLabel(input_folder_frame, text="Input folder", font=ctk.CTkFont("Calibri", weight="bold")).pack(side="left", padx=5)
        self.input_folder_button = ctk.CTkButton(
            input_folder_frame,
            text="Selecteer folder met PDF's",
            command=self.browse_input_folder,
            border_width=1, border_color="black",
            hover_color="#e4e4e4", text_color="black",
            fg_color="transparent", image=self.img_folder
        )
        self.input_folder_button.pack(side="left", fill="x", expand=True)

        # Row 4: Output folder
        output_folder_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        output_folder_frame.pack(pady=(5,5), padx=15, fill="x")
        ctk.CTkLabel(output_folder_frame, text="Output folder", font=ctk.CTkFont("Calibri", weight="bold")).pack(side="left", padx=5)
        self.output_folder_button = ctk.CTkButton(
            output_folder_frame,
            text="Selecteer de output folder",
            command=self.browse_output_folder,
            border_width=1, border_color="black",
            hover_color="#e4e4e4", text_color="black",
            fg_color="transparent", image=self.img_folder
        )
        self.output_folder_button.pack(side="left", fill="x", expand=True)

        # Row 5: Bestandsnaam (only shown if merging is on)
        self.merge_name_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.merge_name_frame.pack(pady=(15,5), padx=15, fill="x")
        ctk.CTkLabel(self.merge_name_frame, text="Bestandsnaam", font=ctk.CTkFont("Calibri", weight="bold")).pack(side="left", padx=5)
        self.merged_name_entry = ctk.CTkEntry(
            self.merge_name_frame,
            placeholder_text="bv. '24-310 W24YR07_Bijlage 02_Vooronderzoek'",
            fg_color="white", border_width=1, border_color="black"
        )
        self.merged_name_entry.pack(side="left", fill="x", expand=True)

        # Row 6: Checkboxes (copy and merge)
        checkbox_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        checkbox_frame.pack(pady=(10,5), padx=15, fill="x")

        self.copy_var = tk.StringVar(value="on")
        self.copy_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="Kopieer gevonden PDF's en plak ze in de output folder",
            variable=self.copy_var, onvalue="on", offvalue="off",
            checkbox_height=16, checkbox_width=16,
            checkmark_color='#dce4ee', hover_color='#c5e7f9',
            corner_radius=5, border_width=0.5, border_color='#676767',
            fg_color='#327bc3', font=ctk.CTkFont("Calibri", size=12)
        )
        self.copy_checkbox.pack(side="top", anchor="w")

        self.merge_var = tk.StringVar(value="on")
        self.merge_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="Voeg PDF's samen tot één bestand",
            variable=self.merge_var, onvalue="on", offvalue="off",
            checkbox_height=16, checkbox_width=16,
            checkmark_color='#dce4ee', hover_color='#c5e7f9',
            corner_radius=5, border_width=0.5, border_color='#676767',
            fg_color='#327bc3', font=ctk.CTkFont("Calibri", size=12),
            command=self.toggle_merge_fields
        )
        self.merge_checkbox.pack(side="top", anchor="w", pady=(5,0))

        # New: Afperkend onderzoek checkbox
        self.afperkend_var = tk.BooleanVar(value=False)
        self.afperkend_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="Is dit een afperkend onderzoek?",
            variable=self.afperkend_var,
            checkbox_height=16, checkbox_width=16,
            checkmark_color='#dce4ee', hover_color='#c5e7f9',
            corner_radius=5, border_width=0.5, border_color='#676767',
            fg_color='#327bc3', font=ctk.CTkFont("Calibri", size=12),
            command=self.toggle_afperkend_fields
        )
        self.afperkend_checkbox.pack(side="top", anchor="w", pady=(5,0))

        # New: Locatiebezoek checkbox – if unchecked deduplicate by file size.
        self.locatiebezoek_var = tk.BooleanVar(value=False)
        self.locatiebezoek_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="Locatiebezoek toevoegen?",
            variable=self.locatiebezoek_var,
            checkbox_height=16, checkbox_width=16,
            checkmark_color='#dce4ee', hover_color='#c5e7f9',
            corner_radius=5, border_width=0.5, border_color='#676767',
            fg_color='#327bc3', font=ctk.CTkFont("Calibri", size=12)
        )
        self.locatiebezoek_checkbox.pack(side="top", anchor="w", pady=(5,0))

        # Save a reference to the checkbox frame for ordering
        self.checkbox_frame = checkbox_frame
        self.toggle_merge_fields()

        # New: Secondary sequence entry (shown only if afperkend is checked)
        # Now make it a child of the checkbox_frame so it appears immediately below the afperkend checkbox.
        self.secondary_seq_frame = ctk.CTkFrame(checkbox_frame, fg_color="transparent")
        self.secondary_seq_label = ctk.CTkLabel(
            self.secondary_seq_frame, text="Secundaire sequentie karakter", font=ctk.CTkFont("Calibri", weight="bold")
        )
        self.secondary_seq_label.pack(side="left", padx=5)
        self.secondary_seq_entry = ctk.CTkEntry(
            self.secondary_seq_frame,
            placeholder_text="bijv. '.'",
            fg_color="white", border_width=1, border_color="black"
        )
        self.secondary_seq_entry.pack(side="left", fill="x", expand=True)

        # Row 7: Date pickers
        date_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        date_frame.pack(pady=(5,5), padx=15, fill="x")

        self.start_date_entry = DateEntry(date_frame, date_pattern="dd-mm-yyyy", borderwidth=2)
        self.start_date_entry.pack(side="left", padx=(5,5))
        self.end_date_entry = DateEntry(date_frame, date_pattern="dd-mm-yyyy", borderwidth=2)
        self.end_date_entry.pack(side="left", padx=(5,5))

        # Row 8: Run button
        self.run_button = ctk.CTkButton(
            self.form_frame,
            text="Run",
            command=self.run_process,
            border_width=1, border_color="black",
            hover_color="#e4e4e4", text_color="black",
            fg_color="transparent", image=self.img_run
        )
        self.run_button.pack(pady=(15,5), padx=15, anchor="e")

        # Status frame (initially empty)
        self.status_frame = None

    def toggle_merge_fields(self):
        if self.merge_var.get() == "on":
            self.merge_name_frame.pack(before=self.checkbox_frame,
                                         pady=(5,5), padx=15, fill="x")
        else:
            self.merge_name_frame.pack_forget()

    def toggle_afperkend_fields(self):
        if self.afperkend_var.get():
            self.secondary_seq_frame.pack(side="top", fill="x", padx=20, pady=(5,5))
        else:
            self.secondary_seq_frame.pack_forget()

    def browse_input_folder(self):
        folder_path = filedialog.askdirectory(title="Selecteer folder met PDF's")
        if folder_path:
            self.input_folder_button.configure(text=folder_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory(title="Selecteer de output folder")
        if folder_path:
            self.output_folder_button.configure(text=folder_path)

    def deduplicate_by_size(self, pdf_list, primary_sequence):
        """
        Groups PDFs by the numeric portion following the primary sequence.
        If afperkend is active, the regex uses the secondary sequence character too.
        Within each group, only the PDF with the largest file size is retained.
        """
        dedup_map = {}
        if self.afperkend_var.get():
            secondary = self.secondary_seq_entry.get().strip()
            if not secondary:
                messagebox.showerror("Error", "Geef een secundaire sequentie karakter op.")
                return pdf_list
            pattern = re.compile(rf"{re.escape(primary_sequence)}(\d+){re.escape(secondary)}(\d+)")
            for pdf in pdf_list:
                base_name = os.path.basename(pdf)
                m = pattern.search(base_name)
                if m:
                    group_key = (m.group(1), m.group(2))
                else:
                    group_key = base_name
                size = os.path.getsize(pdf)
                if group_key not in dedup_map or size > dedup_map[group_key][0]:
                    dedup_map[group_key] = (size, pdf)
            return [v[1] for v in dedup_map.values()]
        else:
            pattern = re.compile(rf"{re.escape(primary_sequence)}(\d+)")
            for pdf in pdf_list:
                base_name = os.path.basename(pdf)
                m = pattern.search(base_name)
                if m:
                    group_key = m.group(1)
                else:
                    group_key = base_name
                size = os.path.getsize(pdf)
                if group_key not in dedup_map or size > dedup_map[group_key][0]:
                    dedup_map[group_key] = (size, pdf)
            return [v[1] for v in dedup_map.values()]

    def run_process(self):
        # Gather input parameters
        sequence = self.sequence_entry.get().strip()
        project_code = self.project_entry.get().strip()
        input_folder = self.input_folder_button.cget("text")
        output_folder = self.output_folder_button.cget("text")
        do_copy = (self.copy_var.get() == "on")
        do_merge = (self.merge_var.get() == "on")

        # Validate basic fields
        if not input_folder:
            messagebox.showerror("Error", "Selecteer de input folder.")
            return
        if not do_copy and not do_merge:
            messagebox.showerror("Error", "Selecteer minstens één bewerking (kopiëren of samenvoegen).")
            return
        if not output_folder:
            messagebox.showerror("Error", "Selecteer de output folder.")
            return

        # If merging is on, ensure bestandsnaam is given
        merged_pdf_name = None
        if do_merge:
            merged_pdf_name = self.merged_name_entry.get().strip()
            if not merged_pdf_name:
                messagebox.showerror("Error", "Voer een bestandsnaam in voor het samengevoegde PDF bestand.")
                return

        # Convert dates to strings
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        start_date_str = start_date.strftime("%d-%m-%Y")
        end_date_str = end_date.strftime("%d-%m-%Y")

        # Gather matching PDF files from input_folder
        try:
            all_files = [
                os.path.join(input_folder, f)
                for f in os.listdir(input_folder)
                if project_code in f and f.lower().endswith(".pdf")
            ]
        except Exception as e:
            messagebox.showerror("Error", f"Error accessing input folder: {e}")
            return

        if not all_files:
            messagebox.showerror("Error", "Geen PDF bestanden gevonden die voldoen aan de OMS code.")
            return

        # Filter PDFs based on date range using PyMuPDF metadata
        filtered_pdfs = []
        start_date_obj = datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date_obj = datetime.strptime(end_date_str, "%d-%m-%Y")
        end_date_obj = end_date_obj.replace(hour=23, minute=59, second=59)

        for pdf in all_files:
            try:
                doc = fitz.open(pdf)
                metadata = doc.metadata
                pdf_date_obj = None
                pdf_date_str = None
                if metadata.get("modDate"):
                    pdf_date_str = metadata.get("modDate")
                elif metadata.get("creationDate"):
                    pdf_date_str = metadata.get("creationDate")
                if pdf_date_str:
                    if pdf_date_str.startswith("D:"):
                        pdf_date_str = pdf_date_str[2:]
                    pdf_date_obj = datetime.strptime(pdf_date_str[:14], "%Y%m%d%H%M%S")
                if pdf_date_obj and start_date_obj <= pdf_date_obj <= end_date_obj:
                    filtered_pdfs.append(pdf)
            except Exception as e:
                print(f"Error processing {pdf}: {e}")

        if not filtered_pdfs:
            messagebox.showerror("Error", "Geen PDF's gevonden in de geselecteerde periode.")
            return

        # If "Locatiebezoek toevoegen?" is unchecked, deduplicate by file size for PDFs with the same number.
        if not self.locatiebezoek_var.get():
            filtered_pdfs = self.deduplicate_by_size(filtered_pdfs, sequence)

        # Further deduplicate exact file paths if needed.
        unique_files = []
        seen = set()
        for f in filtered_pdfs:
            norm_f = os.path.normcase(os.path.abspath(f))
            if norm_f not in seen:
                unique_files.append(f)
                seen.add(norm_f)
        filtered_pdfs = unique_files

        # Progressive ordering by digits after the primary sequence
        filtered_pdfs = self.progressive_order_pdfs(filtered_pdfs, sequence)

        # Setup status UI
        if self.status_frame:
            self.status_frame.destroy()
        self.status_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.status_frame.pack(fill="x")
        self.status_label = ctk.CTkLabel(self.status_frame, text="Running...", font=ctk.CTkFont("Calibri"))
        self.status_label.pack(side="top", pady=(5,5), padx=15)
        self.progress_bar = ctk.CTkProgressBar(self.status_frame, orientation="horizontal", mode="indeterminate")
        self.progress_bar.pack(side="top", pady=(0,5), padx=15)
        self.progress_bar.start()

        # Start thread to process PDFs
        threading.Thread(
            target=self.process_task,
            args=(filtered_pdfs, output_folder, do_copy, do_merge, merged_pdf_name)
        ).start()

    def progressive_order_pdfs(self, pdf_list, primary_sequence):
        """
        Sorts the given PDF list by extracting numbers from filenames.
        If the "afperkend" checkbox is checked, it expects filenames to include:
          primary_sequence + main_number + secondary_sequence_character + secondary_number.
        Otherwise, it extracts only the digits following the primary_sequence.
        """
        if self.afperkend_var.get():
            secondary = self.secondary_seq_entry.get().strip()
            if not secondary:
                messagebox.showerror("Error", "Geef een secundaire sequentie karakter op.")
                return pdf_list
            pattern = re.compile(rf"{re.escape(primary_sequence)}(\d+){re.escape(secondary)}(\d+)")
            matched = []
            for pdf_path in pdf_list:
                base_name = os.path.basename(pdf_path)
                match = pattern.search(base_name)
                if match:
                    try:
                        main_number = int(match.group(1))
                        secondary_number = int(match.group(2))
                        matched.append((pdf_path, main_number, secondary_number))
                    except Exception as e:
                        print(f"Error parsing numbers in {pdf_path}: {e}")
            matched.sort(key=lambda x: (x[1], x[2]))
            return [m[0] for m in matched]
        else:
            pattern = re.compile(rf"{re.escape(primary_sequence)}(\d+)")
            matched = []
            for pdf_path in pdf_list:
                base_name = os.path.basename(pdf_path)
                match = pattern.search(base_name)
                if match:
                    try:
                        number = int(match.group(1))
                        matched.append((pdf_path, number))
                    except Exception as e:
                        print(f"Error parsing number in {pdf_path}: {e}")
            matched.sort(key=lambda x: x[1])
            return [m[0] for m in matched]

    def process_task(self, pdf_list, output_folder, do_copy, do_merge, merged_pdf_name):
        try:
            start_time = time.time()
            processed_size = 0
            total_size = sum(os.path.getsize(f) for f in pdf_list)
            total_size_mb = total_size / (1024 * 1024)

            if do_merge:
                merged_doc = fitz.open()

            for index, pdf_path in enumerate(pdf_list):
                file_size = os.path.getsize(pdf_path)

                if do_copy:
                    dest = os.path.join(output_folder, os.path.basename(pdf_path))
                    try:
                        shutil.copy2(pdf_path, dest)
                    except Exception as e:
                        print(f"Fout bij kopiëren: {pdf_path}, {e}")

                if do_merge:
                    try:
                        doc = fitz.open(pdf_path)
                        merged_doc.insert_pdf(doc)
                        doc.close()
                    except Exception as e:
                        print(f"Fout bij samenvoegen: {pdf_path}, {e}")

                processed_size += file_size
                elapsed = time.time() - start_time
                speed = processed_size / elapsed if elapsed > 0 else 0
                remaining = (total_size - processed_size) / speed if speed > 0 else 0
                progress = (processed_size / total_size) * 100
                self.status_label.after(0, lambda p=progress, ps=processed_size, ts=total_size_mb, r=remaining: self.status_label.configure(
                    text=f"{p:.2f}% ({ps/(1024*1024):.2f} MB / {ts:.2f} MB), Time left: {r:.2f} s"
                ))
                time.sleep(0.05)

            if do_merge:
                merged_path = os.path.join(output_folder, merged_pdf_name + ".pdf")
                try:
                    merged_doc.save(merged_path)
                    merged_doc.close()
                except Exception as e:
                    print(f"Error saving merged PDF: {e}")

            self.status_label.after(0, lambda: self.status_label.configure(
                text="  Succesvol analysecertificaten gegenereerd",
                image=self.img_greenmark,
                compound="left"
            ))
        except Exception as e:
            self.status_label.after(0, lambda: self.status_label.configure(
                text=f"  Error: {e}",
                image=self.img_redmark,
                compound="left"
            ))
        finally:
            self.progress_bar.after(0, self.progress_bar.stop)
            self.progress_bar.after(0, self.progress_bar.pack_forget)
