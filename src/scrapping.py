from bs4 import BeautifulSoup
from selenium import webdriver

URL = "http://www.georisques.gouv.fr/connaitre_les_risques_pres_de_chez_soi"\
      "/ma_maison_mes_risques/rapport?lon={lon}&lat={lat}&isCadastre=true"


def get_risks_from_coordinates(lat, lon):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)

    driver.get(URL.format(lat=lat, lon=lon))

    soup = BeautifulSoup(driver.page_source, "lxml")

    risks_mapping = {
        "Innondations": {"INN": []},
        "Installations Industrielles": {"INST": []},
        "Mouvements du sol et séismes": {"MVMT": [], "SEISM": []},
        "Radon et pollution du sol": {"POL": [], "RADON": []},
    }
    infos_commune = []

    for risk_category, risk_types in risks_mapping.items():
        for risk_type in risk_types:
            container = soup.find("div",
                                  {"id": "alea-{0}-container".format(risk_type)})
            if not container:
                continue

            risks = container.find("div", {"id": "risque-general-container-{0}".format(risk_type)})
            labels = risks.find_all("span", {"class": "label"})
            risks_mapping[risk_category][risk_type] = [label.text for label in labels]

    infos_commune = soup.find("div",
                              {"class": "hogan-container",
                               "id": "dest-commune-info"})

    infos_commune = [info.text for info in infos_commune.find_all("p")]

    return {"risks": risks_mapping,
            "infos_commune": infos_commune}
