import os
import shutil
import time
import argparse
from datetime import datetime

def sync_folders(source_folder, replica_folder, interval, log_file):
    while True:
        # Perform synchronization
        sync_folder_contents(source_folder, replica_folder, log_file)

        # Wait for the specified interval
        time.sleep(interval)

def sync_folder_contents(source_folder, replica_folder, log_file):
    with open(log_file, 'a') as log:
        log.write(f"--- Sync started at {datetime.now()} ---\n")
        print(f"--- Sync started at {datetime.now()} ---\n")

        # Synchronize source folder to replica folder
        sync_result = sync_folder(source_folder, replica_folder, log)

        log.write(f"--- Sync ended at {datetime.now()} ---\n\n")
        print(f"--- Sync ended at {datetime.now()} ---\n\n")

        # Print the synchronization result
        print(sync_result)

def sync_folder(source_folder, replica_folder, log):
    sync_result = ""

    # Ensure replica folder exists
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
        sync_result += f"Replica folder created: {replica_folder}\n"

    # Iterate over items in source folder
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        replica_item = os.path.join(replica_folder, item)

        if os.path.isdir(source_item):
            # Recursively sync subfolders
            sync_result += sync_folder(source_item, replica_item, log)
        else:
            # Check if file exists in replica folder
            if not os.path.exists(replica_item):
                # Copy file from source to replica
                shutil.copy2(source_item, replica_item)
                sync_result += f"File copied: {source_item} to {replica_item}\n"
            else:
                # Check if file needs to be updated
                if os.path.getmtime(source_item) > os.path.getmtime(replica_item):
                    # Copy file from source to replica
                    shutil.copy2(source_item, replica_item)
                    sync_result += f"File updated: {source_item} to {replica_item}\n"

    # Remove items from replica folder that don't exist in source folder
    for item in os.listdir(replica_folder):
        replica_item = os.path.join(replica_folder, item)
        source_item = os.path.join(source_folder, item)

        if not os.path.exists(source_item):
            if os.path.isfile(replica_item):
                os.remove(replica_item)
                sync_result += f"File removed: {replica_item}\n"
            elif os.path.isdir(replica_item):
                shutil.rmtree(replica_item)
                sync_result += f"Folder removed: {replica_item}\n"

    return sync_result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Folder synchronization')
    parser.add_argument('source_folder', type=str, help='Path to source folder')
    parser.add_argument('replica_folder', type=str, help='Path to replica folder')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', type=str, help='Path to log file')
    args = parser.parse_args()

    sync_folders(args.source_folder, args.replica_folder, args.interval, args.log_file)
