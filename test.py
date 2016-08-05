from Server.Users.Workers.Login.tasks import login_user, logout_user
from Server.Users.Workers.Registration.tasks import remove_user, register_user
from Server.Users.Workers.UserActivityReporter.tasks import report_user_activity

result = remove_user.delay('test', 'test')
result = register_user.delay("test", 'test', ['test@test.com', 'test1@test.com'])
result = login_user.delay('test', 'test')
result = logout_user.delay('test', 'test')
result = report_user_activity.delay('test', 'test')
# print(result.get(timeout=10))
#
# time1 = datetime.now()
# time2 = datetime.now()
#
# # time3 = datetime.now()
# # time4 = datetime.now()
# #
# # timedelta1 = time2 - time1
# # timedelta2 = time4 - time3
# #
# # print('timedelta1:', timedelta1)
# # print('timedelta2:', timedelta2)

login_user.delay('test', 'test')
