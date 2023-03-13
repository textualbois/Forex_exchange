from dotenv import dotenv_values


config = dotenv_values(".env")

forex_exchange_db = config['MAIN_DB']