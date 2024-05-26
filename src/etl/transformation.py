import pandas as pd


class Transformation:
    def __init__(self, file_path):
        self.df = None
        self.v_file_format = ""
        self.file_path = file_path

    def file_format(self, file_format):
        self.v_file_format = file_format
        return self

    def read_file(self):
        if self.v_file_format == 'csv':
            self.df = pd.read_csv(self.file_path)
        else:
            raise ValueError("File Format not found!")
        return self

    def remove_null(self):
        self.df.dropna(inplace=True)
        return self

    def remove_duplicate(self):
        self.df.drop_duplicates(inplace=True)
        return self

    def remove_substring(self, column, old_string_regex, new_string):
        self.df[column] = self.df[column].replace(old_string_regex, new_string)
        return self

    def cast(self, column, dt):
        self.df = self.df.astype({column: dt})
        return self

    def generate_dict(self):
        return self.df.to_dict("records")
