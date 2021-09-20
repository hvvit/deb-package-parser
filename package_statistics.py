#!/usr/bin/env python3
import sys
import urllib.request
import gzip

#function to open the file in cache and not download in a location
def download(url):
    try:
        return urllib.request.urlopen(url)
    except:
        print("Error occured while fetching file")
        exit()

#function to update the dict package, if the package is present, in dict
#update the counter if not then add package to the dict and init it with 1
def update_packages(packages,  item):
    if item in packages:
        current_count = packages.get(item)
        packages[item] = current_count + 1
    else:
        packages[item] = 1


def get_top_ten_packeges(arch_type):

    base_url = "http://ftp.uk.debian.org/debian/dists/stable/main/Contents-"
    #form the url here
    url = base_url + arch_type + ".gz"

    #init empty packages dict
    packages = {}

    #open the url in cache
    handle = download(url)

    try:
        #pass the handle to fileopject and read compressed line one by one
        with gzip.GzipFile(fileobj=handle, mode="rb") as file:
            for line in file:
                #decode and split to get package name and remove the section
                package = line.decode('utf-8').split()[1]
                update_packages(packages, package)
    except:
        print("Error occured while parsing file")

    #create a list of sorted keys from pacakges dict which is in reverse order,
    #and using value of occurance to sort the keys
    sorted_packages = sorted(packages, key=packages.get, reverse=True)

    #iterate over first 10 sorted keys in the list
    index = 1
    for item in sorted_packages[:10]:
        print("%d. %s %d" % (index, item.split('/')[-1], packages[item]))
        index = index + 1

if __name__ == "__main__":
    #checking for the length of the arguments provided and if length is greater than 1
    #assign 1st variable to arch_type
    if len(sys.argv) > 1:
        arch_type = sys.argv[1]
        get_top_ten_packeges(arch_type)
    else:
        print("ARCH TYPE arguments not provided")
