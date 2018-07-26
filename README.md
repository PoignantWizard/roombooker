===========================
#Room Booker
===========================

This app automates the process of uploading timetable data in a CSV
file to [https://www.schoolbooking.com](https://www.schoolbooking.com)

schoolbooking.com has its own interface (using the Zinet client) to 
push data from a student records system to an institution's instance 
of the web app. However, this method only supports a limited number 
of student records systems and those are only school-based systems. 

Sadly, colleges and others have to struggle with the manual upload 
of CSV data. This is a simple, but time consuming task, especially 
if your timetable changes a lot. 

That's where roombooker comes in! It can automatically navigate its 
way through your instance of the school booking web app and upload 
your CSV file. It can take user input each time its run or you can 
set up a configuration file, allowing it to be run by scheduled job. 

We're not affiliated with [https://www.schoolbooking.com](https://www.schoolbooking.com) in any way. 
We just needed an automated method of uploading timetable data that 
would work for our setup. 

##Dependencies 
-----------

roombooker requires chrome driver ([http://chromedriver.chromium.org/](http://chromedriver.chromium.org/)) 
to be in an accessible directory. 

You will also need Google Chrome installed [https://www.google.com/chrome/](https://www.google.com/chrome/) 
on the machine that will be running roombooker


##Quick start
-----------

1. Run roombooker to begin. 

2. It will ask you for a series of inputs: 
    * the file path the chrome driver
    * the URL to your instance of [schoolbooking.com](https://www.schoolbooking.com) 
    * the file path to your CSV file containing your timetable data
    * a username and password with permissions on your instance 
      of [schoolbooking.com](https://www.schoolbooking.com) to upload timetable data 

3. It will launch an automated instance of chrome, log into your 
   instance of [schoolbooking.com](https://www.schoolbooking.com), navigate to the upload page 
   and upload your timetable data. It will then log out and close 
   the browser. 

You may wish to use the -c command line switch to set up a local 
configuration file. roombooker will then read this when its run 
instead of asking for user input. You also have the choice of 
storing credentials or not. 

If roombooker can't find or read the configuration file for any 
reason, it will ask for user input instead. 

If you've set up a configuration file, but wish to run a one-off 
upload using different details, use the -n command line switch. 
This runs the application without using an existing configuration 
file. 

We recommend using the -q command line switch if running on a 
server as part of a scheduled job. This suppresses any prompts 
for user data that would otherwise hold up the process. Instead 
it will just close gracefully if it encounters any errors. It 
will still print an error message to the terminal though, to aid 
with debugging. Make sure you've set up a configuration file first, 
including stored credentials. 

Don't forget to generate a new CSV file before running roombooker, 
especially if running as part of a scheduled job. 

## Contributing
--------------

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our 
code of conduct. 

This app is written in python 3.6. 

## Authors
--------------

* **PoignantWizard** - *Initial work* 

## License
--------------

This project is licensed under the 3-Clause BSD License - see 
the [LICENSE.md](LICENSE.md) file for details. 