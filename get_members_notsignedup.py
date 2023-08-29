import pandas as pd

excel_form_title = input('enter name of excel member form to cross check against:') + '.xlsx'
signup_members = pd.read_excel(excel_form_title) # the signup form excel
signup_members = signup_members[['Telegram handle', 'Full Name (as in matriculation card)']]
signup_members = signup_members.replace(r'@','',regex=True)

group_member_title = input('enter name of the telegram members csv file to cross check against:') + '.csv'
group_members = pd.read_csv(group_member_title) # the csv containing memberlist in the announcement group (can change this actually if you want to calculate for other groups)
group_members = group_members[['username', 'name']]

members_ingroup_butnot_signup = ~ group_members['username'].isin(signup_members['Telegram handle'])
members_signup_butnot_ingroup = ~ signup_members['Telegram handle'].isin(group_members['username'])

members_ingroup_butnot_signup = group_members[members_ingroup_butnot_signup]
members_signup_butnot_ingroup = signup_members[members_signup_butnot_ingroup]

print(members_signup_butnot_ingroup)
members_ingroup_butnot_signup.to_csv('members_ingroup_butnot_signedup.csv', index=False) # the created file name can be changed
members_signup_butnot_ingroup.to_csv('members_signedup_butnot_ingroup.csv',index=False) # the created file name can be changed

print('created two csvs of non present members')