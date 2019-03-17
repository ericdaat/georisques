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

    mapping = {
        "flood": {"INN": []},
        "industrial_installation": {"INST": []},
        "sismic_ground_mvt": {"MVMT": [], "SEISM": []},
        "radon_ground_polution": {"POL": [], "RADON": []}
    }

    for risk_category, risk_types in mapping.items():
        for risk_type in risk_types:
            container = soup.find("div", {"id": "alea-{0}-container".format(risk_type)})
            risks = container.find("div", {"id": "risque-general-container-{0}".format(risk_type)})
            labels = risks.find_all("span", {"class": "label"})
            mapping[risk_category][risk_type] = [label.text for label in labels]

    return mapping