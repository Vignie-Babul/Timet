from timet.src.timetable_api.config import TIMETABLE_CONFIG
from timet.src.timetable_api.timetable import Timetable, Reader


def parse_timetable() -> None:
	timetable = Timetable(**TIMETABLE_CONFIG)
	timetable.convert_csv_to_json()
	# timetable_reader = Reader(config.TIMETABLE_CONFIG['json_file_name'])