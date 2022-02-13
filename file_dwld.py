from distutils import command
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
    
    welcome_message = '{}Tip: For all yes/no answers, you can simply leave it blank to answer yes :)\n'.format(welcome_message)
    print(welcome_message)


'''
Validate that the user can properly answers yes/no questions. User can also answer yes by not entering anything
'''
def validate_yes_no_answer(init_question, yes_no_answers=['y', 'n']):
    user_input = input(init_question).strip()
    if not user_input:
        user_input = yes_no_answers[0]
    while user_input not in yes_no_answers:
        user_input = input('Please enter \'y\' (yes) or \'n\' (no): ').strip()
        if not user_input:
            user_input = yes_no_answers[0]
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
    if user_dir_input == 'n':
        user_dir_input = input(
            '\nPlease enter the desired directory path with a \"/\" at the beginning for a path from {}\nor without it for a path from the current working directory {}\nTo download in current working directory, leave it blank :\n'.format(os.environ[home_env_var], os.getcwd())).strip()
        if not user_dir_input:
            download_dir = os.getcwd()
        elif user_dir_input[0] == '/':
            download_dir = '{}{}'.format(home_env_var, user_dir_input)
        else:
            download_dir = '{}/{}'.format(os.getcwd(), user_dir_input)

    # Print download directory
    print('\nThe files will be downloaded in {}\n'.format(download_dir))

    return download_dir


'''
Get arguments for all curl commands. 
'''
def get_all_curl_cmd_args():
    commands = []
    user_continue_input = 'y'

    print('It is now time to add the files to download. If you do not want to name the file, leave its name blank. Else make sure you put the right extension at the end.')
    print('Note that for now the app does not ensure that there are no duplicate file names, so files with the same name may get overwritten.\n')

    while user_continue_input == 'y':
        args = []
        file_nb = len(commands) + 1
        args.append('curl')
        
        # Input download https or http url link
        # TODO may want to do stronger checks
        url_link = input('Enter the http or https url link of file {}:\n'.format(file_nb)).strip()
        while not url_link.startswith('https://') and not url_link.startswith('http://'):
            url_link = input('Please enter a http or https url:\n').strip()
            
        # Input file name if there is any. 
        # TODO Make sure that the user does not name any file the same
        # Make sure the user does not enter / in the file-name
        file_name = input('Enter the name of file {}:\n'.format(file_nb)).strip()
        while '/' in file_name:
            file_name = input('Please make sure to not enter a directory in the file name:\n').strip()

        # Add to approriate args to curl command
        if file_name:
            args.append('-o')
            args.append(file_name)
        else:
            args.append('-O')
        args.append(url_link)
        
        # Add curl command to the array of curl commands
        commands.append(args)

        # Ask user if they want to continue
        user_continue_input = validate_yes_no_answer('\nDo you want to continue adding files? (y/n) ')
        print()

    print('The program will download the following {} files:\n'.format(len(commands)))

    # Display name of files to be downloaded
    display_file_names(commands)

    print()
    # Return all commands and nb of files
    return commands

'''
Display the name of all files to be downloaded to the user in 2 columns
'''
def display_file_names(commands):
    # Get only name of files
    file_names = []
    for cmd in commands:
        file_names.append(cmd[2].split('/')[-1])

    
    # Display file names to be downloaded to user. 2 file names per row
    iterator = 0
    max_len = max(len(file_name) for file_name in file_names)
    while iterator < len(file_names):
        # Print a row
        if iterator % 2 == 1:
            print('{}{}'.format(file_names[iterator - 1].ljust(max_len + 5), file_names[iterator]))
            
        # Print the last leftover element if we have an odd number of files
        if iterator == len(file_names) - 1 and iterator % 2 == 0:
            print(file_names[iterator])
        
        iterator += 1

# '''
# Execute all curl commands and verify their status
# '''
# def execute_curl(commands, download_dir): 
#     for args in commands:
#         file_name = None
        
#         if args[1] == '-O':
#             file_name = args[2].split('/')[-1]
#         else: 
#             file_name = args[2]
        
#         # if subprocess.Popen(args, cwd=download_dir).wait() == 0:
            
        

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

while user_proceed_input == 'y':

    # Select download destination folder
    download_dir = select_dlwd_path()

    # Prompt user to enter all args for all curl commands
    commands = get_all_curl_cmd_args()

    # TODO Implement curl command (must decide between run and popen)
    # https://www.geeksforgeeks.org/curl-command-in-linux-with-examples/?ref=lbp


    # Ask if user wants to proceed again
    user_proceed_input = validate_yes_no_answer(
        'Do you want to try again? (y/n) ')


display_closing_message()
'''
END of program
'''