import argparse
import shutil
import errno
import sys
import json
import os
import stat

def ignore_function(ignore):
    def _ignore_(path,names):
        ignored_names = []
        if ignore in names:
            ignored_names.append(ignore)
        return set(ignored_names)
    return _ignore_

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def copy_directory(src,dest, directory_to_ignore):
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        new_directory = shutil.copytree(src, dest + 'temp',ignore = ignore_function([directory_to_ignore, '.git/']))
        os.remove(dest + 'temp/.gitignore')
        ## on windows machines our git file is read only, so we add an error call back to force deletion
        shutil.rmtree(dest + 'temp' + '/.git/', onerror=remove_readonly )
        shutil.make_archive(dest,'zip',dest + 'temp')
        
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src,dest)
        else:
            print('Directory not copied. Error: %s' % e)

def update_json_file(json_path,prop_to_change, value):
    ## takes path to json file, finds the property and updates the value
    with open(json_path, "r") as jsonFile:
        data = json.load(jsonFile)

    tmp = data[prop_to_change]
    data[prop_to_change] = value

    with open("json_path", "w") as jsonFile:
        jsonFile.write(json.dumps(data))
        
parser  = argparse.ArgumentParser(description="zip up a file ignoring certain files")

parser.add_argument("directory_a", help="directory to zip")
parser.add_argument("directory_to_ignore", help="directory to ignore", nargs="?")
parser.add_argument("directory_b", help="name of new directory", nargs="?", default=sys.argv[1])

parser.add_argument("json_path", help="path to the json file in your directory", nargs="?")
parser.add_argument("property_to_update", help="property to update", nargs="?")
parser.add_argument("json_value", help="value to update to", nargs="?")


args = parser.parse_args()

directory_to_zip = args.directory_a
directory_to_ignore = args.directory_to_ignore
new_directory_name = args.directory_b;

if directory_to_zip:
    if args.json_path:
        if args.property_to_update:
            if args.json_value:
                update_json_file(args.json_path,args.property_to_update,args.json_value)
            else:
                print('Please input a value to update to')
        else:
            print('Please try again and submit a property to update ')
    copy_directory(directory_to_zip, new_directory_name, directory_to_ignore)
    shutil.rmtree(new_directory_name + 'temp', onerror=remove_readonly)
    print ('Your new zip file was created!')
else:
    print ("Please put in a directory name")