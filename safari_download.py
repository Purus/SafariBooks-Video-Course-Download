from bs4 import BeautifulSoup
import requests
import shutil
import os
import string
from subprocess import check_output

url = 'https://www.safaribooksonline.com/library/view/learning-docker/9781491956885/'
domain = 'https://www.safaribooksonline.com'
output_folder = './output'
username = '<<your-email>>@gmail.com'
password = '<<password>>'
download_count = 5

req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')

lessons = soup.find_all('li', class_='toc-level-1')
print("Total Chapters : {}".format(len(lessons)))

shutil.rmtree(output_folder, ignore_errors=True)
os.makedirs(output_folder)
module_name = 'Module 0'

try:
    os.remove("myOutFile.txt")
except Exception:
    pass

outF = open("myOutFile.txt", "a")

i=1

for lesson in lessons:
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    lesson_name = ''.join(c for c in lesson.a.text if c in valid_chars)
    lesson_name = lesson_name.replace("?","").encode('utf8', 'replace')

    if lesson_name.startswith('Module') and not 'Summary' in lesson_name:
        module_name = lesson_name.encode('utf8', 'replace')
        os.makedirs(output_folder + '/' + module_name)
        for index, video in enumerate(lesson.ol.find_all('a')):
            video_name = str(index+1) + ' - ' + video.text
            video_name = video_name.replace("?","").replace(":","").encode('utf8', 'replace')            
            video_url = domain + video.get('href')
            video_out = output_folder + '/' + module_name + '/' + video_name + '.mp4'
            cmd = "youtube-dl -u {} -p {} {} -g".format(username, password, video_url)
            output = check_output(cmd,shell=True)
            #print("URL is {}".format(output))
            textout= "{}   dir={} \n   out={}\n".format(output,output_folder + '/' + module_name + '/' + lesson_name + '/',video_name + '.mp4').encode('utf8', 'ignore')
            outF.write(textout)	
            print(lesson_name + '/' + video_name + '.mp4')			
    else:
        lesson_name = "{}. {}".format(i,lesson_name)
        os.makedirs(output_folder + '/' + module_name + '/' + lesson_name)
        for index, video in enumerate(lesson.ol.find_all('a')):
            video_name = str(index+1) + ' - ' + video.text
            video_name = video_name.replace("?","").replace(":","").encode('utf8', 'replace')            
            video_url = domain + video.get('href')
            video_out = output_folder + '/' + module_name + '/' + lesson_name + '/' + video_name + '.mp4'
            cmd = "youtube-dl -u {} -p {} {} -g".format(username, password, video_url)
            output = check_output(cmd,shell=True)
            #print("URL is {}".format(output))
            textout= "{}   dir={} \n   out={}\n".format(output,output_folder + '/' + module_name + '/' + lesson_name + '/',video_name + '.mp4')
            print(lesson_name + '/' + video_name + '.mp4')			
            outF.write(textout)	
        i += 1

outF.close()
download_cmd = "aria2c -j{} -i .\myOutFile.txt".format(download_count)
#check_output(download_cmd,shell=True)
os.system(download_cmd)