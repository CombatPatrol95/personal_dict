# import sqlite3
#
#
# def search_all_matching(word):
#     with sqlite3.connect("notebook.sqlite3") as conn:
#         cur = conn.cursor()
#         return [i[0] for i in cur.execute("SELECT word FROM words WHERE word LIKE ? || '%' ",
#                                           (word,)).fetchall()]
#
#
# def search_word(word):
#     with sqlite3.connect("notebook.sqlite3") as conn:
#         cur = conn.cursor()
#         try:
#             return \
#                 cur.execute("SELECT description FROM words WHERE word = ?",
#                             (word,)).fetchall()[0][0]
#         except IndexError:
#             return []
#
#
# def get_all_words():
#     with sqlite3.connect("notebook.sqlite3") as conn:
#         cur = conn.cursor()
#         return [i[0] for i in cur.execute("SELECT word FROM words").fetchall()]
#
#
# def insert_new_word(*data):
#     with sqlite3.connect("notebook.sqlite3") as conn:
#         cur = conn.cursor()
#         cur.executemany("INSERT INTO words VALUES(?, ?, ?, ?, ?, ?)", *data)
#         conn.commit()
#
#
# def db_init():
#     with sqlite3.connect("notebook.sqlite3") as conn:
#         cur = conn.cursor()
#         cur.execute("CREATE TABLE words(word, parts_of_speech, meaning, meaning_similar, form_similar,"
#                     "pronoun_similar)")
#         conn.commit()
import sqlite3

def insert_new_word(data):
    with sqlite3.connect("notebook.sqlite3") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO words VALUES (?, ?, ?, ?, ?, ?)", data)
        conn.commit()


# def insert_new_word(word, parts_of_speech, meaning, meaning_similar, form_similar, pronoun_similar):
#     with sqlite3.connect("notebook.sqlite3") as conn:
#         cur = conn.cursor()
#         cur.execute("INSERT INTO words VALUES (?, ?, ?, ?, ?, ?)",
#                     (word, parts_of_speech, meaning, meaning_similar, form_similar, pronoun_similar))
#         conn.commit()

def search_word(word):
    with sqlite3.connect("notebook.sqlite3") as conn:
        cur = conn.cursor()
        cur.execute("SELECT description FROM words WHERE word = ?", (word,))
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return "Word not found"

def search_all_matching(word):
    with sqlite3.connect("notebook.sqlite3") as conn:
        cur = conn.cursor()
        cur.execute("SELECT word FROM words WHERE word LIKE ? || '%'", (word,))
        return [row[0] for row in cur.fetchall()]

def get_all_words():
    with sqlite3.connect("notebook.sqlite3") as conn:
        cur = conn.cursor()
        cur.execute("SELECT word FROM words")
        return [row[0] for row in cur.fetchall()]

def db_init():
    with sqlite3.connect("notebook.sqlite3") as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS words (word TEXT, parts_of_speech TEXT, meaning TEXT, "
                    "meaning_similar TEXT, form_similar TEXT, pronoun_similar TEXT)")
        conn.commit()

