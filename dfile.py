import os 
import hashlib from multiprocessing import Pool, cpu_count from tkinter import Tk, filedialog 
 
# Select folder def select_folder(): root = Tk() root.withdraw() 
return filedialog.askdirectory(title="Select Folder") 
 
# Get all files recursively def get_all_files(folder): 
file_paths = [] for root, dirs, files in os.walk(folder): for file in files: 
file_paths.append(os.path.join(root, file)) return file_paths 
 
# Generate MD5 hash def get_file_hash(file_path): 
hasher = hashlib.md5() try: 
with open(file_path, 'rb') as f: while chunk := f.read(8192): 
hasher.update(chunk) 
return (file_path, hasher.hexdigest()) 
except: 
return (file_path, None) 
 
# Find duplicates using parallel processing def find_duplicates(file_paths): 
hash_dict = {} 
 
with Pool(cpu_count()) as pool: results = pool.map(get_file_hash, file_paths) 
 
for file_path, file_hash in results: if file_hash: 
hash_dict.setdefault(file_hash, []).append(file_path) 
 
return {h: paths for h, paths in hash_dict.items() if len(paths) 
> 1} 
 
# Main function def main(): 
folder = select_folder() if not folder: 
print("No folder selected") return 
 
print("Scanning folder...") files = get_all_files(folder) 
 
print("Processing files using parallel processing...") duplicates = find_duplicates(files) 
 
if duplicates: 
print("\nDuplicate Files Found:") for group in duplicates.values(): 
print("\nGroup:") for file in group: 
print(file) else: 
print("No duplicates found") 
 
if __name__ == "__main__": 
main() 
 
 
 
 
