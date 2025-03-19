import os
import customtkinter as ctk
from PIL import Image

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, base_dir, analysis_callback=None, merge_callback=None, kwaliteiten_callback=None):
        super().__init__(parent, fg_color="white")
        self.base_dir = base_dir

        # --------------------------
        # 1) Load a large background image with CTkImage
        # --------------------------
        # bg_path = os.path.join(self.base_dir, "resources", "images", "bg4.png")
        # self.bg_image = ctk.CTkImage(
        #     dark_image=Image.open(bg_path),
        #     light_image=Image.open(bg_path),
        #     size=(1100, 700)  # Adjust to fit your window
        # )
        # # 2) Label to hold background
        # self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
        # self.bg_label.pack(fill="both", expand=True)

        # 3) Foreground frame on top of the background
        self.foreground_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height = 600,
            width = 500
        )
        # Position the foreground frame over the background.
        self.foreground_frame.place(relx=0.02, rely=0.02, anchor="nw")  

        # --------------------------
        # 4) Load smaller button images with CTkImage
        # --------------------------
        eurofins_img_path = os.path.join(self.base_dir, "resources", "images", "eurofins.png")
        pdf_img_path = os.path.join(self.base_dir, "resources", "images", "pdf.png")
        excel_img_path = os.path.join(base_dir, "resources", "images", "excel_logo.png")

        self.img_eurofins = ctk.CTkImage(
            dark_image=Image.open(eurofins_img_path),
            light_image=Image.open(eurofins_img_path),
            size=(24, 24)  # icon size
        )
        self.img_pdf = ctk.CTkImage(
            dark_image=Image.open(pdf_img_path),
            light_image=Image.open(pdf_img_path),
            size=(24, 24)  # icon size
        )
        self.img_excel = ctk.CTkImage(
            dark_image=Image.open(excel_img_path),
            light_image=Image.open(excel_img_path),
            size=(24, 24)  # icon size
        )

        # --------------------------
        # 5) Place your labels and buttons in the foreground_frame
        # --------------------------
        label1 = ctk.CTkLabel(
            self.foreground_frame,
            text="Toelichting op de tool",
            text_color="#327bc3",
            anchor='w',
            font=ctk.CTkFont('Bahnschrift SemiLight SemiConde', size=24, weight="bold")
        )
        label1.pack(anchor='w', pady=(10, 5), padx=(30, 0))

        # Button to navigate to "Analysecertificaten"
        button_analysis = ctk.CTkButton(
            self.foreground_frame,
            text="Analysecertificaten",
            corner_radius=15,
            hover_color="#508C9B",
            fg_color="#134B70",
            text_color='#EEEEEE',
            image=self.img_eurofins,
            command=analysis_callback  # When clicked, switch to the Analysis page
        )
        button_analysis.pack(anchor="w", pady=(40,2), padx=(25, 0))

        text_analysis = (
            "Hiermee kun je kiezen welke analysecertificaten van de Y-schijf \n"
            "(of een andere map) naar de projectmap moeten worden gekopieerd. \n"
            "Bovendien worden al deze analysecertificaten ook samengevoegd \n"
            "in progressieve volgorde."
        )
        textbox = ctk.CTkTextbox(
            self.foreground_frame,
            text_color='#201E43',
            font=ctk.CTkFont('Calibri', size=15),
            fg_color='transparent',
            height=100, width=450
        )
        textbox.insert("0.0", text_analysis)
        textbox.configure(state="disabled")
        textbox.pack(fill='x', pady=10, padx=10)

        # Button to navigate to "PDF's mergen"
        button_merge = ctk.CTkButton(
            self.foreground_frame,
            text="PDF's mergen",
            corner_radius=15,
            hover_color="#508C9B",
            fg_color="#134B70",
            text_color='#EEEEEE',
            image=self.img_pdf,
            command=merge_callback  # When clicked, switch to the Merge page
        )
        button_merge.pack(anchor="w", pady=(20,2), padx=(25, 0))

        label_merge = ctk.CTkTextbox(
            self.foreground_frame,
            text_color='#201E43',
            font=ctk.CTkFont('Calibri', size=15),
            fg_color='transparent',
            height=100, width=400
        )
        text_merge = (
            "Hiermee kun je kiezen welke PDF's bestanden samengevoegd moeten worden "
            "tot één bestand.\nDit is handig om bijlagen voor de rapportage te maken."
        )
        label_merge.insert("0.0", text_merge)
        label_merge.configure(state="disabled")
        label_merge.pack(fill='x', pady=(2,20), padx=(25,0))

        # Button to navigate to "Kwaliteiten CSV file"
        button_kwaliteiten = ctk.CTkButton(
            self.foreground_frame,
            text="Kwaliteiten CSV bestand",
            corner_radius=15,
            hover_color="#508C9B",
            fg_color="#134B70",
            text_color='#EEEEEE',
            image=self.img_excel,
            command=kwaliteiten_callback  # When clicked, switch to the Merge page
        )
        button_kwaliteiten.pack(anchor="w", pady=(5,2), padx=(25, 0))

        label_kwaliteiten = ctk.CTkTextbox(
            self.foreground_frame,
            text_color='#201E43',
            font=ctk.CTkFont('Calibri', size=15),
            fg_color='transparent',
            height=100, width=400
        )
        text_kwaliteiten = (
            "Hiermee kun je de SOR en PFAS toetsingen samenvoegen tot "
            "één CSV-bestand.\nDit kun je in ArcGIS inladen voor een kwaliteiten shape."
        )
        label_kwaliteiten.insert("0.0", text_kwaliteiten)
        label_kwaliteiten.configure(state="disabled")
        label_kwaliteiten.pack(fill='x', pady=(2,20), padx=(25,0))
