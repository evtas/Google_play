import psycopg2
import pymongo

if __name__ == '__main__':
    conn = psycopg2.connect(database='google_play', user='postgres', password='binshao123', host='127.0.0.1', port='5432')
    cur = conn.cursor()

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
        count += 1
        print("res: ", total - count)
        
        assert len(attr) == len(game)
        item = {}
        for i in range(len(attr)):
            item[attr[i]] = game[i]
        
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['google_play_games']
        post = db['games_collections']

        post.insert_one(item)