from Databases.Users.Workers.Login.tasks import login_user

# result = remove_user.delay('test', 'test')
# result = register_user.delay("test", 'test', ['test@test.com', 'test1@test.com'])
# result = login_user.delay('test', 'test')
# result = logout_user.delay('test', 'test')
# result = user_is_alive.delay('test', 'test')
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

login_user('test', 'test')
