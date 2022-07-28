##
# configure:
#   subjects
# datetime: (json)
#   class_targets

from pathlib import Path
import os


def precheckFolder(loc):

    Path(f"{loc}").mkdir(parents=True, exist_ok=True)


def findLatestFile(dir, end_with):

    latest_file_date = ""
    latest_file_num = 0

    for file in os.listdir(dir):
        if file.endswith(end_with):
            tmp_split = str(file).split("-")
            tmp_split_date = tmp_split[0]
            tmp_split_num = int(tmp_split[1].split(".")[0])

            if latest_file_date == "":  # first file
                latest_file_date = tmp_split_date
                latest_file_num = tmp_split_num
            elif latest_file_date < tmp_split_date:  # not first file
                latest_file_date = tmp_split_date
                latest_file_num = tmp_split_num
            elif latest_file_date == tmp_split_date and latest_file_num < tmp_split_num:
                latest_file_num = tmp_split_num

    if latest_file_date == "":
        raise LookupError("Find no file")

    latest_file = latest_file_date + "-" + str(latest_file_num) + end_with
    latest_file = os.path.join(dir, latest_file)

    return latest_file
