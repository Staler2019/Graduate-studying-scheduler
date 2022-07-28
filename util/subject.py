import json
from datetime import date
import sys
from typing import List

import util

# file: "{yyyymmdd-number}.json"
# {"sub1": {"on":[], "off": []}}


class SubjectManager:
    def __init__(self, subjects):

        super().__init__()
        self.subjects = subjects
        self.on = {}
        self.off = {}
        self.schedule = {}
        self.now = date.today()
        self.new_file_num = 1
        try:
            self.url = util.findLatestFile("./db_files/data", ".json")
            print("Now reading date:", self.url)

            # compare daytime or create new file
            tmp_split = self.url.split("\\")[-1].split("-")
            tmp_date = tmp_split[0]
            self.file_date = date(int(tmp_date[0:4]), int(tmp_date[4:6]), int(tmp_date[6:8]))
            self.file_num = int(tmp_split[1].split(".")[0])
            if self.now < self.file_date:
                print("There's a new file after today, please modify it")
                sys.exit()

            if self.now == self.file_date:
                self.new_file_num = self.file_num + 1

            with open(self.url, "r", encoding="utf-8") as f:
                data = json.load(f)
                for s in self.subjects:
                    self.on[s] = data[s]["on"] if (s in data) else []
                    self.off[s] = data[s]["off"] if (s in data) else []
                self.schedule = data["schedule"]

        except LookupError as e:  # setup new file
            print("Setting up first data file...")
            for s in self.subjects:
                self.on[s] = []
                self.off[s] = []

    def saveFile(self):

        file_name = (
            f"./db_files/data/{self.now.strftime('%Y%m%d')}-{self.new_file_num}.json"
        )

        out_dict = {}
        out_dict["schedule"] = self.schedule

        for s in self.subjects:
            out_dict[s] = {"on": self.on[s], "off": self.off[s]}

        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(out_dict, f, indent=4, ensure_ascii=False)

        self.new_file_num += 1

    def setSchedule(self, day: date, subjects: list):

        self.schedule[day.isoformat()] = subjects

    def addReminder(self, sub: str, reminder: str):

        if sub in self.subjects:
            if reminder in self.off[sub]:
                self.off[sub].remove(reminder)
            if reminder not in self.on[sub]:
                self.on[sub].append(reminder)
            else:
                raise ValueError("Dup reminder")
        else:
            raise KeyError(f"{sub}, no such subject")

    def setRemindersToFinished(self, sub: str, reminders: List[str]):

        if sub in self.subjects:
            for r in reminders:
                if r not in self.on[sub]:
                    RuntimeError(f"Each reminder should be found in self.on[{sub}]")

            for r in reminders:
                self.on[sub].remove(r)
                if r not in self.off[sub]:
                    self.off[sub].append(r)
        else:
            raise KeyError(f"{sub}, no such subject")
