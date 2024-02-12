import os
import math
import shutil

# run the user's program in our generated folders
os.chdir('module/root_folder')


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    # s = round(size_bytes / p, 2)
    s = int(size_bytes / p)
    return f"{s}{size_names[i]}"


def mv_action(command):
    if command == "mv":
        print("Specify the current name of the file or directory and the new location and/or name")
        return

    if command.startswith("mv "):
        parts = command.split()

        if len(parts) == 3:
            old_name = parts[1]
            new_name = parts[2]
            found = False

            if old_name.startswith('.'):
                ext, root = os.path.splitext(old_name)
                if not root and ext:
                    with os.scandir('.') as entries:
                        for entry in entries:
                            if entry.is_file() and entry.path.endswith(ext):
                                move_file(entry, new_name)
                                found = True
                        if not found:
                            ext_not_found(ext)
            elif os.path.exists(old_name):
                move_file(old_name, new_name)
            else:
                print("No such file or directory")
        else:
            print("Specify the current name of the file or directory and the new location and/or name")


def move_file(old_name, new_name):
    if os.path.isdir(new_name):
        try:
            shutil.move(old_name, new_name)
        except (shutil.SameFileError, shutil.Error):
            print(f"{os.path.basename(old_name)}already exists in this directory. Replace? (y/n)")
    elif not os.path.exists(new_name):
        shutil.move(old_name, new_name)
    else:
        print("The file or directory already exists")


def rm_action(command):
    if command == "rm":
        print("Specify the file or directory")
        return
    if command.startswith("rm "):
        args = command.split(" ", 2)[1]
        found = False

        if args.startswith("."):
            ext, root = os.path.splitext(args)
            if not root and ext:
                with os.scandir('.') as entries:
                    for entry in entries:
                        if entry.is_file() and entry.path.endswith(ext):
                            os.remove(entry)
                            found = True
                    if not found:
                        ext_not_found(ext)
        elif os.path.isfile(args):
            os.remove(args)
        elif os.path.isdir(args):
            shutil.rmtree(args)
        else:
            print("No such file or directory")


def ext_not_found(extension):
    print(f"File extension {extension} not found in this directory")


def cd_action(command):
    if command == "cd ..":
        os.chdir(os.path.dirname(os.getcwd()))
        print(os.path.basename(os.getcwd()))

    elif command.startswith("cd "):
        path = command.split(" ", 1)[1]
        try:
            os.chdir(path)
            print(os.path.basename(os.getcwd()))
        except OSError:
            print("Invalid command")


def ls_action(command):
    if command.endswith("-l"):
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_dir():
                    print(entry.name)
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_file():
                    print(entry.name, os.stat(entry).st_size)
    elif command.endswith(" -lh"):
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_dir():
                    print(entry.name)
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_file():
                    print(entry.name, convert_size(os.stat(entry).st_size))
    elif command == "ls":
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_dir():
                    print(entry.name)
        with os.scandir('.') as entries:
            for entry in entries:
                if entry.is_file():
                    print(entry.name)


def mkdir_action(command):
    parts = command.split()
    if len(parts) == 2:
        new_directory = parts[1]
        if not os.path.isdir(new_directory):
            os.mkdir(new_directory)
        else:
            print("The directory already exists")
    else:
        print("Specify the name of the directory to be made")


def cp_action(command):
    parts = command.split()
    if len(parts) == 1:
        print("Specify the file")
    elif len(parts) > 3:
        print("Specify the current name of the file or directory and the new location and/or name")
    elif len(parts) == 3:
        source = parts[1]
        destination = parts[2]
        if os.path.isdir(destination):
            try:
                if source.startswith('.'):
                    ext, root = os.path.splitext(source)
                    found = False

                    if not root and ext:
                        with os.scandir('.') as entries:
                            for entry in entries:
                                if entry.is_file() and entry.path.endswith(ext):
                                    destination_file = os.path.join(destination, entry)
                                    if not os.path.isfile(destination_file):
                                        shutil.copyfile(entry, destination_file)
                                        found = True
                                    else:
                                        print(f"{os.path.basename(entry)} already exists in this directory. Replace? "
                                              f"(y/n)")
                                        command = input()
                                        if 'y' == command:
                                            shutil.copyfile(entry, destination_file)
                                        else:
                                            cmd(command)
                            if not found:
                                ext_not_found(ext)
                elif os.path.isfile(source):
                    destination_file = os.path.join(destination, os.path.basename(source))
                    if not os.path.isfile(destination_file):
                        shutil.copyfile(source, destination_file)
                    else:
                        print(f"{os.path.basename(source)} already exists in this directory. Replace? "
                              f"(y/n)")
                        command = input()
                        if 'y' == command:
                            shutil.copyfile(source, destination_file)
                        else:
                            cmd(command)
            except (shutil.SameFileError, shutil.Error):
                print(f"{os.path.basename(source)} already exists in this directory")
        elif not os.path.exists(source):
            print("No such file or directory")


def cmd(command):
    if command == "quit":
        exit()
    elif command == "pwd":
        print(os.getcwd())
    elif command.startswith("cd"):
        cd_action(command)
    elif command.startswith("rm"):
        rm_action(command)
    elif command.startswith("mv"):
        mv_action(command)
    elif command.startswith("ls"):
        ls_action(command)
    elif command.startswith("mkdir"):
        mkdir_action(command)
    elif command.startswith("cp"):
        cp_action(command)
    else:
        print("Invalid command")


def main():
    print("Input the command")

    while True:
        command = input()
        cmd(command)


if __name__ == "__main__":
    main()
