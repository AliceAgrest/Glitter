import socket
import glitter as g

SERVER_IP = '54.187.16.171'
SERVER_PORT = 1336
URL = 'http://cyber.glitter.org.il'

CHALLENGE_LIST = 'CHALLENGE LIST\n[1] Login to other user\n[2] Get password\n[3] Get privet messages of required user\n[4] Get cookie of required user\n[5] Do special post(xss)\n'
ERRORS_LIST = 'ERROR LIST:\n[1] Like more then one time\n[2] Comment with not your name\n[3] Do wow\n[4] Edit post\n[5] Load posts from any profile\n[6] Search by id\n[7] See for which users viseted requared user\n[8] Load messages from server from requared user\n[9] Refuse glanceship\n[10] Get username by editing the post\n[11] Approve glance request\n[12] Unwow\n[13] Unlike\n'

def login_func(sock):
    '''
    The func is logging to the server
    :param sock: socket that we opened
    :type sock: socked
    '''
    username = ''
    password = ''
    user_id = ' '
    while user_id == ' ':
        username = input('Enter username: ')
        password = input('Enter password: ')
        user_id ,a = g.login(sock, username, password)
    return username, user_id
   
def errors_to_do(sock, curr_username, curr_id):
    '''
    The func shows the errors the server has
    :param sock: socket that we opened
    :param curr_username: user that we loggin with 
    :param curr_id: number of user we loggin with
    :type sock: socket
    :type curr_username: string
    :type curr_id: stirng
    '''
    try:
        op = int(input(ERRORS_LIST))
    except Exception:
        return
    if op == 1:
        other_username = input('Enter username who you want to do like: ')
        other_id = g.search_id(sock,other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return
        chosed_post = g.choose_post(sock, other_username)
        g.do_like(sock, chosed_post, curr_id, curr_username)
        g.do_like(sock, chosed_post, curr_id, curr_username)
    elif op == 2:
        other_username = input('Enter username who you want to write a comment: ')
        other_id = g.search_id(sock,other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return
        chosed_post = g.choose_post(sock, other_username)
        comment = input('Enter a comment: ')
        comment_name = input('Enter name that going to be above the comment: ')
        g.do_comment(sock,chosed_post , curr_id, comment_name, comment)
    elif op == 3:
        other_username = input('Enter username to publish wow: ')
        other_id = g.search_id(sock,other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return
        chosed_post = g.choose_post(sock, other_username)
        g.wow(sock, curr_username, curr_id, chosed_post)
    elif op == 4:
        chosed_post = g.choose_post(sock, curr_username)
        if chosed_post == '_':
            print('Too much posts\nChose other user')
            return
        comment = input('Enter a comment to change: ')
        color = input('Enter background color: ')
        ava = input('Enter avatar(you have ): ')
        words_color = input('Enter color for words in the glit: ')
        g.edit_post(sock, curr_id, curr_id, curr_username, ava, color, comment, chosed_post,words_color)
    elif op == 5:
        other_username = input('Enter username to search: ')
        other_id = g.search_id(sock,other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return
        post_count = input('Enter count of posts you want to see: ')
        if int(post_count) < 1:
            post_count = '1'
        posts = g.load_user_profile_info(sock, other_username, post_count)
        g.print_posts(posts)
    elif op == 6:
        other_id = input('Enter id to search: ')
        g.search_by_id(sock, other_id)
    elif op == 7:
        other_username = input('Enter username for checking entities whose feed was visited: ')
        other_id = g.search_id(sock, other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return
        g.users_visited_profiles(sock, other_id)
    elif op == 8:
        other_username = input('Enter username to see thier messages from the server: ')
        other_id = g.search_id(sock, other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return
        g.load_users_details(sock, other_id)
    elif op == 9:
        user1 = input('Enter user name that require the glanceship: ')
        user2 = input('Enter user name that responder the glanceship: ')
        user_id1 = g.search_id(sock, user1)
        user_id2 = g.search_id(sock, user2)
        if user_id1 == 'wrong username' or user_id2 == 'wrong username': #checking if the user exist
            print('One of the user are not exist')
            return
        g.refuse_glanceship(sock, user_id1, user_id2)
    elif op == 10:
        other_id = input('Enter any id(number that less then 10000) you want: ')
        g.update_profile(sock, curr_username, other_id)
    elif op == 11:
        other_username = input('Enter username that you be friend: ')
        other_id = g.search_id(sock, other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return
        g.approving_glance_rq(sock, curr_id, other_id)
    elif op == 12:
        other_username = input('Enter username that you want to unwow him: ')
        other_id = g.search_id(sock, other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return
        g.unwow(sock, other_username)
    elif op == 13:
        other_username = input('Enter username that you want to unlike him: ')
        other_id = g.search_id(sock, other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return
        g.unlike(sock, other_username)
    else:
        exit(0)

def challenges_to_do(sock, curr_username,curr_id):
    '''
    The func is shows the challenges that server has
    :param sock: socket that we opened
    :param curr_username: user that we loggin with 
    :param curr_id: number of user we loggin with
    :type sock: socket
    :type curr_username: string
    :type curr_id: stirng
    '''
    try:
        op = int(input(CHALLENGE_LIST))
    except Exception:
        return
    if op == 1:
        username = input('Enter username that you want login to: ')
        the_id, password = g.login_to_other_user(sock, curr_username, username)
        print('Login succsed, '+ username)
        print("Now you'r in " + username + ' profile')
        return username, the_id
    elif op == 2:
        other_username = input('Enter username that you want to find their password: ')
        other_id = g.search_id(sock, other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return ' ',' '
        encrypt_id = g.encrypt_user_id(other_id)
        reset_msg = g.reset_password_msg(encrypt_id)
        g.find_password_web(other_username, reset_msg)
        return ' ',' '
    elif op == 3:
        other_username = input('Enter username to find his private things: ')
        other_id = g.search_id(sock, other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return ' ',' '
        g.users_visited_profiles(sock, other_id)
        g.load_users_details(sock, other_id)
        posts = g.load_user_profile_info(sock, other_username)
        g.print_posts(posts)
        return ' ',' '
    elif op == 4:
        other_username = input('Enter username you want to find his cookie: ')
        print(other_username + ' cookie is => ' + g.find_cookie(other_username))
        return ' ',' '
    elif op == 5:
        other_username = input('Enter username to post special post: ')
        other_id = g.search_id(sock, other_username)
        if other_id == 'wrong username': #checking if the user exist
            print('Wrong username')
            return ' ',' '
        g.do_xss(sock, other_username, other_id, curr_id)
        return ' ',' '
    else:
        exit(0)

def new_session():
    '''
    The func opens socket between the server and client
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server_address = (SERVER_IP, SERVER_PORT)
        try:
            sock.connect(server_address)
        except Exception:
            exit()
        username,user_id = login_func(sock)
        print('Login succsed, '+ username)
        while True:
            try:
                try:
                    op = int(input('What you want to see\n[1] Errors\n[2] Challenges\n'))
                except Exception:
                    continue
                if op == 1:
                    errors_to_do(sock, username, user_id)
                elif op == 2:
                    username1, id1 = challenges_to_do(sock, username, user_id)
                    if username1 != ' ' and id1 != ' ':
                        username = username1
                        user_id = id1
            except KeyboardInterrupt:
                exit()

def main():
    new_session()

if __name__ == "__main__":
    main()