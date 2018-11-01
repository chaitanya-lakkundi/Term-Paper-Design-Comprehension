from lxml import html
from lxml.cssselect import CSSSelector
import requests
import simpleflock as sf
from subprocess import call
from time import sleep

def chooseRepos(filename, count):
    choices = []
    with sf.SimpleFlock("/tmp/" + filename + "_lock"):
        with open(filename) as rf:
            choices.extend([line.strip() for line in rf.readlines()[:count]])
        call("sed -i '1," + str(count) + "d' " + filename, shell=True)
    if not choices:
        raise EOFError("File Empty")
    return choices

def writeEmails(user_emails_list):
    with sf.SimpleFlock("/tmp/scrape_write_email"):
        with open("username_email_github.csv", "a") as f:
            for username,email in user_emails_list:
                f.write(username+","+email+"\n")

def getEmail(user_project, username_emails_list):
    print(user_project)

    r = requests.get('https://github.com/'+ user_project + "/commits")
    tree = html.fromstring(r.text)
    sel = CSSSelector('a.sha')
    commit_href = sel(tree)[0].get('href')

    r = requests.get("https://github.com" + commit_href + ".patch")
    all_lines = r.text.split("\n")

    if all_lines[1].find("<") != -1:
        email_line = all_lines[1]
    elif all_lines[2].find("<") != -1:
        email_line = all_lines[2]
    else:
        return
    start_pos = email_line.find("<") + 1
    email = email_line[start_pos:-1]
    username = user_project.split("/")[0]
    print(username, email)
    username_emails_list.append((user_project, email))
    if len(username_emails_list) >= 10:
        writeEmails(username_emails_list)
        username_emails_list.clear()

def patchUnfinished(username_list_filename, choices):
    with sf.SimpleFlock("/tmp/" + username_list_filename + "_lock"):
        with open(username_list_filename, "a") as wf:
            wf.write("\n".join(choices) + "\n")

def main(choices):
    username_emails_list = list()
    try:
        for line in choices:
            getEmail(line.strip(), username_emails_list)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    try:
        from sys import argv
        username_list_filename = argv[1]
        choices = []
        while True:
            choices = chooseRepos(username_list_filename, 10)
            main(choices)

    except:
        patchUnfinished(username_list_filename, choices)
        print("Handled")
