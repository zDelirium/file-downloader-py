import subprocess
import os

subprocess.run('clear')

# Welcome message
welcome_message = '\nHello ' + os.environ['USER'] + "!\n\n" + 'This program will let you downloads multiple files at once in your local machine using the curl command.\n'

print(welcome_message)

# Ask user if they want to proceed or not
user_proceed_input = input('Are you ready to proceed? (y/n) ')

while user_proceed_input is 'y':
    
    # Get Downloads folder directory
    download_dir = str(os.environ['HOME']) + '/Downloads'
    
    # Ask user if they want to continue with the Downloads directory
    print('\nBy default, the files will be downloaded in ' + download_dir + ' folder')
    user_dir_input = input('Do you want to continue with this directory? (y/n) ')

    # Ask user for alternate directory if not
    if user_dir_input is 'n':
        user_dir_input = input('\nPlease enter the desired directory path with a \"/\" at the beginning for a path from ' +  str(os.environ['HOME']) + '\nor without it for a path from' + os.getcwd() + ' :\n')
        if user_dir_input[0] is '/':
            download_dir = str(os.environ['HOME']) + user_dir_input 
        else:
            download_dir = os.getcwd() + "/" + user_dir_input
            
    # Print download directory
    print('\nThe files will be downloaded in ' + download_dir + '\n')
    
    # TODO Prompt user to enter curl command arguments
    
    # TODO Implement curl command
    
    # TODO Ask if user wants to proceed again
    user_proceed_input = 'n'

# TODO Maybe be able to choose the destination folder (like Downloads for example) 
'''
sut_url = 'https://static.wikia.nocookie.net/iz-one/images/4/4c/One-reeler_Digital.jpg'
sut_filename = 'izone-pic.jpg'

# default_dir = 'output'
curl_flag = '-o'

args = ['curl', curl_flag, sut_filename, sut_url]

# Create the output directory if it does not exist already
# This may change
# subprocess.run(['mkdir', default_dir])


# Execute the curl command
# subprocess.Popen(args, cwd='output').wait()
'''

# Closing message
print("\n\nSee you next time!\n\n\n")