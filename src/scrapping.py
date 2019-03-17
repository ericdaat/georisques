from bs4 import BeautifulSoup
from selenium import webdriver

URL = "http://www.georisques.gouv.fr/connaitre_les_risques_pres_de_chez_soi"\
      "/ma_maison_mes_risques/rapport?lon={lon}&lat={lat}&isCadastre=true"

options = webdriver.ChromeOptions()
options.add_argument("headless")  # Headless so that Chrome does not open
global driver
driver = webdriver.Chrome(options=options)


def get_risks_from_coordinates(lat, lon):
    """ Scrap the website given the coordinates, and return the informations
    about the area concerned along with the declared risks.

    Arguments:
        lat {float} -- Latitude value
        lon {float} -- Longitude value

    Returns:
        tuple -- dict of results and a boolean telling whether we found
            informations or not.
    """

    # Scrap the url given lat and lon params
    driver.get(URL.format(lat=lat, lon=lon))

    # Parse the url content with Beautifulsoup to extract the HTML
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Build a base dict with the risks to be filled
    risks_mapping = {
        "Innondations": {"INN": []},
        "Installations Industrielles": {"INST": []},
        "Mouvements du sol et séismes": {"MVMT": [], "SEISM": []},
        "Radon et pollution du sol": {"POL": [], "RADON": []},
    }
    # Informations on commune to be filled
    infos_commune = []

    # Loop over the different kind of risks and find the appropriate
    # values in the HTML content
    for risk_category, risk_types in risks_mapping.items():
        for risk_type in risk_types:
            # risks are located within a container identified by its id field
            # e.g: concerning floods, the id equals `alea-INN-container`
            container = soup.find(
                "div",
                {"id": "alea-{0}-container".format(risk_type)}
            )
            if not container:
                continue

            # Within the container, we have another container that contains
            # the risks labels.
            risks = container.find(
                "div",
                {"id": "risque-general-container-{0}".format(risk_type)}
            )

            # We find all the labels within that last container
            labels = risks.find_all("span", {"class": "label"})

            # We remove the HTML tags by storing the `text` attribute
            risks_mapping[risk_category][risk_type] = \
                [label.text for label in labels]

    # Get informations on the commune corresponding to coordinates
    # They can be found within a container identified by a class
    # and an id
    infos_commune = soup.find(
        "div",
        {"class": "hogan-container", "id": "dest-commune-info"}
    )

    # Within this last container, get the labels as texts
    infos_commune = [info.text for info in infos_commune.find_all("p")]

    # If we found informations on commune and risks, consider that the
    # call was successfull and the boolean will be True. Otherwise False.
    has_found_results = labels and infos_commune
    results = {"risks": risks_mapping, "infos_commune": infos_commune}

    return results, has_found_results
