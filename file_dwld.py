import subprocess
import os

'''
Clear console and display welcoming message
'''
def display_welcome_message():
    # Welcome message
    subprocess.run('clear')
    welcome_message = '\nHello {}!\n\nThis program will let you downloads multiple files at once in your local machine using the curl command.\n'.format(
        os.environ['USER'])

    print(welcome_message)


'''
Validate that the user can properly answers yes/no questions
'''
def validate_yes_no_answer(init_question, yes_no_answers=['y', 'n']):
    user_input = input(init_question).strip()
    while user_input not in yes_no_answers:
        user_input = input('Please enter \'y\' (yes) or \'n\' (no): ').strip()
    return user_input


'''
Prompts user to choose the download path of the files
'''
def select_dlwd_path():
    home_env_var = 'HOME'
    
    # Get Downloads folder directory
    download_dir = '{}/Downloads'.format(os.environ[home_env_var])

    # Ask user if they want to continue with the Downloads directory
    print('\nBy default, the files will be downloaded in {} folder'.format(download_dir))
    user_dir_input = validate_yes_no_answer(
        'Do you want to continue with this directory? (y/n) ')

    # Ask user for alternate directory if not
    if user_dir_input is 'n':
        user_dir_input = input(
            '\nPlease enter the desired directory path with a \"/\" at the beginning for a path from {}\nor without it for a path from the current working directory {}\nTo download in current working directory, leave it blank :\n'.format(os.environ[home_env_var], os.getcwd())).strip()
        if not user_dir_input:
            download_dir = os.getcwd()
        elif user_dir_input[0] is '/':
            download_dir = '{}{}'.format(home_env_var, user_dir_input)
        else:
            download_dir = '{}/{}'.format(os.getcwd(), user_dir_input)

    # Print download directory
    print('\nThe files will be downloaded in {}\n'.format(download_dir))

    return download_dir


'''
Get arguments for curl command. 
'''
def get_curl_args():
    args = []
    nb_of_files = 0
    user_continue_input = 'y'

    print('It is now time to add the files to download. If you do not want to name the file, leave its name blank. Else make sure you put the right extension at the end.\n')

    # TODO Modify code so that args is a 2d list that contains each curl command for a file each
    while user_continue_input:
        nb_of_files += 1
        # Input file name if there is any
        file_name = input('Enter the name of file {}:\n'.format(nb_of_files)).strip()

        # Input download link
        url_link = input('Enter the download url link of file {}:\n'.format(nb_of_files)).strip()
        while not url_link.startswith('https://'):
            url_link = input('Please enter a https url link:\n').strip()
            

        # Add to approriate args to curl command
        if file_name:
            args.append('-o')
            args.append(file_name)
        else:
            args.append('-O')
        args.append(url_link)

        # TODO Ask user if they want to continue
        user_continue_input = validate_yes_no_answer('Do you want to continue adding files? (y/n) ')

        # TODO Have the user verify if all files are there. If not, continue adding files
        #user_continue_input = 'n'
        
    print('The program will download {}.\n'.format(nb_of_files))

    # Return args and nb of files
    return args, nb_of_files


'''
Display closing message
'''
def display_closing_message():
    print("\n\nSee you next time!\n\n")


'''
START of program
'''
display_welcome_message()

# Ask user if they want to proceed or not
user_proceed_input = validate_yes_no_answer('Are you ready to proceed? (y/n) ')

while user_proceed_input is 'y':

    # Select download destination folder
    download_dir = select_dlwd_path()

    # TODO Prompt user to enter curl command arguments
    args, nb_of_files = get_curl_args()

    # TODO Implement curl command (must decide between run and popen)
    # https://www.geeksforgeeks.org/curl-command-in-linux-with-examples/?ref=lbp
    # print("\n\nDownload has finished!\n\n")
    # subprocess.run(args).returncode

    # Ask if user wants to proceed again
    user_proceed_input = validate_yes_no_answer(
        'Do you want to try again? (y/n) ')


display_closing_message()
'''
END of program
'''