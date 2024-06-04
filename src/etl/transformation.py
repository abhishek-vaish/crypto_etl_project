class Transformation:
    def __init__(self, file_path, df):
        self.df = df
        self.v_file_format = ""
        self.file_path = file_path

    def file_format(self, file_format):
        self.v_file_format = file_format
        return self

    def remove_null(self):
        self.df.dropna(inplace=True)
        return self

    def remove_duplicate(self):
        self.df.drop_duplicates(inplace=True)
        return self

    def split_substring(self, column, old_string_regex):
        self.df[column] = \
            self.df[column].str.split(old_string_regex, n=0, regex=True).str[1]
        return self

    def cast(self, column, dt):
        self.df = self.df.astype({column: dt})
        return self

    def generate_dict(self):
        return self.df.to_dict("records")
