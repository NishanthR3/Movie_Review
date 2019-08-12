from os import system

if __name__ == '__main__':
    system("echo installing packages as sudo")
    try:
        system("sudo apt-get install python3-pip")
    except:
        system("echo failed to install pip3")
        exit(1)
    try:
        system("sudo pip3 install kafka")
    except:
        system("echo failed to install kafka")
        exit(1)
    try:
        system("sudo pip3 install tweepy")
    except:
        system("echo failed to install pip3")
        exit(1)
    try:
        system("sudo pip3 install cassandra-driver")
    except:
        system("echo failed to install pip3")
        exit(1)
    system("echo installed all packages succesfully")
