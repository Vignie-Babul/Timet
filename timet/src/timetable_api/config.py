import re


TIMETABLE_SOURCE_URL = 'https://vk.com/@kolledge39-timetable'
TIMETABLE_FILE_NAME = 'timetable.csv'
TIMETABLE_ITERATE_NUMBERS = {
	'otherdays_iterate_number': 8,
	'saturday_iterate_number': 4,
}
TIMETABLE_JSON_FILE_NAME = 'timet\\data\\timetable.json'
TIMETABLE_CONFIG = {
	'csv_source_url': TIMETABLE_SOURCE_URL,
	'file_name': TIMETABLE_FILE_NAME,
	'json_file_name': TIMETABLE_JSON_FILE_NAME,
	**TIMETABLE_ITERATE_NUMBERS,
}