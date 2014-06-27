import requests
import json


def getMozilliansData(appKey, appName):
    all_users = {}
    entry_list = []
    # base_url should point to the server hosting Mozillian.
    base_url = 'http://192.168.56.101:8000/api/v1/'
    users_url = base_url + 'users/' + '?app_key=' + appKey + '&app_name=' + appName + '&groups=bugbounty'
    headers = {'Accept': 'application/json'}
    resp = requests.get(users_url, headers=headers)
    jresp = resp.json()
    users = jresp['objects']
    for user in users:
        entry = {}
        entry['full_name'] = user['full_name']
        entry['email'] = user['email']
        entry['photo'] = user['photo']

        entry_list.append(entry)

    all_users['users'] = entry_list
    jusers = json.dumps(all_users, indent=4)
    f = open('mozillian_users.json', 'w')
    print >> f, jusers
    f.close()


def getBugDetails(username, password):
    # http://localhost:8080/bmo/buglist.cgi?f1=attachments.filename&o3=equals&list_id=7&v3=sec-bounty%2B&o1=equals&o2=equals&query_format=advanced&f3=flagtypes.name&f2=attachments.isprivate&v1=my-sec-bounty-desc.txt&v2=1
    bug_id_list = []
    summary_list = []
    all_bugs = {}
    headers = {'Accept': 'application/json'}
    base_url = 'http://localhost:8080/bmo/rest/'

    # GET request to get login and fetch the token.
    login_url = base_url + 'login?login=' + username + '&password=' + password
    login_resp = requests.get(login_url, headers=headers)
    token = login_resp.json()['token']

    url = base_url + 'bug?f1=attachments.filename&o1=equalsv1=my-sec-bounty-desc.txt&f2=attachments.isprivate&o2=equals&v2=1&f3=flagtypes.name&o3=equals&v3=sec-bounty%2B&query_format=advanced&include_fields=id'
    token_url = url + '&token=' + token
    r = requests.get(token_url, headers=headers)
    jdata = r.json()
    bugs = jdata['bugs']
    num_bugs = len(bugs)
    for bug in bugs:
        bug_id_list.append(bug['id'])

    for bug_id in bug_id_list:
        attachment_url = base_url + 'bug/' + str(bug_id) + '/attachment'
        token_attachment_url = attachment_url + '?token=' + token
        resp = requests.get(token_attachment_url, headers=headers)
        jresp = resp.json()
        attachment_bugs = jresp["bugs"]
        attachment_list = attachment_bugs[str(bug_id)]
        for attachment in attachment_list:
            #Attachment filename should be the filename that is agreed upon for all bugs.
            if attachment['file_name'] == 'my-sec-bounty-desc.txt' and attachment['is_private'] == 1:
                bounty_desc = attachment['description']
                bounty_desc_list = bounty_desc.split(',')
                summary_dict = {}
                summary_dict['bug_id'] = bug_id
                summary_dict['reporter_email'] = bounty_desc_list[0]
                summary_dict['amount'] = bounty_desc_list[1]
                summary_dict['fixed_date'] = bounty_desc_list[2]
                summary_dict['reported_date'] = bounty_desc_list[3]
                summary_dict['awarded_date'] = bounty_desc_list[4]
                summary_dict['publish'] = bounty_desc_list[5]
                #summary_dict['credit1']         = bounty_desc_list[6]
                #summary_dict['credit2']         = bounty_desc_list[7]
                #summary_dict['credit3']         = bounty_desc_list[8]
                summary_list.append(summary_dict)

    all_bugs['bugs'] = summary_list
    jsummary = json.dumps(all_bugs, indent=4)
    f = open('bounty_bugs.json', 'w')
    print >> f, jsummary
    f.close()


def filter():
    filtered_data = {}
    final_list = []
    mozillian_data = json.loads(open('mozillian_users.json').read())
    print mozillian_data
    mozillians = mozillian_data['users']
    print len(mozillians)
    bugzilla_data = json.loads(open('bounty_bugs.json').read())
    print bugzilla_data
    bugs = bugzilla_data['bugs']
    print len(bugs)
    for bug in bugs:
        bug_email = bug['reporter_email']
        for mozillian in mozillians:
            mozillian_email = mozillian['email']
            if bug_email == mozillian_email:
                entry = {}
                entry['reported_date'] = bug['reported_date']
                entry['publish'] = bug['publish']
                entry['awarded_date'] = bug['awarded_date']
                entry['bug_id'] = bug['bug_id']
                entry['amount'] = bug['amount']
                entry['fixed_date'] = bug['fixed_date']
                entry['reporter_email'] = bug['reporter_email']
                entry['reporter_photo'] = mozillian['photo']
                entry['reporter_full_name'] = mozillian['full_name']
                final_list.append(entry)
    filtered_data['bugs'] = final_list
    j_filtered_data = json.dumps(filtered_data)
    f = open('bounty_data.json', 'w')
    print >> f , j_filtered_data
    f.close()





