import customtkinter as ctk
from tkinter import filedialog, messagebox
import os, threading, time, shutil
from pathlib import Path
from PIL import Image
import fitz  # Using PyMuPDF for merging

class MergePage(ctk.CTkFrame):
    def __init__(self, parent, base_dir):
        super().__init__(parent, fg_color="white")
        self.base_dir = base_dir

        # Load images as CTkImage
        folder_img_path = os.path.join(self.base_dir, "resources", "images", "folder.png")
        pdf_img_path = os.path.join(self.base_dir, "resources", "images", "pdf.png")
        run_img_path = os.path.join(self.base_dir, "resources", "images", "run.png")
        greenmark_path = os.path.join(self.base_dir, "resources", "images", "greenmark.png")
        redmark_path   = os.path.join(self.base_dir, "resources", "images", "redmark.png")

        self.img_folder = ctk.CTkImage(
            dark_image=Image.open(folder_img_path),
            light_image=Image.open(folder_img_path),
            size=(24, 24)
        )
        self.img_pdf = ctk.CTkImage(
            dark_image=Image.open(pdf_img_path),
            light_image=Image.open(pdf_img_path),
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
        # Left info frame
        info_frame = ctk.CTkFrame(self, fg_color='transparent')
        info_frame.pack(side="left", padx=10, pady=(20,10), fill="both", expand=True)

        label_title = ctk.CTkLabel(
            info_frame,
            text="PDF's mergen",
            fg_color='transparent',
            text_color='#327bc3',
            font=ctk.CTkFont('Bahnschrift SemiLight SemiConde', size=20, weight="bold")
        )
        label_title.pack(padx=10, pady=(20,10), anchor='w')

        instructions = (
            "Gebruiksaanwijzing:\n"
            "1) Selecteer de PDF-bestanden in de gewenste volgorde.\n"
            "2) De PDF's zullen worden samengevoegd in de volgorde van boven naar beneden.\n"
            "3) In één regel kun je ook meerdere PDF's tegelijkertijd selecteren.\n"
            "4) Klik op 'Run' om de PDF's samen te voegen!\n"
        )
        textbox = ctk.CTkTextbox(
            info_frame,
            height=350,
            fg_color='transparent',
            text_color='#201E43',
            font=ctk.CTkFont('Calibri', size=15)
        )
        textbox.insert("0.0", instructions)
        textbox.configure(state="disabled")
        textbox.pack(fill='x', padx=10, pady=10)

        # Right form frame
        self.form_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.form_frame.pack(side="right", padx=10, pady=(90,20), fill="both", expand=True)

        # Initialize PDF selections (8 slots for individual selection)
        self.pdf_paths = [[] for _ in range(4)]
        self.pdf_buttons = []
        self.create_pdf_buttons()

        # Output PDF location button
        self.output_path = ""
        self.output_button = ctk.CTkButton(
            self.form_frame,
            text="Geef je bestand een naam en locatie",
            command=self.browse_output_path,
            border_width=1,
            border_color='black',
            hover_color='#e4e4e4',
            text_color='black',
            fg_color="transparent",
            image=self.img_pdf
        )
        self.output_button.pack(pady=(10,10), padx=15, fill='x')

        # Validation label for general errors
        self.validation_label = ctk.CTkTextbox(
            self.form_frame,
            text_color='red',
            fg_color='transparent',
            font=ctk.CTkFont('Calibri', weight='bold'),
            height=55,
            width=220
        )
        self.validation_label.insert("0.0", "")
        self.validation_label.configure(state="disabled")
        self.validation_label.pack(pady=(45,0), padx=5, anchor='e')

        # Run button
        self.run_button = ctk.CTkButton(
            self.form_frame,
            text="Run",
            command=self.run_process,
            border_width=1,
            border_color='black',
            hover_color='#e4e4e4',
            text_color='black',
            fg_color="transparent",
            image=self.img_run
        )
        self.run_button.pack(pady=(20,5), padx=15, anchor='e')

        # Status frame (initially empty)
        self.status_frame = None

    def create_pdf_buttons(self):
        # Eight buttons for selecting individual PDFs
        for i in range(8):
            btn = ctk.CTkButton(
                self.form_frame,
                text="Selecteer je PDFs",
                command=lambda idx=i: self.browse_pdfs(idx),
                border_width=1,
                border_color='black',
                hover_color='#e4e4e4',
                text_color='black',
                fg_color="transparent",
                image=self.img_pdf
            )
            btn.pack(pady=5, padx=15, fill='x')
            self.pdf_buttons.append(btn)

    def browse_pdfs(self, index):
        file_paths = filedialog.askopenfilenames(title="Selecteer je PDFs", filetypes=[("PDF files", "*.pdf")])
        if file_paths:
            self.pdf_paths[index] = list(file_paths)
            names = [os.path.basename(fp) for fp in file_paths]
            self.pdf_buttons[index].configure(text=", ".join(names))
        else:
            self.pdf_paths[index] = []
            self.pdf_buttons[index].configure(text="Selecteer je PDFs")

    def browse_folder(self, index):
        folder_path = filedialog.askdirectory(title="Selecteer je folder")
        if folder_path:
            from pathlib import Path
            files = [str(fp) for fp in Path(folder_path).rglob("*.pdf")]
            self.pdf_paths[index] = files
            self.pdf_buttons[index].configure(text=folder_path)
        else:
            self.pdf_paths[index] = []
            self.pdf_buttons[index].configure(text="Selecteer je folder")

    def browse_output_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.output_path = file_path
            self.output_button.configure(text=file_path)
        else:
            self.output_button.configure(text="Geef je bestand een naam en locatie")

    def run_process(self):
        # Flatten all PDFs from the slots into a single list.
        all_files = []
        for file_list in self.pdf_paths:
            if file_list:
                all_files.extend(file_list)

        # Ensure there are at least two PDFs and an output path is selected.
        if len(all_files) < 2 or not self.output_path:
            self.validation_label.configure(state="normal")
            self.validation_label.delete("0.0", "end")
            self.validation_label.insert("0.0", "Selecteer ten minste 2 PDF bestanden en selecteer een folder om in op te slaan.")
            self.validation_label.configure(state="disabled")
            return
        else:
            self.validation_label.configure(state="normal")
            self.validation_label.delete("0.0", "end")
            self.validation_label.configure(state="disabled")

        # Deduplicate the file list (normalize paths)
        unique_files = []
        seen = set()
        for f in all_files:
            norm_f = os.path.normcase(os.path.abspath(f))
            if norm_f not in seen:
                unique_files.append(f)
                seen.add(norm_f)
        all_files = unique_files

        if self.status_frame:
            self.status_frame.destroy()
            self.status_frame = None

        self.status_frame = ctk.CTkFrame(self.form_frame, fg_color='transparent')
        self.status_frame.pack(fill='x')
        self.status_label = ctk.CTkLabel(self.status_frame, text="Running...", font=ctk.CTkFont('Calibri'))
        self.status_label.pack(side='top', pady=(5,5), padx=15)
        self.progress_bar = ctk.CTkProgressBar(self.status_frame, orientation='horizontal', mode='indeterminate')
        self.progress_bar.pack(side='top', pady=(0,5), padx=15)
        self.progress_bar.start()

        threading.Thread(target=self.process_task, args=(all_files,)).start()

    def process_task(self, file_list):
        try:
            start_time = time.time()
            processed_size = 0
            total_size = sum(os.path.getsize(f) for f in file_list)
            total_size_mb = total_size / (1024 * 1024)
            merged_doc = fitz.open()

            for index, pdf_path in enumerate(file_list):
                file_size = os.path.getsize(pdf_path)
                try:
                    doc = fitz.open(pdf_path)
                    merged_doc.insert_pdf(doc)
                    doc.close()
                except Exception as e:
                    print(f"Error merging {pdf_path}: {e}")
                processed_size += file_size
                # Update progress
                elapsed = time.time() - start_time
                speed = processed_size / elapsed if elapsed > 0 else 0
                remaining = (total_size - processed_size) / speed if speed > 0 else 0
                progress = (processed_size / total_size) * 100
                self.status_label.after(0, lambda p=progress, ps=processed_size, ts=total_size_mb, r=remaining: self.status_label.configure(
                    text=f"{p:.2f}% ({ps/(1024*1024):.2f} MB / {ts:.2f} MB), Time left: {r:.2f} s"
                ))
                time.sleep(0.05)
            merged_pdf_path = self.output_path
            try:
                merged_doc.save(merged_pdf_path)
                merged_doc.close()
            except Exception as e:
                print(f"Error saving merged PDF: {e}")
            self.status_label.after(0, lambda: self.status_label.configure(
                text=" Succesvol PDF's samengevoegd",
                image=self.img_greenmark,
                compound="left"
            ))
        except Exception as e:
            self.status_label.after(0, lambda: self.status_label.configure(
                text=f"   Error: {e}",
                image=self.img_redmark,
                compound="left"
            ))
        finally:
            self.progress_bar.after(0, self.progress_bar.stop)
            self.progress_bar.after(0, self.progress_bar.pack_forget)