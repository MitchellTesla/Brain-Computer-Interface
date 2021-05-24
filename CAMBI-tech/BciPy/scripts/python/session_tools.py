"""Tools for viewing and debugging session.json data"""
# pylint: disable=invalid-name
import json
from bcipy.helpers.session import session_data, session_db, session_csv, session_excel


def main(data_dir: str, alphabet: str):
    """Transforms the session.json file in the given directory and prints the
    resulting json."""
    print(json.dumps(session_data(data_dir, alphabet), indent=4))


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Opens session.json file for analysis. Optionally creates a sqlite database summarizing the data.")

    parser.add_argument('-p',
                        '--path',
                        help='path to the data directory',
                        default=None)
    parser.add_argument('--db', help='create sqlite database', action='store_true')
    parser.add_argument('--csv', help='create a csv file from the database', action='store_true')
    parser.add_argument('--charts', help='create an Excel spreadsheet with charts', action='store_true')
    parser.add_argument('-a',
                        '--alphabet',
                        help='alphabet (comma-delimited string of items)',
                        default=None)

    args = parser.parse_args()
    path = args.path
    if not path:
        from tkinter import Tk
        from tkinter import filedialog

        root = Tk()
        root.withdraw()
        path = filedialog.askdirectory(parent=root,
                                       initialdir="/",
                                       title='Please select a directory')

    alp = None
    if args.alphabet:
        alp = args.alphabet.split(",")

    if args.db or args.csv or args.charts:
        session_db(path, alp=alp)
        if args.csv:
            session_csv()
        if args.charts:
            session_excel()
        if not args.db:
            os.remove('session.db')
    else:
        main(path, alp)
