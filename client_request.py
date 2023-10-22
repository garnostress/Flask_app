import requests

base_url = 'http://127.0.0.1:5000'

# response_get = requests.get('http://127.0.0.1:5000/users/14')
# print(response_get.status_code)
# print(response_get.json())
# #
# #
# response_post = requests.post(
#      'http://127.0.0.1:5000/users/',
#      json={
#          'name': 'Ivan',
#          'user_pass': '12345kiojoi'
#      }
#  )
# print(response_post.status_code)
# print(response_post.json())
# # #
# # #
# response_patch = requests.patch(
#     'http://127.0.0.1:5000/users/1',
#     json={
#         'name': 'Stepan',
#         'user_pass': '123456789'
#     }
# )
# print(response_patch.status_code)
# print(response_patch.json())
# #
# #
# response_delete = requests.delete('http://127.0.0.1:5000/users/13')
# print(response_delete.status_code)
# print(response_delete.json())
# #
#
# response_get = requests.get('http://127.0.0.1:5000/users/1')
# print(response_get.status_code)
# print(response_get.json())

#
# response_get = requests.get(f'{base_url}/adv/9')
# print(response_get.status_code)
# print(response_get.json())
# #
# #
# response_post = requests.post(
#     f'{base_url}/adv/',
#     json={
#         'header': 'New adv',
#         'desc': 'это тестовое описание объявления1',
#         'owner_id': 1
#     }
# )
# print(response_post.status_code)
# print(response_post.json())

#
# response_patch = requests.patch(
#     f'{base_url}/adv/9',
#     json={
#         'header': 'Измененный заголовок',
#         'desc': 'это тестовое описание объявления',
#         'owner_id': 1
#     }
# )
# print(response_patch.status_code)
# print(response_patch.json())
# #
#
# response_delete = requests.delete(f'{base_url}/adv/9')
# print(response_delete.status_code)
# print(response_delete.json())
# #
# #
# response_get = requests.get(f'{base_url}/adv/9')
# print(response_get.status_code)
# print(response_get.json())
#
