import random
from aiogram import Bot, Router, types, F
from aiogram.filters import CommandStart, or_f, Command
import sqlite3 as sq
import json
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests
from bs4 import BeautifulSoup
from checkKnowledgesFuncs import (addWordsForKnowLedgesInDB, outputSecondWord, outputFifthWord, outputThirdWord,
                                  outputFourthWord, outputFirstWord, outputRusWord, cleanWordsForTest)
from keyboards import  start_kbrd, my_dictionary_kbrd, yes_or_not_kbrd, numbers_kbrd, numbers_kbrd_withoutTranslate
from translate import Translator
user_private = Router()

class AddWords(StatesGroup):
    eng_word = State()
    rus_word = State()

class DeleteWord(StatesGroup):
    eng_word = State()

class CheckKnowledge(StatesGroup):
    word1 = State()
    word2 = State()
    word3 = State()
    word4 = State()
    word5 = State()
    outputresults = State()

def parser_wordOfDay(URL, tag, class_):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    word = soup.find(tag, class_ = class_).text.strip()
    return word

def parserDescription(tag, class_, word):
    page = requests.get("https://dictionary.cambridge.org/ru/%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D1%8C/%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9/" + word)
    soup = BeautifulSoup(page.content, "html.parser")
    word = soup.find(tag, class_=class_).text.strip()
    return word


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

def add_user_to_database(user_id):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT user_id FROM users")
    result = cur.fetchall()
    count = 0
    for i in range(len(result)):
        if user_id != result[i][0]:
            count +=1
    if len(result) == count:
        cur.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        con.commit()
        con.close()
    else:
        pass

def add_engword_to_database(word, user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT ENG_words FROM users WHERE user_id LIKE ?", (user_id_num,))
    result = cur.fetchall()
    result = result[0][0]
    result = str_to_array(result)
    if "on" in result:
        result.remove("on")
    result.append(word)
    json_result = json.dumps(result)
    # print(json_result, result)
    cur.execute("UPDATE users SET ENG_words=? WHERE user_id LIKE ?", (json_result,user_id_num,))
    con.commit()
    con.close()

def add_rusword_to_database(word, user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT RUS_words FROM users WHERE user_id LIKE ?", (user_id_num,))
    result = cur.fetchall()
    result = result[0][0]
    result = str_to_array(result)
    if "on" in result:
        result.remove("on")
    result.append(word)
    json_result = json.dumps(result, ensure_ascii=False)
    # print(json_result, result)
    cur.execute("UPDATE users SET RUS_words=? WHERE user_id LIKE ?", (json_result, user_id_num,))
    con.commit()
    con.close()

def output_engwords(user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT ENG_words FROM users WHERE user_id LIKE ?", (user_id_num,))
    result = cur.fetchall()
    result = result[0][0]
    result = str_to_array(result)
    con.commit()
    con.close()
    return result

def output_ruswords(user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT RUS_words FROM users WHERE user_id LIKE ?", (user_id_num,))
    result = cur.fetchall()
    result = result[0][0]
    result = str_to_array(result)
    con.commit()
    con.close()
    return result

def delete_word(word, user_id_num):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT ENG_words FROM users WHERE user_id LIKE ?", (user_id_num,))
    result_eng = cur.fetchall()
    result_eng = result_eng[0][0]
    result_eng = str_to_array(result_eng)
    number = 0
    for i in range(len(result_eng)):
        if word == result_eng[i]:
            number = i
            result_eng.remove(word)
            break
    json_result_eng = json.dumps(result_eng)
    cur.execute("UPDATE users SET ENG_words=? WHERE user_id LIKE ?",(json_result_eng, user_id_num,))
    cur.execute("SELECT RUS_words FROM users WHERE user_id LIKE ?", (user_id_num,))
    result_rus = cur.fetchall()
    result_rus = result_rus[0][0]
    result_rus = str_to_array(result_rus)
    result_rus.remove(result_rus[number])
    json_result_rus = json.dumps(result_rus, ensure_ascii=False)
    cur.execute("UPDATE users SET RUS_words=? WHERE user_id LIKE ?",(json_result_rus, user_id_num,))
    con.commit()
    con.close()

def random_engWords(user_num_id):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT ENG_words FROM users WHERE user_id LIKE ?", (user_num_id,))
    result = cur.fetchall()
    result = result[0][0]
    result = str_to_array(result)
    con.commit()
    con.close()
    start = 0
    end = len(result)-1
    unique_numbers = set()
    while len(unique_numbers) < 5:
        unique_numbers.add(random.randint(start, end))
    random_numbers = list(unique_numbers)
    array = []
    for i in range(len(result)):
        if i in random_numbers:
            array.append(result[i])
    return array

def output_rusword(user_num_id, word):
    con = sq.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT RUS_words FROM users WHERE user_id LIKE ?", (user_num_id,))
    result_rus = cur.fetchall()
    result_rus = result_rus[0][0]
    result_rus = str_to_array(result_rus)
    cur.execute("SELECT ENG_words FROM users WHERE user_id LIKE ?", (user_num_id,))
    result_eng = cur.fetchall()
    result_eng = result_eng[0][0]
    result_eng = str_to_array(result_eng)
    for i in range(len(result_eng)):
        if result_eng[i] == word:
            return result_rus[i]
    con.commit()
    con.close()


@user_private.message(CommandStart())
async def start_cmd(message: types.Message):
    username = message.from_user.first_name
    await message.answer("Приветствую, " + username + "! 😉" + "\n" + "Вы используете бота для изучения английского языка, занимайтесь регулярно и у вас обязательно все получится! 📔", reply_markup=start_kbrd)
    add_user_to_database(message.from_user.id)

@user_private.message(or_f(Command('my_dictionary'), F.text == "Мой словарь 📖"))
async def my_dictionary_cmd(message: types.Message):
    await message.answer("Вы попали в меню раздела 'Мой словарь'", reply_markup=my_dictionary_kbrd)

@user_private.message(or_f(Command('add_word'), F.text=="Добавить слово"))
async def add_word_cmd(message: types.message, state: FSMContext):
    await state.set_state(AddWords.eng_word)
    await message.answer("Введите слово на английском")

@user_private.message(AddWords.eng_word)
async def add_engword_cmd(message: types.Message, state: FSMContext):
    add_engword_to_database(message.text, message.from_user.id)
    await state.set_state(AddWords.rus_word)
    await message.answer("Добавлено! Введите перевод на русский 😄")

@user_private.message(AddWords.rus_word)
async def add_rusword_cmd(message: types.Message, state: FSMContext):
    add_rusword_to_database(message.text, message.from_user.id)
    data = await state.get_data()
    await message.answer("Успешно добавлено, зайдите в словарь, чтобы увидеть результат! 😉", reply_markup=my_dictionary_kbrd)
    await state.clear()

@user_private.message(F.text=="Список слов")
async def list_words_cmd(message: types.Message):
    await message.answer("Вы хотите увидеть слова с переводом?", reply_markup=yes_or_not_kbrd)

@user_private.message(F.text=="Да, хочу")
async def yes_i_want_cmd(message: types.message):
    array_eng = output_engwords(message.from_user.id)
    array_rus = output_ruswords(message.from_user.id)
    await message.answer("Вот список слов, добавленных в ваш словарь, удачного изучения 🙂", reply_markup = numbers_kbrd)
    s = ""
    if len(array_eng) <= 10:
        for i in range(len(array_eng)):
            s += str(i+1) + ". " + array_eng[i] + " -- " + array_rus[i] + "\n"
        await message.answer(s)
    else:
        for i in range(0, 10):
            s += str(i+1) + ". " + array_eng[i] + " -- " + array_rus[i] + "\n"
        await message.answer(s)

@user_private.message(F.text=="1 страница")
async def first_page_cmd(message: types.Message):
    array_eng = output_engwords(message.from_user.id)
    array_rus = output_ruswords(message.from_user.id)
    s = ""
    if len(array_eng) <= 10:
        for i in range(len(array_eng)):
            s += str(i+1) + ". " + array_eng[i] + " -- " + array_rus[i] + "\n"
        await message.answer(s, reply_markup = numbers_kbrd)
    else:
        for i in range(0, 10):
            s += str(i+1) + ". " + array_eng[i] + " -- " + array_rus[i] + "\n"
        await message.answer(s, reply_markup = numbers_kbrd)

@user_private.message(F.text=="2 страница")
async def second_page_cmd(message: types.Message):
    array_eng = output_engwords(message.from_user.id)
    array_rus = output_ruswords(message.from_user.id)
    s = ""
    if len(array_eng) <= 20:
        for i in range(10, len(array_eng)):
                s += str(i+1) + ". " + array_eng[i] + " -- " + array_rus[i] + "\n"
        await message.answer(s, reply_markup = numbers_kbrd)
    else:
        for i in range(10, 20):
                s += str(i+1) + ". " + array_eng[i] + " -- " + array_rus[i] + "\n"
        await message.answer(s, reply_markup = numbers_kbrd)

@user_private.message(F.text=="3 страница")
async def second_page_cmd(message: types.Message):
    array_eng = output_engwords(message.from_user.id)
    array_rus = output_ruswords(message.from_user.id)
    s = ""
    if len(array_eng) <= 30:
        for i in range(20, len(array_eng)):
                s += str(i+1) + ". " + array_eng[i] + " -- " + array_rus[i] + "\n"
        await message.answer(s, reply_markup = numbers_kbrd)
    else:
        for i in range(20, 30):
                s += str(i+1) + ". " + array_eng[i] + " -- " + array_rus[i] + "\n"
        await message.answer(s, reply_markup = numbers_kbrd)

@user_private.message(F.text=="4 страница")
async def second_page_cmd(message: types.Message):
    array_eng = output_engwords(message.from_user.id)
    array_rus = output_ruswords(message.from_user.id)
    s = ""
    if len(array_eng) <= 40:
        for i in range(30, len(array_eng)):
                s += str(i+1) + ". " + array_eng[i] + " -- " + array_rus[i] + "\n"
        await message.answer(s, reply_markup = numbers_kbrd)
    else:
        for i in range(30, 40):
                s += str(i+1) + ". " + array_eng[i] + " -- " + array_rus[i] + "\n"
        await message.answer(s, reply_markup = numbers_kbrd)

@user_private.message(F.text=="Нет, не хочу")
async def no_idont_want_cmd(message: types.Message):
    array_eng = output_engwords(message.from_user.id)
    await message.answer("Вот список слов, добавленных в ваш словарь, удачного изучения 🙂", reply_markup = numbers_kbrd_withoutTranslate)
    s = ""
    if len(array_eng) <= 10:
        for i in range(len(array_eng)):
            s += str(i+1) + ". " + array_eng[i] + "\n"
        await message.answer(s)
    else:
        for i in range(0, 10):
            s += str(i+1) + ". " + array_eng[i] + "\n"
        await message.answer(s)

@user_private.message(F.text=="Первая страница")
async def no_idont_want_cmd(message: types.Message):
    array_eng = output_engwords(message.from_user.id)
    s = ""
    if len(array_eng) <= 10:
        for i in range(0, len(array_eng)):
            s += str(i+1) + ". " + array_eng[i] + "\n"
        await message.answer(s)
    else:
        for i in range(0, 10):
            s += str(i+1) + ". " + array_eng[i] + "\n"
        await message.answer(s)

@user_private.message(F.text=="Вторая страница")
async def no_idont_want_cmd(message: types.Message):
    array_eng = output_engwords(message.from_user.id)
    s = ""
    if len(array_eng) <= 20:
        for i in range(10, len(array_eng)):
            s += str(i+1) + ". " + array_eng[i] + "\n"
        await message.answer(s)
    else:
        for i in range(10, 20):
            s += str(i+1) + ". " + array_eng[i] + "\n"
        await message.answer(s)

@user_private.message(F.text=="Третья страница")
async def no_idont_want_cmd(message: types.Message):
    array_eng = output_engwords(message.from_user.id)
    s = ""
    if len(array_eng) <= 30:
        for i in range(20, len(array_eng)):
            s += str(i+1) + ". " + array_eng[i] + "\n"
        await message.answer(s)
    else:
        for i in range(20, 30):
            s += str(i+1) + ". " + array_eng[i] + "\n"
        await message.answer(s)

@user_private.message(F.text=="Четвертая страница")
async def no_idont_want_cmd(message: types.Message):
    array_eng = output_engwords(message.from_user.id)
    s = ""
    if len(array_eng) <= 40:
        for i in range(30, len(array_eng)):
            s += str(i+1) + ". " + array_eng[i] + "\n"
        await message.answer(s)
    else:
        for i in range(30, 40):
            s += str(i+1) + ". " + array_eng[i] + "\n"
        await message.answer(s)

@user_private.message(F.text=="Вернуться в меню словаря")
async def cancel_to_dictionary_cmd(message: types.message):
    await message.answer("Вы успешно вернулись в меню словаря", reply_markup = my_dictionary_kbrd)

@user_private.message(F.text=="Назад")
async def cancel_to_main_menu_cmd(message: types.Message):
    await message.answer("Вы успешно вернулись в главное меню", reply_markup=start_kbrd)

@user_private.message(F.text=="Удалить слово")
async def delete_word_from_list_cmd(message: types.Message, state: FSMContext):
    await state.set_state(DeleteWord.eng_word)
    await message.answer("Введите словао на английском, которое хотите удалить")

@user_private.message(DeleteWord.eng_word)
async def delete_now_cmd(message: types.Message, state: FSMContext):
    delete_word(message.text, message.from_user.id)
    data = await state.get_data()
    await state.clear()
    await message.answer("Слово успешно удалено!", reply_markup=my_dictionary_kbrd)


array_for_check_knowLedges = []
count = 0

mistakes_engWord = []
mistakes_rusWordReal = []
mistakes_rusWordUser = []


@user_private.message(F.text == "Проверка знаний 📚")
async def check_knowLedge_cmd(message: types.Message, state: FSMContext):
    await message.answer("Вам будет предоставлен тест - 5 английских слов, перевод которым вам нужно написать, удачи ;)")
    global array_for_check_knowLedges
    array_for_check_knowLedges = random_engWords(message.from_user.id)
    addWordsForKnowLedgesInDB(message.from_user.id, array_for_check_knowLedges)
    await state.set_state(CheckKnowledge.word1)
    first_word = outputFirstWord(message.from_user.id)
    await message.answer("Введите первого слова -> " + str(first_word))


@user_private.message(CheckKnowledge.word1)
async def check_knowLedge1_cmd(message: types.Message, state: FSMContext):
    global array_for_check_knowLedges, mistakes_rusWordUser, mistakes_engWord, mistakes_rusWordReal, count
    real_translate = outputRusWord(array_for_check_knowLedges[0], message.from_user.id)
    if real_translate.lower() == message.text.lower():
        count += 1
    else:
        mistakes_engWord.append(array_for_check_knowLedges[0])
        mistakes_rusWordReal.append(real_translate)
        mistakes_rusWordUser.append(message.text)
    await state.set_state(CheckKnowledge.word2)
    second_word = outputSecondWord(message.from_user.id)
    await message.answer("Введите второго слова -> " + str(second_word))


@user_private.message(CheckKnowledge.word2)
async def check_knowLedge2_cmd(message: types.Message, state: FSMContext):
    global array_for_check_knowLedges, mistakes_rusWordUser, mistakes_engWord, mistakes_rusWordReal, count
    real_translate = outputRusWord(array_for_check_knowLedges[1], message.from_user.id)
    if real_translate.lower() == message.text.lower():
        count += 1
    else:
        mistakes_engWord.append(array_for_check_knowLedges[0])
        mistakes_rusWordReal.append(real_translate)
        mistakes_rusWordUser.append(message.text)
    await state.set_state(CheckKnowledge.word3)
    third_word = outputThirdWord(message.from_user.id)
    await message.answer("Введите третьего слова -> " + str(third_word))


@user_private.message(CheckKnowledge.word3)
async def check_knowLedge3_cmd(message: types.Message, state: FSMContext):
    global array_for_check_knowLedges, mistakes_rusWordUser, mistakes_engWord, mistakes_rusWordReal, count
    real_translate = outputRusWord(array_for_check_knowLedges[2], message.from_user.id)
    if real_translate.lower() == message.text.lower():
        count += 1
    else:
        mistakes_engWord.append(array_for_check_knowLedges[0])
        mistakes_rusWordReal.append(real_translate)
        mistakes_rusWordUser.append(message.text)
    await state.set_state(CheckKnowledge.word4)
    fourth_word = outputFourthWord(message.from_user.id)
    await message.answer("Введите четвертого слова -> " + str(fourth_word))


@user_private.message(CheckKnowledge.word4)
async def check_knowLedge4_cmd(message: types.Message, state: FSMContext):
    global array_for_check_knowLedges, mistakes_rusWordUser, mistakes_engWord, mistakes_rusWordReal, count
    real_translate = outputRusWord(array_for_check_knowLedges[3], message.from_user.id)
    if real_translate.lower() == message.text.lower():
        count += 1
    else:
        mistakes_engWord.append(array_for_check_knowLedges[0])
        mistakes_rusWordReal.append(real_translate)
        mistakes_rusWordUser.append(message.text)
    await state.set_state(CheckKnowledge.word5)
    fifth_word = outputFifthWord(message.from_user.id)
    await message.answer("Введите пятого слова -> " + str(fifth_word))


@user_private.message(CheckKnowledge.word5)
async def check_knowLedge5_cmd(message: types.Message, state: FSMContext):
    global array_for_check_knowLedges, mistakes_rusWordUser, mistakes_engWord, mistakes_rusWordReal, count
    real_translate = outputRusWord(array_for_check_knowLedges[4], message.from_user.id)
    if real_translate.lower() == message.text.lower():
        count += 1
    else:
        mistakes_engWord.append(array_for_check_knowLedges[0])
        mistakes_rusWordReal.append(real_translate)
        mistakes_rusWordUser.append(message.text)
    await message.answer(F"Количество правильных ответов = {count}/5")
    if count == 5:
        await message.answer("Молодец, все решено верно!")
    else:
        s = "Вы неправильно перевели следующие слова: " + "\n"
        qwe = len(s)
        for i in range(len(mistakes_engWord)):
            s += mistakes_engWord[i] + " -- " + mistakes_rusWordUser[i] + "\n"
        await message.answer(s)
    real_answers = ""
    for i in range(len(array_for_check_knowLedges)):
        real_answers += array_for_check_knowLedges[i] + " -- " + output_rusword(message.from_user.id,
                                                                                array_for_check_knowLedges[i]) + "\n"
    await message.answer("Ответы к тесту: " + "\n" + real_answers)
    await state.clear()
    array_for_check_knowLedges = []
    mistakes_engWord = []
    mistakes_rusWordReal = []
    mistakes_rusWordUser = []
    count = 0
    data = state.get_data()
    await state.clear()
    cleanWordsForTest(message.from_user.id)


@user_private.message(F.text == "Слово дня 💯")
async def wordOfDay(message: types.Message):
    word = parser_wordOfDay(
        "https://www.merriam-webster.com/word-of-the-day",
        "h2",
        "word-header-txt"
    )
    translator = Translator(from_lang="en", to_lang="ru")
    translate_word = translator.translate(word)
    await message.answer("Word of the day:" + "\n" +  word + " -- " + translate_word)














































