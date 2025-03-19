import os
import customtkinter as ctk
from PIL import Image

# Import pages
from pages.home_page import HomePage
from pages.analysis_page import AnalysisPage
from pages.merge_page import MergePage
from pages.kwaliteiten_page import KwaliteitenPage


def main():
    app = ctk.CTk()
    app.title("Analysecertificaten PDF")
    app.geometry("1100x700")
    app.resizable(True, True)

    # Container for pages
    container = ctk.CTkFrame(app)
    container.pack(side="right", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # ─────────────────────────────────────────────────────────
    # 1) Load icons for the sidebar as CTkImage
    # ─────────────────────────────────────────────────────────
    home_img_path = os.path.join(base_dir, "resources", "images", "home.png")
    analysis_img_path = os.path.join(base_dir, "resources", "images", "eurofins.png")
    merge_img_path = os.path.join(base_dir, "resources", "images", "pdf.png")
    kwali_img_path = os.path.join(base_dir, "resources", "images", "excel_logo.png")

    img_home = ctk.CTkImage(
        dark_image=Image.open(home_img_path),
        light_image=Image.open(home_img_path),
        size=(24, 24)
    )
    img_analysis = ctk.CTkImage(
        dark_image=Image.open(analysis_img_path),
        light_image=Image.open(analysis_img_path),
        size=(24, 24)
    )
    img_merge = ctk.CTkImage(
        dark_image=Image.open(merge_img_path),
        light_image=Image.open(merge_img_path),
        size=(24, 24)
    )
    img_kwali = ctk.CTkImage(
        dark_image=Image.open(kwali_img_path),
        light_image=Image.open(kwali_img_path),
        size=(24, 24)
    )
    # ─────────────────────────────────────────────────────────
    # 2) Instantiate pages
    # ─────────────────────────────────────────────────────────
    pages = {}
    pages["AnalysisPage"] = AnalysisPage(container, base_dir)
    pages["MergePage"] = MergePage(container, base_dir)
    pages["KwaliteitenPage"] = KwaliteitenPage(container, base_dir)
    pages["HomePage"] = HomePage(
        container,
        base_dir,
        analysis_callback=lambda: pages["AnalysisPage"].tkraise(),
        merge_callback=lambda: pages["MergePage"].tkraise(),
        kwaliteiten_callback=lambda: pages["KwaliteitenPage"].tkraise()

    )
    # Place each page in the same grid cell
    for page in pages.values():
        page.grid(row=0, column=0, sticky="nsew")

    # ─────────────────────────────────────────────────────────
    # 3) Create the sidebar
    # ─────────────────────────────────────────────────────────
    sidebar = ctk.CTkFrame(app, width=200, corner_radius=0, fg_color='#327bc3')
    sidebar.pack(side="left", fill="y")

    # 3a) "Home" button with icon, different default color
    btn_home = ctk.CTkButton(
        master=sidebar,
        text="Home",
        image=img_home,
        compound="left",
        command=lambda: pages["HomePage"].tkraise(),
        width=180,
        font=ctk.CTkFont('Calibri', weight='bold'),
        text_color='white',
        fg_color='#134B70',
        hover_color='#508C9B',
        corner_radius=8
    )
    btn_home.pack(pady=(15,6), padx=10)

    # 3b) "Analysecertificaten" button with icon
    btn_analysis = ctk.CTkButton(
        master=sidebar,
        text="Analysecertificaten",
        image=img_analysis,
        compound="left",
        command=lambda: pages["AnalysisPage"].tkraise(),
        width=180,
        font=ctk.CTkFont('Calibri', weight='bold'),
        text_color='white',
        fg_color='#134B70',
        hover_color='#508C9B',
        corner_radius=8
    )
    btn_analysis.pack(pady=6, padx=10)

    # 3c) "PDF's mergen" button with icon
    btn_merge = ctk.CTkButton(
        master=sidebar,
        text="PDF's mergen",
        image=img_merge,
        compound="left",
        command=lambda: pages["MergePage"].tkraise(),
        width=180,
        font=ctk.CTkFont('Calibri', weight='bold'),
        text_color='white',
        fg_color='#134B70',
        hover_color='#508C9B',
        corner_radius=8
    )
    btn_merge.pack(pady=6, padx=10)

    # 3d) "Kwaliteiten CSV file button with icon
    btn_kwali = ctk.CTkButton(
        master=sidebar,
        text="Kwaliteiten CSV file",
        image=img_kwali,
        compound="left",
        command=lambda: pages["KwaliteitenPage"].tkraise(),
        width=180,
        font=ctk.CTkFont('Calibri', weight='bold'),
        text_color='white',
        fg_color='#134B70',
        hover_color='#508C9B',
        corner_radius=8
    )
    btn_kwali.pack(pady=6, padx=10)

    # Start with HomePage visible
    pages["HomePage"].tkraise()

    app.mainloop()

if __name__ == "__main__":
    main()
