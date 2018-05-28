DELAY = 1
FILE_HLASY = "data/hlasy.h5"
FILE_KLUBY = "data/kluby.h5"
FILE_HLASY_METADATA = "data/hlasy_metadata.h5"
FILE_DEMAGOG = "data/demagog.h5"
FILE_ROZPRAVY = "data/rozpravy.pkl"
HDF_KEY = "data"

HLASY_STATS_MEANING = {"[Z]": "Za", "[P]": "Proti", "[N]": "Nehlasoval/a",
                       "[0]": "Neprítomný/á", "[?]": "Zdržal/a sa"}
HLASY_STATS_ORDER = ["[Z]", "[P]", "[?]", "[0]", "[N]"]
HLASY_STATS_VYSLEDOK = ["prešiel", "neprešiel"]
FILE_STATS_HLASY_PIE = "data/hlasy_pie.h5"

DEMAGOG_LABELS = ["Pravda", "Nepravda", "Zavádzanie", "Neoveriteľné"]
FILE_DEMAGOG_PIE = "data/demagog_pie.h5"

ROZPRAVY_COLUMNS = ["name", "type", "start_time", "end_time", "text"]
FILE_ROZPRAVY_APP = "data/rozpravy_app.h5"
ROZPRAVY_APP_LABELS = ["trvanie (hod.)", "počet slov"]
FILE_ROZPRAVY_DURATION = "data/rozpravy_duration.pkl"
