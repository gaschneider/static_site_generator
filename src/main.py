import os, shutil
from generatepage import generate_pages_recursive

def clear_directory(path):
    if not os.path.exists(path):
        return

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def copy_file_or_dir(from_path, to_path):
    is_file = os.path.isfile(from_path)
    if is_file:
        shutil.copy2(from_path, to_path)
        return
    
    if not os.path.exists(to_path):
        os.mkdir(to_path)

    for filename in os.listdir(from_path):
        file_path_from = os.path.join(from_path, filename)
        file_path_to = os.path.join(to_path, filename)
        copy_file_or_dir(file_path_from, file_path_to)

def copy_from_to(from_path, to_path):
    clear_directory(to_path)
    copy_file_or_dir(from_path, to_path)


def main():
    copy_from_to("./static","./public")
    generate_pages_recursive("./content", "template.html", "./public")

if __name__ == "__main__":
    main()