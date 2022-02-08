import subprocess

# TODO Maybe be able to choose the destination folder (like Downloads for example) 

sut_url = 'https://static.wikia.nocookie.net/iz-one/images/4/4c/One-reeler_Digital.jpg'
sut_filename = 'izone-pic.jpg'

default_dir = 'output'
curl_flag = '-o'

args = ['curl', curl_flag, sut_filename, sut_url]

# Create the output directory if it does not exist already
# This may change
subprocess.run(['mkdir', default_dir])


# Execute the curl command
subprocess.Popen(args, cwd=default_dir).wait()

print("Done")