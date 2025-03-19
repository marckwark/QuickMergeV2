# File: utils/pages/home_page_web.py
def display():
    """
    Injects the Home Page HTML into the element with id "home-content".
    """
    from js import document
    html = """
    <div class="home-page">
      <h2 style="color:#327bc3; font-family: 'Bahnschrift SemiLight'; font-size:24px; font-weight:bold; text-align:left; margin: 20px 0 10px 30px;">
        Toelichting op de tool
      </h2>
      <div class="section" style="margin: 20px 30px;">
         <button id="analysis-btn" class="btn">Analysecertificaten</button>
         <p style="font-size:16px; margin-top:5px;">
           Hiermee kun je kiezen welke analysecertificaten van de Y-schijf (of een andere map) naar de projectmap moeten worden gekopieerd. Bovendien worden al deze analysecertificaten ook samengevoegd in progressieve volgorde.
         </p>
      </div>
      <div class="section" style="margin: 20px 30px;">
         <button id="merge-btn" class="btn">PDF's mergen</button>
         <p style="font-size:16px; margin-top:5px;">
           Hiermee kun je kiezen welke PDF's bestanden samengevoegd moeten worden tot één bestand. Dit is handig om bijlagen voor de rapportage te maken.
         </p>
      </div>
      <div class="section" style="margin: 20px 30px;">
         <button id="kwaliteiten-btn" class="btn">Kwaliteiten CSV bestand</button>
         <p style="font-size:16px; margin-top:5px;">
           Hiermee kun je de SOR en PFAS toetsingen samenvoegen tot één CSV-bestand. Dit kun je in ArcGIS inladen voor een kwaliteiten shape.
         </p>
      </div>
    </div>
    """
    document.getElementById("home-content").innerHTML = html

    # Example event listeners (replace these with real navigation or processing)
    document.getElementById("analysis-btn").addEventListener("click", lambda e: print("Navigating to Analysis Page"))
    document.getElementById("merge-btn").addEventListener("click", lambda e: print("Navigating to Merge Page"))
    document.getElementById("kwaliteiten-btn").addEventListener("click", lambda e: print("Navigating to Kwaliteiten Page"))
