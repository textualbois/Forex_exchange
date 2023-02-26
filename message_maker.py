from rq import job  # нужно, чтобы задачи могли аксесить результат работы других задач.
					# т.к. результат работы первичной задачи
					# в момент добавления вторичной вероятно будет все ещё null
					# обходим это добавлением id первичной работы в аргументы


# Does the bid have stored values
def bid_has_values(bid_data):
	NEED_VAL = int(bid_data["NEED_VAL"])
	HAS_VAL = int(bid_data["HAS_VAL"])
	if NEED_VAL != 0 and HAS_VAL != 0:
		return True
	else:
		return False


def bid_string_without_values(bid_data):
	NEED_VAL = int(bid_data["NEED_VAL"])
	HAS_VAL = int(bid_data["HAS_VAL"])
	NEED_CUR = bid_data["NEED_CUR"]
	HAS_CUR = bid_data["HAS_CUR"]
	NEED_LOC = bid_data["NEED_LOC"]
	HAS_LOC = bid_data["HAS_LOC"]
	LOC_MAIN_ALIAS = bid_data["LOC_MAIN_ALIAS"]
	msg = (f"Вы находитесь в {LOC_MAIN_ALIAS}\n"
		   f"У вас {HAS_VAL:,} в {HAS_CUR} "
		   f"{trans_CUR_LOC(HAS_LOC)}\n"
		   f"Вам нужно {NEED_VAL:,} в {NEED_CUR} "
		   f"{trans_CUR_LOC(NEED_LOC)}\n"
		   f"Примерный курс пока нельзя указать без "
		   f"указания сумм желаемых и имеющихся валют")
	return msg


def bid_string_with_values(bid_data):
	NEED_VAL = int(bid_data["NEED_VAL"])
	HAS_VAL = int(bid_data["HAS_VAL"])
	NEED_CUR = bid_data["NEED_CUR"]
	HAS_CUR = bid_data["HAS_CUR"]
	NEED_LOC = bid_data["NEED_LOC"]
	HAS_LOC = bid_data["HAS_LOC"]
	LOC_MAIN_ALIAS = bid_data["LOC_MAIN_ALIAS"]
	msg = (f"Вы находитесь в {LOC_MAIN_ALIAS}\n"
		   f"У вас {HAS_VAL:,} в {HAS_CUR} "
		   f"{trans_CUR_LOC(HAS_LOC)}\n"
		   f"Вам нужно {NEED_VAL:,} в {NEED_CUR} "
		   f"{trans_CUR_LOC(NEED_LOC)}\n"
		   f"Примерный курс "
		   f"{HAS_CUR + '/' + NEED_CUR if HAS_VAL >= NEED_VAL else NEED_CUR + '/' + HAS_CUR}:\n"
		   f"{max(NEED_VAL / HAS_VAL, HAS_VAL / NEED_VAL):.4}\n"
		   f"Обратный курс "
		   f"{HAS_CUR + '/' + NEED_CUR if NEED_VAL < NEED_VAL else NEED_CUR + '/' + HAS_CUR}:\n"
		   f"{min(HAS_VAL / NEED_VAL, NEED_VAL / HAS_VAL):.4}\n")
	return msg


# forms bid data in to human message
def show_bids(bids_job_id, shown_data_job_id):
	print("show_bids:")
	bids_job = job.Job.fetch(bids_job_id)
	bids = bids_job.result
	offset_job = job.Job.fetch(shown_data_job_id)
	count = int(offset_job.result)
	print(bids)
	msg = ""
	for bid in bids:
		count += 1
		if bid_has_values(bid):
			msg = msg + f"{count}: {bid_string_with_values(bid)}\n"
		else:
			msg = msg + f"{count}: {bid_string_without_values(bid)}\n"
	return msg


# translates strings in DB to human text
def trans_CUR_LOC(location):
    if location == "NAL":
        return "Наличными"
    elif location == "RU":
        return "На Российской карте"
    elif location == "TR":
        return "на турецкой карте"