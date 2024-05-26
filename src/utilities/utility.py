from datetime import datetime
import shutil


def convert_list_to_dict(data_lst, schema):
    crypto_zip = zip(schema, data_lst)
    return dict(crypto_zip)


def archive_file(source_location, target_location):
    if target_location.exists():
        path = target_location.stem
        extension = target_location.suffix
        date_text = '_' + str(datetime.today())
        target_location = f"{path}{date_text}{extension}"
        shutil.move(source_location, target_location)
    else:
        shutil.move(source_location, target_location)
