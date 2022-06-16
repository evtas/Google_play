import psycopg2

if __name__ == '__main__':
    conn = psycopg2.connect(database='google_play', user='postgres', password='binshao123', host='127.0.0.1', port='5432')
    cur = conn.cursor()

    conn_2 = psycopg2.connect(database='google_play_games', user='postgres', password='binshao123', host='127.0.0.1', port='5432')
    cur_2 = conn_2.cursor()

    sql = "select * from google_play_games"
    cur.execute(sql)
    games = cur.fetchall() 
    conn.close()

    attr = ['id', 'name', 'author', 'star_rating', 'download_times', 
            'content_rating', 'introduction', 'update_time', 'genre', 
            'url', 'apk']

    total = len(games)
    count = 0
    for game in games:
        flag = True
        count += 1
        print("res: ", total - count)
        for val in game:
            if not val:
                flag = False
                break
        if flag:
            cur_2.execute("insert into games_games (name, author, star_rating, download_times, content_rating, introduction, update_time, url, genre, image, apk) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (game[1], game[2], game[3], game[4], game[5], game[6], game[7], game[9], game[8], '1', "1"))        
            conn_2.commit()

            
