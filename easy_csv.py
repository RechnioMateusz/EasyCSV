# TODO: Add docstrings

import os
import csv

try:
    from .errors import CsvCreatorError
    from .utils import check_slice
except ImportError:
    from errors import CsvCreatorError
    from utils import check_slice


class CsvEditor():
    def __init__(self, path=None):
        self.path = path
        self.matrix = list()
        self.headers = list()
        is_csv_file = isinstance(path, str) and os.path.isfile(path)
        is_csv_file = is_csv_file and path.endswith(".csv")
        if is_csv_file:
            with open(path, "r") as csv_file:
                rows = list(csv.DictReader(f=csv_file))
                self.headers = list(rows[0])
                for row_id, row in enumerate(rows):
                    self.matrix.append(list())
                    for header in self.headers:
                        self.matrix[row_id].append(row[header])

    @property
    def rows_amount(self):
        return len(self.matrix)

    @property
    def columns_amount(self):
        return len(self.headers)

    def __str__(self):
        lengths = [len(header) for header in self.headers]
        for row in self.matrix:
            for i, cell in enumerate(row):
                cell_len = len(str(cell))
                if cell_len > lengths[i]:
                    lengths[i] = cell_len

        string = "+" + "+".join("-" * length for length in lengths) + "+\n"
        string += "|"
        for i, header in enumerate(self.headers):
            string += "{:^{length}}|".format(header, length=lengths[i])
        string += "\n"
        string += "+" + "+".join("-" * length for length in lengths) + "+\n"
        for row in self.matrix:
            string += "|"
            for i, cell in enumerate(row):
                string += "{:^{length}}|".format(cell, length=lengths[i])
            string += "\n"
        string += "+" + "+".join("-" * length for length in lengths) + "+\n"

        return string

    def get_row(self, index):
        if not 0 <= index < self.rows_amount:
            raise CsvCreatorError(
                msg="Invalid row index",
                desc=f"Is {index}. Should be between 0 and {self.rows_amount}"
            )

        for i, row in enumerate(self.matrix):
            if i == index:
                return row

    def get_rows(self, index, size):
        if size < 0:
            raise CsvCreatorError(msg="Size should be positive number")
        if index + size >= self.rows_amount:
            desc = f"index + size = {index + size}\t"
            desc += f"csv height = {self.rows_amount}"
            raise CsvCreatorError(
                msg="Index + size is bigger than csv height", desc=desc
            )

        rows = list()
        for i in range(index, index + size):
            rows.append(self.get_row(index=i))

        return rows

    def get_column(self, index):
        if not 0 <= index < self.columns_amount:
            desc = f"Is {index}. Should be between 0 and {self.columns_amount}"
            raise CsvCreatorError(
                msg="Invalid column index", desc=desc
            )

        column = list()
        for row in self.matrix:
            column.append(row[index])

        return column

    def get_columns(self, index, size):
        if size < 0:
            raise CsvCreatorError(msg="Size should be positive number")
        if index + size >= self.columns_amount:
            desc = f"index + size = {index + size}\t"
            desc += f"csv width = {self.columns_amount}"
            raise CsvCreatorError(
                msg="Index + size is bigger than csv width", desc=desc
            )

        columns = list()
        for i in range(index, index + size):
            columns.append(self.get_column(index=i))

        return columns

    def get_cell(self, row_id, column_id):
        if not 0 <= row_id < self.rows_amount:
            raise CsvCreatorError(
                msg="Invalid row index",
                desc=f"Is {row_id}. Should be between 0 and {self.rows_amount}"
            )
        if not 0 <= column_id < self.columns_amount:
            desc = f"Is {column_id}. "
            desc += f"Should be between 0 and {self.columns_amount}"
            raise CsvCreatorError(
                msg="Invalid column index", desc=desc
            )

        return self.matrix[row_id][column_id]

    def __getitem__(self, key):
        check_slice(key=key)

        start = isinstance(key.start, int)
        stop = isinstance(key.stop, int)
        step = isinstance(key.step, int)

        if start and not stop and not step:
            return self.get_row(index=key.start)
        if start and not stop and step:
            return self.get_rows(index=key.start, size=key.step)
        if not start and stop and not step:
            return self.get_column(index=key.stop)
        if not start and stop and step:
            return self.get_columns(index=key.stop, size=key.step)
        if start and stop and not step:
            return self.get_cell(row_id=key.start, column_id=key.stop)

        desc = "To get nth row use [n::]\n"
        desc += "To get nth + s rows use [n::s]\n"
        desc += "To get mth column use [:m:]\n"
        desc += "To get mth + s columns use [:m:s]\n"
        desc += "To get n x m cell use [n:m:]\n"
        raise CsvCreatorError(msg="Prohibited action!", desc=desc)

    # TODO: !!! ADD REST OF DESCRIPTIONS TO EXCEPTIONS !!!
    def set_row(self, index, data):
        if not 0 <= index < self.rows_amount:
            raise CsvCreatorError(msg="Invalid row index")
        if len(data) > self.columns_amount:
            raise CsvCreatorError(msg="New row is longer than csv width")

        for i in range(len(data), self.columns_amount):
            data.append(self.matrix[index][i])
        for i in range(len(self.matrix[index])):
            self.matrix[index][i] = data[i]

    def set_rows(self, index, size, data):
        if size < 0:
            raise CsvCreatorError(msg="Size should be positive number")
        if size != len(data):
            raise CsvCreatorError(msg="Size and data length are NOT equal")
        if index + size >= self.rows_amount:
            raise CsvCreatorError(msg="Index + size is bigger than csv width")
        if max([len(row) for row in data]) > self.columns_amount:
            raise CsvCreatorError(msg="Some row is longer than csv width")

        data_iter = 0
        for i in range(index, index + size):
            self.set_row(index=i, data=data[data_iter])
            data_iter += 1

    def set_column(self, index, data):
        if not 0 <= index <= self.columns_amount:
            raise CsvCreatorError(msg="Invalid row index")
        if len(data) > self.rows_amount:
            raise CsvCreatorError(msg="Column is longer than csv height")

        for i in range(len(data), self.rows_amount):
            data.append(self.matrix[i][index])
        for i, row in enumerate(self.matrix):
            new_row = row.copy()
            new_row[index] = data[i]
            self.matrix[i] = new_row

    def set_columns(self, index, size, data):
        if size < 0:
            raise CsvCreatorError(msg="Size should be positive number")
        if size != len(data):
            raise CsvCreatorError(msg="Size and data length are NOT equal")
        if index + size >= self.columns_amount:
            raise CsvCreatorError(msg="Index + size is bigger than csv width")
        if max([len(column) for column in data]) > self.rows_amount:
            raise CsvCreatorError(msg="Some column is longer than csv width")

        data_iter = 0
        for i in range(index, index + size):
            self.set_column(index=i, data=data[data_iter])
            data_iter += 1

    def set_cell(self, row_id, column_id, data):
        if not 0 <= row_id <= self.rows_amount:
            raise CsvCreatorError(msg="Invalid row index")
        if not 0 <= column_id <= self.columns_amount:
            raise CsvCreatorError(msg="Invalid column index")

        self.matrix[row_id][column_id] = data

    def __setitem__(self, key, data):
        check_slice(key=key)

        start = isinstance(key.start, int)
        stop = isinstance(key.stop, int)
        step = isinstance(key.step, int)

        if start and not stop and not step:
            self.set_row(index=key.start, data=data)
            return
        if start and not stop and step:
            self.set_rows(index=key.start, size=key.step, data=data)
            return
        if not start and stop and not step:
            self.set_column(index=key.stop, data=data)
            return
        if not start and stop and step:
            self.set_columns(index=key.stop, size=key.step, data=data)
            return
        if start and stop and not step:
            self.set_cell(row_id=key.start, column_id=key.stop, data=data)
            return

        msg = "Prohibited action!\n"
        msg += "To set nth row use [n::]\n"
        msg += "To set nth + s rows use [n::s]\n"
        msg += "To set mth column use [:m:]\n"
        msg += "To set mth + s columns use [:m:s]\n"
        msg += "To set n x m cell use [n:m:]\n"
        raise CsvCreatorError(msg=msg)

    def get_row_as_dict(self, index):
        if not 0 <= index <= self.rows_amount:
            raise CsvCreatorError(msg="Invalid row index")

        return dict(zip(self.headers, self.get_row(index=index)))

    def get_column_by_header(self, header):
        if header not in self.headers:
            raise CsvCreatorError("Given header is not in headers")

        header_id = self.headers.index(header)
        return [elem[header_id] for elem in self.matrix]

    def add_row_list(self, data):
        if not isinstance(data, (list, tuple)):
            raise CsvCreatorError(msg="Given data is not list nor tuple")
        if len(data) > self.columns_amount:
            raise CsvCreatorError(msg="Too much data")

        if len(data) < self.columns_amount:
            diff = self.columns_amount - len(data)
            data = data + ["", ] * diff
        self.matrix.append(list())
        for elem in data:
            self.matrix[-1].append(elem)

    def add_row_dict(self, data):
        if not isinstance(data, dict):
            raise CsvCreatorError(msg="Given data is not dict")
        if len(data) < self.columns_amount:
            raise CsvCreatorError(msg="Not enough cells to add")

        columns_to_add = 0
        for key in data:
            if key not in self.headers:
                self.headers.append(key)
                columns_to_add += 1

        for i, row in enumerate(self.matrix):
            self.matrix[i] = row + ["", ] * columns_to_add
        self.matrix.append(list())

        for header in self.headers:
            self.matrix[-1].append(data[header])

    def add_header(self, header):
        if not isinstance(header, str):
            raise CsvCreatorError(msg="Header is not string")
        if header in self.headers:
            raise CsvCreatorError(msg="Header already exist")

        self.headers.append(header)
        for i, row in enumerate(self.matrix):
            self.matrix[i] = row + ["", ]

    def add_headers(self, headers):
        if not isinstance(headers, (list, tuple)):
            raise CsvCreatorError(msg="Given headers are not list nor tuple")

        for header in headers:
            self.add_header(header=header)

    def add_column(self, header, column):
        if not isinstance(header, str):
            raise CsvCreatorError(msg="Header is not string")
        if not isinstance(column, (list, tuple)):
            raise CsvCreatorError(msg="Given column is not list nor tuple")
        if len(column) > self.rows_amount:
            raise CsvCreatorError(msg="Column is longer than csv height")

        if len(column) < self.rows_amount:
            diff = self.rows_amount - len(column)
            column = column + ["", ] * diff
        self.headers.append(header)
        for i in range(len(self.matrix)):
            self.matrix[i].append(column[i])

    def save(self, path=None):
        file_path = self.path
        if path is not None:
            if path.endswith(".csv"):
                file_path = path
            else:
                raise CsvCreatorError(msg="Given path does not end with .csv")

        with open(file_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(f=csv_file, fieldnames=self.headers)
            writer.writeheader()
            for i in range(len(self.matrix)):
                writer.writerow(self.get_row_as_dict(index=i))
