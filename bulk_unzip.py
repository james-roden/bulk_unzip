# -----------------------------------------------
# Project: bulk_unzip
# Name: bulk_unzip
# Purpose: Recursively searches directory for zip files and extracts them into folder. Deletes zip file if delete_flag
#          parameter is selected
# Version: 1.0
# Author: James M Roden
# Created: Nov 2020
# Python Version 3.6
# PEP8
# -----------------------------------------------

import click
import glob
import zipfile
import os


@click.command()
@click.option('--directory', prompt='Please enter the LAN folder to recursively query for zip files to unzip',
              help='Folder Path', type=click.Path(exists=True))
@click.option('--delete_flag', type=click.Choice(['Y', 'N'], case_sensitive=False),
              prompt='Delete successfully unzipped files?', help='Delete the .zip if successfully unzipped ~ Y or N')
def unzip(directory, delete_flag):
    """Recursively searches directory for zip files and extracts them into folder. Deletes zip file if delete_flag
    parameter is selected

    Builds an iterator containing all zip files in directory and sub-directory. Checks if zip file + _unzipped already
    exists. If if exists, it skips that zip file. If it doesn't exist, the zip file is extracted to _unzipped folder.
    If the delete_flag is Y, the zip file is deleted after successful extraction. It is not deleted if extraction was
    not successful.

    directory: Folder path to begin recursive search
    delete_flag: (Y or N) delete successfully extracted .zip file

    """

    zip_file_iter = glob.iglob(directory + '/**/*.zip', recursive=True)  # Build iterator

    # Zip File Counter
    count = 0

    for zip_file in zip_file_iter:

        path = os.path.dirname(zip_file)  # path to zip file
        name = os.path.basename(zip_file)  # zip filename
        unzipped_folder_name = name[:-4] + '_unzipped'
        unzipped_folder_path = os.path.join(path, unzipped_folder_name)

        # Check if <zip>_unzipped exists already
        if os.path.exists(unzipped_folder_path):
            click.echo('{} already exists'.format(unzipped_folder_name))
            continue

        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(unzipped_folder_path)

            click.echo('{} extracted to {}'.format(zip_file, unzipped_folder_path))
            count += 1

            if delete_flag.lower() == 'y':
                os.remove(zip_file)
                click.echo('{} DELETED'.format(zip_file))

        except zipfile.BadZipFile or zipfile.LargeZipFile:
            click.echo('Bad zip file or zip file too large: {} was skipped'.format(name))
            continue

    click.echo('{} zip files extracted'.format(count))
    input('Press Enter to exit')


if __name__ == '__main__':
    unzip()

