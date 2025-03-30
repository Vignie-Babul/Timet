from bs4 import BeautifulSoup
import html5lib 
import requests

import csv
import os
import json
import re
from typing import Generator
import urllib.request


class Timetable:
	def __init__(
			self,
			csv_source_url: str,
			file_name: str,
			json_file_name: str,
			otherdays_iterate_number: int,
			saturday_iterate_number: int,
		) -> None:

		self._csv_source_url = csv_source_url
		self._file_name = file_name
		self._json_file_name = json_file_name
		self._csv_url = ''
		self._otherdays_iterate_number = otherdays_iterate_number
		self._saturday_iterate_number = saturday_iterate_number

		self._timetable_dict = {}

	def _parse_csv_url(self) -> str:
		response = requests.get(self._csv_source_url)
		soup = BeautifulSoup(response.text, 'html5lib')

		raw_url = soup.find('a', {'title': re.compile(r'(https\S+)edit\?')}).text
		clear_url = re.search(r'(\S+)edit\?', raw_url).group(1)
		export_url = 'export?format=csv'

		return clear_url + export_url

	def _download_csv(self) -> None:
		urllib.request.urlretrieve(self._csv_url, self._file_name)

	def _delete_csv(self) -> None:
		if os.path.exists(self._file_name):
			os.remove(self._file_name)

	def _generate_lesson_chunk(self, lessons_row: list, groups: list) -> Generator[list, None, None]:
		groups_number = len(groups)
		groups_range = range(1, groups_number + 1)

		for group_number in groups_range:
			yield lessons_row[6*(group_number-1):6*group_number]

	def _convert_csv_to_dict(self) -> tuple[dict, str, str]:
		with open(self._file_name, 'r', encoding='utf-8', newline='') as csv_file:
			timetable = csv.reader(csv_file)
			timetable_gen = (i for i in timetable)

			groups = [group for group in next(timetable_gen) if group]
			next(timetable_gen) # skip headers
			timetable_dict = {group: {} for group in groups}

			days_iterate_numbers = (
				self._otherdays_iterate_number,
				self._otherdays_iterate_number,
				self._otherdays_iterate_number,
				self._otherdays_iterate_number,
				self._otherdays_iterate_number,
				self._saturday_iterate_number,
			)
			days = (
				(
					next(timetable_gen) for _ in range(iterate_number)
				) for iterate_number in days_iterate_numbers
			)

			for day in days:
				current_date = ''
				for lessons_row in day:
					for lesson_chunk, name in zip(
							self._generate_lesson_chunk(lessons_row, groups),
							groups
						):

						date = lesson_chunk[0]
						chunk_data = {
							'lesson_number': lesson_chunk[1],
							'note': lesson_chunk[2],
							'lesson_name': lesson_chunk[3],
							'teacher': lesson_chunk[4],
							'cabinet': lesson_chunk[5],
						}

						if chunk_data['lesson_number']:
							if date:
								current_date = date

							if current_date not in timetable_dict[name]:
								timetable_dict[name][current_date] = []

							timetable_dict[name][current_date].append(chunk_data)

			return timetable_dict

	def _save_json(self) -> None:
		with open(self._json_file_name, 'w', encoding='utf-8') as json_file:
			json.dump(self._timetable_dict, json_file, indent=4, ensure_ascii=False)

	def convert_csv_to_json(self) -> None:
		self._csv_url = self._parse_csv_url()
		self._download_csv()

		self._timetable_dict = self._convert_csv_to_dict()

		self._delete_csv()
		self._save_json()


class Reader():
	def __init__(self, json_file_name: str) -> None:
		print(json_file_name)