import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMessageBox, QPushButton, QLineEdit, QVBoxLayout, QCheckBox
from PyQt6 import uic
from datetime import timedelta

from util.configure import ConfigureManager
from util.subject import SubjectManager
import util


class MainWindows(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        uic.loadUi("./view/main.ui", self)

        self.cm = ConfigureManager()
        self.sm = SubjectManager(self.cm.subjects)
        self.today_iso = self.sm.now.isoformat()
        self.checkBox_holder = [[],[],[]]
        self.vl_list = [self.vl_1, self.vl_2, self.vl_3]
        # self.le_add_list = [self.le_add1, self.le_add2, self.le_add3]

        self.initBtn()

        try:
            self.initView()
        except Exception as e:
            print(e)
        except KeyError as e:
            print(e)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:

        self.btn_saveAndDelControl()
        return super().closeEvent(a0)

    def initView(self):

        # view with agenda
        if self.today_iso not in self.sm.schedule:
            self.lbl_warn.setText("Please add TODAY's agenda")
            raise Exception("Agenda not exist")
        elif self.sm.schedule[self.today_iso] == []:
            self.lbl_warn.setText("Please add TODAY's agenda")
            raise KeyError("Today's agenda is empty")
        else:
            for sub in self.sm.schedule[self.today_iso]:  # 3 times
                if sub not in self.cm.subjects:
                    self.lbl_warn.setText("Please modify TODAY's agenda")
                    raise KeyError("Today's subjects spell wrong")

            # agenda ok
        if (self.sm.now + timedelta(days=1)).isoformat() not in self.sm.schedule:
            self.lbl_warn.setText("Please add agendas after today")
        else:
            self.lbl_warn.setText("Feel good today")

        # view after agenda setting up
        self.lbl_n1.setText(self.sm.schedule[self.today_iso][0])
        self.lbl_n2.setText(self.sm.schedule[self.today_iso][1])
        self.lbl_n3.setText(self.sm.schedule[self.today_iso][2])
        self.cb_n1.addItems(self.cm.subjects)
        self.cb_n1.addItem("")
        self.cb_n1.setCurrentText(self.sm.schedule[self.today_iso][0])
        self.cb_n2.addItems(self.cm.subjects)
        self.cb_n2.addItem("")
        self.cb_n2.setCurrentText(self.sm.schedule[self.today_iso][1])
        self.cb_n3.addItems(self.cm.subjects)
        self.cb_n3.addItem("")
        self.cb_n3.setCurrentText(self.sm.schedule[self.today_iso][2])
        self.lbl_date.setText("Day Now " + self.today_iso)
        self.resetCheckBoxLayout()

    def initBtn(self):

        self.btn_save_del.clicked.connect(self.btn_saveAndDelControl)
        self.cw_calendar.clicked.connect(self.btn_findAgenda)
        self.btn_mdAgenda.clicked.connect(self.btn_modifyAgenda)
        self.btn_add1.clicked.connect(lambda: self.btn_add(0, self.le_add1))
        self.btn_add2.clicked.connect(lambda: self.btn_add(1, self.le_add2))
        self.btn_add3.clicked.connect(lambda: self.btn_add(2, self.le_add3))

    def btn_findAgenda(self):

        selected_date = self.cw_calendar.selectedDate().toPyDate().isoformat()

        try:
            self.cb_n1.setCurrentText(self.sm.schedule[selected_date][0])
        except (IndexError, KeyError) as e:
            self.cb_n1.setCurrentText("")

        try:
            self.cb_n2.setCurrentText(self.sm.schedule[selected_date][1])
        except (IndexError, KeyError) as e:
            self.cb_n2.setCurrentText("")

        try:
            self.cb_n3.setCurrentText(self.sm.schedule[selected_date][2])
        except (IndexError, KeyError) as e:
            self.cb_n3.setCurrentText("")

    def btn_modifyAgenda(self):

        selected_date = self.cw_calendar.selectedDate().toPyDate()
        try:
            agenda = [
                self.cb_n1.currentText(),
                self.cb_n2.currentText(),
                self.cb_n3.currentText(),
            ]
            for a in agenda:
                if a == "":
                    raise ValueError("Donot input empty string")

            self.sm.setSchedule(selected_date, agenda)

        except ValueError as e:
            QMessageBox.critical(
                self,
                "課目錯誤",
                "科目不可空白",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Close,
            )

    def btn_add(self, sub_index, le: QLineEdit):

        try:
            if le.text() == "":
                raise ValueError("Please input some words")

            self.sm.addReminder(self.sm.schedule[self.today_iso][sub_index], le.text())
            print(
                f"add '{le.text()}' to {self.sm.schedule[self.today_iso][sub_index]}"
            )

            self.resetCheckBoxLayoutEach(sub_index, self.vl_list[sub_index], self.checkBox_holder[sub_index])

        except ValueError as e:
            text = "something wrong here"

            if str(e) == "Please input some words":
                text = "內容不可以空白"
            elif str(e) == "Dup reminder":
                text = "請不要重複輸入"

            QMessageBox.critical(
                self,
                "備忘錄錯誤",
                text,
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Close,
            )

        except KeyError as e:
            print(e)

        finally:
            le.setText("")

    def resetCheckBoxLayout(self):

        self.resetCheckBoxLayoutEach(0, self.vl_list[0], self.checkBox_holder[0])
        self.resetCheckBoxLayoutEach(1, self.vl_list[1], self.checkBox_holder[1])
        self.resetCheckBoxLayoutEach(2, self.vl_list[2], self.checkBox_holder[2])

    def resetCheckBoxLayoutEach(self, sub_index, vl: QVBoxLayout, holder: list):

        for cb in holder:
            # print(cb)
            vl.removeWidget(cb)
            cb.deleteLater()
            cb = None
        holder.clear()

        sub = self.sm.schedule[self.today_iso][sub_index]
        for r in self.sm.on[sub]:
            tmp_checkbox = QCheckBox()
            font = QtGui.QFont()
            font.setPointSize(10)
            tmp_checkbox.setFont(font)
            tmp_checkbox.setText(r)
            holder.append(tmp_checkbox) # TODO: error here, seems as holder is a local var # TODO: make everything simple to use
            vl.addWidget(holder[-1])

        # print("self.holder_1:", self.checkBox_holder[0])

    def deleteCheckBox(self, text, vl: QVBoxLayout, holder: list):

        target_holder_i = 0
        for i in range(len(holder)):
            if holder[i].text() == text:
                target_holder_i = i
                break

        widget = holder[target_holder_i]
        vl.removeWidget(widget)
        widget.deleteLater()
        widget = None
        del holder[target_holder_i]

    def btn_saveAndDelControl(self):

        sub1_checked = []
        sub2_checked = []
        sub3_checked = []

        for cb in self.checkBox_holder[0].copy():
            if cb.isChecked():
                sub1_checked.append(cb.text())
                self.deleteCheckBox(cb.text(), self.vl_list[0], self.checkBox_holder[0])
        for cb in self.checkBox_holder[1].copy():
            if cb.isChecked():
                sub2_checked.append(cb.text())
                self.deleteCheckBox(cb.text(), self.vl_list[1], self.checkBox_holder[1])
        for cb in self.checkBox_holder[2].copy():
            if cb.isChecked():
                sub3_checked.append(cb.text())
                self.deleteCheckBox(cb.text(), self.vl_list[2], self.checkBox_holder[2])

        # deleteWidget after changing of self.on[] data make "RuntimeError: wrapped C/C++ object of type QCheckBox has been deleted"
        self.sm.setRemindersToFinished(self.sm.schedule[self.today_iso][0], sub1_checked)
        self.sm.setRemindersToFinished(self.sm.schedule[self.today_iso][1], sub2_checked)
        self.sm.setRemindersToFinished(self.sm.schedule[self.today_iso][2], sub3_checked)
        print(f"delete {sub1_checked} from {self.sm.schedule[self.today_iso][0]}")
        print(f"delete {sub2_checked} from {self.sm.schedule[self.today_iso][1]}")
        print(f"delete {sub3_checked} from {self.sm.schedule[self.today_iso][2]}")

        self.sm.saveFile()
        self.resetCheckBoxLayout()


if __name__ == "__main__":

    util.precheckFolder("./db_files/config")
    util.precheckFolder("./db_files/data")

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindows()
    window.show()
    app.exec()

