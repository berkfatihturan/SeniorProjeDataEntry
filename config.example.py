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
FROM_EMAIL = ""
MAIL_PASSWORD = "[use app password]"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
NOTIFICATIONS_ENABLED = True

# sending who, use array, example -> ["xx@xx.com","xx@xx.com"]
USERS_MAIL = []

# db settings
DB_URI = "mongodb://localhost:27017/"
DB_NAME = "mydatabase"
DB_COLLECTION = "cars"

# Path location
SAVE_FILE_PATH = './data/state.json'
MESSAGE_FILE_PATH = 'data/message_records.json'
# Fill with your driver path
CHROME_DRIVER_PATH = "/Users/berkfatihturan/Desktop/bft/Projects/Python/SeniorProject/SeniorProjeDataEntry/chromedriver"


