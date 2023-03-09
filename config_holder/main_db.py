from dotenv import dotenv_values

config = dotenv_values(".env")

forex_db = config["SQLITE_DB"]
user_data_table = "USER_DATA"
bids_table = "BIDS_SUMMARY"
active_bids_table = "ACTIVE_BIDS"
cancelled_bids_table = "CANCELLED_BIDS"
fulfilled_bids_table = "FULFILLED_BIDS"
pending_requests_table = "PENDING_REQUESTS"
