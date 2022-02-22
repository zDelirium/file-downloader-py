import subprocess
import os

def display_welcome_message():
    """
    Clear console and display welcoming message
    """
    # Welcome message
    subprocess.run('clear')
    welcome_message = '\nHello {}!\n\nThis program will let you downloads multiple files at once in your local machine using the curl command.\n'.format(
        os.environ['USER'])
    
    welcome_message = '{}Tip: For all yes/no answers, you can simply leave it blank to answer yes :)\n'.format(welcome_message)
    print(welcome_message)

def validate_yes_no_answer(init_question, yes_no_answers=['y', 'n']):
    """
    Validate that the user can properly answers yes/no questions. User can also answer yes by not entering anything

    Args:
        init_question (str): the question of interest
        yes_no_answers (list, optional): answer list. Defaults to ['y', 'n'].

    Returns:
        bool: user's answer
    """
    # Get user answer
    user_input = input(init_question).strip().casefold()
    if not user_input:
        user_input = yes_no_answers[0]
    while user_input not in yes_no_answers:
        user_input = input('Please enter \'y\' (yes) or \'n\' (no): ').strip().casefold()
        if not user_input:
            user_input = yes_no_answers[0]
    
    # Transforming to boolean        
    return user_input == yes_no_answers[0]
    
def select_dlwd_path():
    """
    Prompts user to choose the download path of the files

    Returns:
        str: absolute path representing the intended download directory
    """
    home_env_var = 'HOME'
    
    # Get Downloads folder directory
    download_dir = '{}/Downloads'.format(os.environ[home_env_var])

    # Ask user if they want to continue with the Downloads directory
    print('\nBy default, the files will be downloaded in {} folder'.format(download_dir))
    user_dir_input = validate_yes_no_answer(
        'Do you want to continue with this directory? (y/n) ')

    # Ask user for alternate directory if not
    if not user_dir_input:
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

def get_all_curl_cmd_args():
    """
    Get arguments for all curl commands. 
    
    Returns:
        list: all curl commands to be executed (2D list) 
    """
    commands = []

    print('It is now time to add the files to download. If you do not want to name the file, leave its name blank. Else make sure you put the right extension at the end.')
    print('Note that for now the app does not ensure that there are no duplicate file names, so files with the same name may get overwritten.\n')

    user_stops = False
    while not user_stops:
        # Prompt user to enter file links and info
        enter_files_info(commands)

        print('The program will download the following {} file(s):\n'.format(len(commands)))

        # Display name of files to be downloaded
        display_file_names(commands)
        
        user_stops = validate_yes_no_answer('\nConfirm that these are all the files to download. If not, you can continue adding. (y/n) ')
        print()
        
    # Return all commands and nb of files
    return commands

def enter_files_info(commands):
    """
    Prompt user to enter file names and links

    Args:
        commands (list): all curl commands to be executed
    """
    user_continue_input = True
    while user_continue_input:
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

def display_file_names(commands):
    """
    Display the name of all files to be downloaded to the user in 2 columns

    Args:
        commands (list): all curl commands to be executed (or have already been)
    """
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

def execute_curl(commands, download_dir):
    """
    Execute all curl commands and verify their status

    Args:
        commands (list): 2D list of all curl commands
        download_dir (str): absolute path of the intended download directory
    """
    # Create destination folder if it does not exist
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)
        print('\nCreated new {} directory'.format(download_dir))
    
    print('\nStarting to download all files to {}\n'.format(download_dir))
    
    # Attempt file downloads
    failed_commands = []
    counter = 0
    for cmd in commands:
        counter += 1
        current_file_name = cmd[2].split('/')[-1]
        print('Attempting to download {} in {}\t({}/{})'.format(current_file_name, download_dir, counter, len(commands)))
        if subprocess.Popen(cmd, cwd=download_dir).wait() == 0:
            print('Succesfully downloaded {} in {}\t({}/{})\n'.format(current_file_name, download_dir, counter, len(commands)))
        else:
            failed_commands.append(cmd)
            print('Failed to download {} in {}\t({}/{})\n'.format(current_file_name, download_dir, counter, len(commands)))
            
    # Display if all downloads were successful
    if not failed_commands:
        print('Successfully downloaded all files!\n') 
    # If not, display how many files were successfully downloaded and show which ones were not   
    else:
        print('Successfully downloaded {}/{} files. The following files are missing:\n'.format(len(commands)-len(failed_commands), len(commands)))
        display_file_names(failed_commands)
        

def display_closing_message():
    """
    Display closing message
    """
    print("\n\nSee you next time!\n\n")


'''
START of program
'''
display_welcome_message()

# Ask user if they want to proceed or not
user_proceed_input = validate_yes_no_answer('Are you ready to proceed? (y/n) ')

while user_proceed_input:

    # Select download destination folder
    download_dir = select_dlwd_path()

    # Prompt user to enter all args for all curl commands
    commands = get_all_curl_cmd_args()

    # Implement curl command (must decide between run and popen)
    # https://www.geeksforgeeks.org/curl-command-in-linux-with-examples/?ref=lbp
    if validate_yes_no_answer('Do you want to download now? If not, you can start from anew. (y/n) '):
        execute_curl(commands, download_dir)

    # Ask if user wants to proceed again
    user_proceed_input = validate_yes_no_answer(
        '\nDo you want to try again from another directory? (y/n) ')


display_closing_message()
'''
END of program
'''