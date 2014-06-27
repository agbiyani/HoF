import dataGen
import getpass

username = raw_input('Enter your bugzilla username: ')
password = getpass.getpass("Enter your bugzilla password: ")
# appKey = raw_input("Enter your app-key to access Mozillian API: ")
# appName = raw_input("Enter your app-name to access Mozillian API: ")

appKey = '4d53a41ee1beaf13ddd6b1be5d012c36a02e2e99'
appName = 'hof'


#if __name__ == 'main':
dataGen.getMozilliansData(appKey=appKey, appName=appName)
dataGen.getBugDetails(username=username, password=password)
dataGen.filter()