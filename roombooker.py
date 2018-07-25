import time
import getpass
import os
import platform
import json
import argparse
from selenium import webdriver
from cryptography.fernet import Fernet


class userInput():
    """Holds data submitted by the user"""
    def __init__(self, webDriver, institutionKey, username, password, uploadCsv):
        self.webDriver = webDriver
        self.institutionKey = institutionKey
        self.username = username
        self.password = password
        self.uploadCsv = uploadCsv
    
    def __str__(self):
        return "Details for uploading data to https://secure.schoolbooking.com/" + self.institutionKey \
                + "\nPath to CSV file: " + self.uploadCsv \
                + "\nUsername: " + self.username \
                + "\n\nPath to web driver: " + self.webDriver


def get_deets():
    """Capture user data"""
    # Chrome web driver
    webDriver = input("What's the path to the Chrome webdriver? (Leave blank to default to current directory) ")
    if not webDriver:
        dirPath = os.path.dirname(os.path.realpath(__file__))
        webDriver = os.path.join(dirPath, 'chromedriver.exe')
    
    # instition's instance of schoolbooking.com
    institutionKey = input("What's the institution key (for example exampleschool from https://secure.schoolbooking.com/exampleschool)? ")

    # CSV with timetable details 
    while True:
        uploadCsv = input("What's the path to the CSV file to upload? ")
        # check file format is CSV
        if uploadCsv[-4:] != '.csv':
            print("Invalid file format, please try again.")
        else:
            break
    
    # credentials 
    username = input("What's the username? ")
    password = getpass.getpass("What's the password? ")

    # pass to object and return to main programme
    return userInput(webDriver, institutionKey, username, password, uploadCsv)


def room_upload(userInput):
    """Logs into schoolbooking.com and uploads timetable date"""
    # spawn automated browser
    try:
        print("Launching web driver...")
        driver = webdriver.Chrome(executable_path=userInput.webDriver)
        driver.get('https://secure.schoolbooking.com/' + userInput.institutionKey)
        time.sleep(2)
    except:
        print("Failed to launch web driver. Check the file path is correct.")
        print("Quitting...")
        quit()

    try:
        # submit details to login form
        userElement = driver.find_element_by_id('username')
        userElement.send_keys(userInput.username)
        passElement = driver.find_element_by_id('password')
        passElement.send_keys(userInput.password)
        passElement.submit()

        # navigate to the import page
        driver.get('https://secure.schoolbooking.com/apps/administration/academic_index.php')
        driver.find_element_by_xpath("//a[contains(@onclick, 'academic_import')]").click()
        driver.find_element_by_xpath("//div[contains(@onclick, 'academic_import_1_browse.php?sims=no')]").click()

        # upload room booking csv data
        uploadElement = driver.find_element_by_id("filechoice")
        uploadElement.send_keys(userInput.uploadCsv)
        driver.find_element_by_id("button_on").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[contains(@onclick, 'info')]").click()
        driver.find_element_by_xpath("//div[contains(@onclick, 'academic_import_3_transfer.php')]").click()

        # sign out
        time.sleep(2)
        print("Signing out...")
        driver.get('https://secure.schoolbooking.com/apps/shared/signout.php')

    except:
        # inform user of process failure
        print('Failed to complete timetable upload.')

    finally:
        # close the browser
        print('Closing web driver...')
        driver.quit()


def config_manager():
    """The configuration manager for the timetable room booker"""
    # clear the terminal and start the manager
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        os.system('clear')
    elif platform.system() == 'Windows':
        os.system('cls')
    print("Welcome to the timetable uploader configuration manager\n" + "-" * 55, end = "\n\n")

    # main menu
    while True:
        newConfig = input("Would you like to set up a new configuration (n) or quit (q)? ")
        if newConfig == 'n':
            # check if there are pre-existing configurations
            if os.path.isfile('roomConfig.json'):
                print("There is already a config file set up. Creating a new one will overwrite the existing file.")
                confirm = input("Are you sure you want to continue (y/n)? ")
                if confirm == 'y':
                    break
                else:
                    print("Quitting...")
                    quit()
            else:
                break
        elif newConfig == 'q':
            print("Quitting...")
            quit()

    # set up new configuration
    if newConfig == 'n':
        config_writer()


def config_reader_general():
    """Extract generic pre-defined configuration data"""
    # extract config file data
    with open('roomConfig.json') as infile:
        config = json.load(infile)
    print("Configuration file found. Reading...")

    # extract general details
    webDriver = config['webdriver']
    institution = config['institution']
    return webDriver, institution


def config_reader_institution(institution, quiet):
    """Extract each institution pre-defined configuration data"""
    # get main data
    institutionKey = institution['institutionkey']
    uploadCsv = institution['uploadcsv']

    # check credentials are in config data
    if 'username' in institution:
        ncryptUsername = institution['username']
        ncryptPassword = institution['password']
        secret = institution['secret']

        # decrypt credentials
        cipher = Fernet(secret.encode())
        dcrptUsername = cipher.decrypt(ncryptUsername.encode())
        dcrptPassword = cipher.decrypt(ncryptPassword.encode())
        username = dcrptUsername.decode()
        password = dcrptPassword.decode()

    else:
        if quiet:
            print("No stored credentials detected. Quitting...")
            quit()
        else:
            # ask for user details
            username = input("What's the username? ")
            password = getpass.getpass("What's the password? ")
    
    # return to main programme
    return institutionKey, username, password, uploadCsv

        
def config_writer():
    """Writes configuration file to make regular use easier"""
    print("Setting up a new configuration")
    try:
        config = {}

        # Chrome web driver
        webDriver = input("What's the path to chromedriver.exe (default is just chromedriver.exe for same directory as this application)? ")
        if not webDriver:
            webDriver = 'chromedriver.exe'
        config['webdriver'] = webDriver

        # number of institutions
        while True:
            insts = input("How many separate institutions would you like to set this up for? ")
            try:
                if int(insts) > 0:
                    break
                elif int(insts) <= 0:
                    print('Invalid entry, please try again.')
            except:
                print("That's not a number! Please try again.")
        config['institution'] = []

        # iterate through institutions and add to configuration
        i = 1
        while i <= int(insts):
            print("")
            print("Setting up configuration for institution", int(insts))
            instDict = {}
            institutionKey = input("What's the institution key (for example exampleschool from https://secure.schoolbooking.com/exampleschool)? ")

            # CSV file for timetable data
            while True:
                uploadCsv = input("What's the path to the CSV file to upload? ")
                # check file format is CSV
                if uploadCsv[-4:] != '.csv':
                    print("Invalid file format, please try again.")
                else:
                    break
            instDict['institutionkey'] = institutionKey
            instDict['uploadcsv'] = uploadCsv

            # credentials
            creds = input("Would you like to store credentials (must have admin privileges on your instance of schoolbooking.com) (y/n)? ")
            if creds == 'y':
                username = input("What's the username? ")
                password = getpass.getpass("What's the password? ")
                secret = Fernet.generate_key()
                cipher = Fernet(secret)
                ncryptUsername = cipher.encrypt(username.encode()) # encode to bytes for cryptographic process
                ncryptPassword = cipher.encrypt(password.encode())
                instDict['username'] = ncryptUsername.decode() # decode to string to store in JSON format
                instDict['password'] = ncryptPassword.decode()
                instDict['secret'] = secret.decode()
            config['institution'].append(instDict)
            i += 1
    except:
        print("Failed to build configuration. Please try again.")
        print("Quitting...")
        quit()
    
    # write config to JSON file
    try:
        with open('roomConfig.json', 'w') as outfile:
            json.dump(config, outfile)
    except:
        print("Failed to write configuration to file. Please check permissions and try again.")
        print("Quitting...")
        quit()


def main():
    print("Timetable to the school booking system uploader\n" + "-" * 55, end="\n\n")
    # define command line arguments
    parser = argparse.ArgumentParser(description="upload timetable data to the school room booking system")
    parser.add_argument("-c", "--configure", help="configure this application for your institution", action="store_true")
    parser.add_argument("-n", "--noconfig", help="run the application without using a configuration file", action="store_true")
    parser.add_argument("-q", "--quiet", help="run the application without asking for user input", action="store_true")
    args = parser.parse_args()

    # run configuration manager
    if args.configure:
        config_manager()

    # run room uploader without using a configuration file
    elif args.noconfig:
        data = get_deets()
        room_upload(data)
    
    # read config file and upload timetable data without issuing user prompts
    elif args.quiet:
        try:
            webDriver, institution = config_reader_general()
            for inst in institution:
                try:
                    institutionKey, username, password, uploadCsv = config_reader_institution(inst, args.quiet)
                    data = userInput(webDriver, institutionKey, username, password, uploadCsv)
                    room_upload(data)
                except:
                    print("Failed to read institution data.")
        except:
            print("No configuration file found. Quitting...")
            quit()

    # read config file and upload timetable data to the school booking system
    else:
        try:
            webDriver, institution = config_reader_general()
            for inst in institution:
                try:
                    institutionKey, username, password, uploadCsv = config_reader_institution(inst, False)
                    data = userInput(webDriver, institutionKey, username, password, uploadCsv)
                except:
                    print("Failed to read institution data.")
                    check = input("Would you like to enter details manually (y/n)? ")
                    if check == 'y':
                        data = get_deets()
                    else:
                        print("Quitting...")
                        quit()
                finally:
                    room_upload(data)
        except:
            print("No configuration file found.\n")
            check = input("Would you like to enter details manually (y/n)? ")
            if check == 'y':
                data = get_deets()
                room_upload(data)
            else:
                print("Quitting...")
                quit()


if __name__ == '__main__':
    main()