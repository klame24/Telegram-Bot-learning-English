import sqlite3 as sq


def str_to_array(s):
    s = str(s)
    s = s[1:]
    s = s[:-1]
    array = []
    s = s.replace(', '," ")
    s = s.replace('"','')
    string = ""
    for i in range(len(s)):
        if s[i] != " ":
            string += s[i]
        else:
            array.append(string)
            string = ""
    array.append(string)
    return array


def addWordsForKnowLedgesInDB(user_id_num, array):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET FIRST_word=? WHERE user_id LIKE ?", (array[0], user_id_num, ))
    cur.execute("UPDATE users SET SECOND_word=? WHERE user_id LIKE ?", (array[1], user_id_num,))
    cur.execute("UPDATE users SET THIRD_word=? WHERE user_id LIKE ?", (array[2], user_id_num,))
    cur.execute("UPDATE users SET FOURTH_word=? WHERE user_id LIKE ?", (array[3], user_id_num,))
    cur.execute("UPDATE users SET FIFTH_word=? WHERE user_id LIKE ?", (array[4], user_id_num,))
    con.commit()
    con.close()


def outputFirstWord(user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT FIRST_word FROM users WHERE user_id LIKE ?", (user_id_num, ))
    result = cur.fetchall()
    return result[0][0]


def outputSecondWord(user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT SECOND_word FROM users WHERE user_id LIKE ?", (user_id_num, ))
    result = cur.fetchall()
    return result[0][0]


def outputThirdWord(user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT THIRD_word FROM users WHERE user_id LIKE ?", (user_id_num, ))
    result = cur.fetchall()
    return result[0][0]


def outputFourthWord(user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT FOURTH_word FROM users WHERE user_id LIKE ?", (user_id_num, ))
    result = cur.fetchall()
    return result[0][0]


def outputFifthWord(user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT FIFTH_word FROM users WHERE user_id LIKE ?", (user_id_num, ))
    result = cur.fetchall()
    return result[0][0]


def outputRusWord(wordEng, user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT ENG_words FROM users WHERE user_id LIKE ?", (user_id_num, ))
    result_eng = cur.fetchall()
    result_eng = result_eng[0][0]
    result_eng = str_to_array(result_eng)
    cur.execute("SELECT RUS_words FROM users WHERE user_id LIKE ?", (user_id_num,))
    result_rus = cur.fetchall()
    result_rus = result_rus[0][0]
    result_rus = str_to_array(result_rus)
    for i in range(len(result_eng)):
        if result_eng[i] == wordEng:
            return result_rus[i]


def cleanWordsForTest(user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET FIRST_word=?", ("",))
    cur.execute("UPDATE users SET SECOND_word=?", ("",))
    cur.execute("UPDATE users SET THIRD_word=?", ("",))
    cur.execute("UPDATE users SET FOURTH_word=?", ("",))
    cur.execute("UPDATE users SET FIFTH_word=?", ("",))
    con.commit()
    con.close()



