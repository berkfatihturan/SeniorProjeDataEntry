# search settings
MAX_TOWN_CODE = 970
MAX_PAGE_NUM = 51
MAX_RELOAD_NUM = 20
MAX_CITY_NUM = 81
BASE_URL = "https://www.arabam.com/ikinci-el?take=50&days=1"

# error timer settings
NETWORK_ERR_WAITING_TIME = 10
DATA_ER404_WAITING_TIME = 5

# email msg code [DONT CHANGE]
MSG_CODE_ERR = 0
MSG_CODE_PAGE_DONE = 1
MSG_CODE_TOWN_DONE = 2
MSG_CODE_PROCESS_DONE = 3
MSG_CODE_DATA_ERR = 4

# mail settings
FROM_EMAIL = "testtest12323123@gmail.com"
MAIL_PASSWORD = "rrau dgea szak cudw"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# sending who
USERS_MAIL = ["fatihliler32@gmail.com", "nihat0851@gmail.com"]

# db settings
DB_URI = "mongodb://localhost:27017/"
DB_NAME = "mydatabase"
DB_COLLECTION = "cars"

# Path location
SAVE_FILE_PATH = 'data/state.json'
MESSAGE_FILE_PATH = 'data/message_records.json'
CHROME_DRIVER_PATH = "/Users/berkfatihturan/Desktop/bft/Projects/Python/SeniorProject/SeniorProjeDataEntry/chromedriver"


