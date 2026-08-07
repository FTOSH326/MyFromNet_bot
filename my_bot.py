import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from telebot.formatting import escape_html
from telebot.apihelper import ApiTelegramException
import random
import json
import os
import threading
import time

# ================= الإعدادات الأساسية =================
TOKEN = "8875575510:AAEsKbhxntev_MOQpd5nRWhq4jpdiT_RJ_s" # توكن البوت الخاص بك
bot = telebot.TeleBot(TOKEN)

# 🛑 المطور الأساسي (المالك) 🛑
DEV_ID = 6748284002

# مسارات الملفات (الصور والفيديو)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_VIDEO = os.path.join(BASE_DIR, "gametime.mp4")       # فيديو بداية اللعبة (بدلاً من الصورة)
TIMER_VIDEO = os.path.join(BASE_DIR, "timer.gif.mp4")             
HIDE_TIMER_VIDEO = os.path.join(BASE_DIR, "hide_timer2.mp4")   
               
PUNISH_MEDIA = os.path.join(BASE_DIR, "punish.jpg")           

WINNER_VIDEO = os.path.join(BASE_DIR, "winer.mp4")           # فيديو احتفال الفريق الفائز
DRAW_VIDEO = os.path.join(BASE_DIR, "draw.mp4")               # فيديو التعادل
STOP_VIDEO = os.path.join(BASE_DIR, "stop.mp4")               # فيديو إيقاف اللعبة
      

# ================= ملفات الحفظ =================
DATA_FILE = "mheibes_data.json"   
DB_FILE = "bot_database.json"     

# ================= قاموس اللغات للعبة =================
LANG = {
    "ar": {
        "welcome": "أهلاً بك في بوت لعبة المحيبس! 💍✨\n\nأضفني إلى مجموعتك، واكتب (محيبس) أو /play لبدء التحدي!",
        "lang_set": "✅ | تم تعيين اللغة العربية بنجاح.",
        "started": "📢 | بـدأت لـعـبـة الــ **مـحـيـبـس** 💍🔥\n\nالساحة جاهزة والتحدي بانتظاركم.\nدوس على (🙋‍♂️ أشارك) لتسجيل اسمك وحجز مكانك في الفريق:",
        "join_btn": "🙋‍♂️ | أشارك",
        "start_btn": "🎮 | ابدأ اللعبة",
        "stop_btn": "🛑 | إنهاء اللعبة",
        "joined": "👥 | اللاعبون :\n{}",
        "max_players": "⚠️ | اكتمل العدد! الحد الأقصى هو 20 لاعباً (10 لكل فريق).",
        "not_even": "⚠️ | عدد اللاعبين فردي! نحتاج إلى لاعب إضافي لتوزيع الفرق بالتساوي.",
        "too_few": "⚠️ | لا يمكن بدء اللعبة! نحتاج إلى لاعبين اثنين على الأقل.",
        "voting": "🗳️ | تصويت سريع لتحديد عدد الجولات!\n\n⏳ الوقت المتبقي: {} ثانية",
        "voted": "✅ | تم تسجيل تصويتك لـ {} جولات!",
        "round_set": "✅ | انتهى التصويت! ستكون اللعبة من: {} جولات 🔥",
        "teams_ready": "✅ | تم توزيع الفرق! 🔥\n\n🔴 الفريق الأحمر:\n{}\n👑 الكابتن: {}\n\n🔵 الفريق الأزرق:\n{}\n👑 الكابتن: {}",
        "captains_changed": "🔄 | وصلنا لمنتصف اللعبة! تم تغيير الكباتن عشوائياً لزيادة الحماس 🔥\n\n👑 كابتن الفريق الأحمر الجديد: {}\n👑 كابتن الفريق الأزرق الجديد: {}",
        "check_dm": "يا {}، يرجى مراجعة الخاص فوراً! 🏃‍♂️\nأرسلت لك تعليمات إخفاء المحبس. 💍🤫",
        "dm_hide": "👑 | أنت الكابتن في هذه الجولة!\n\nاختر اليد التي ستخبئ فيها المحبس عند أحد لاعبي فريقك: ✊👀",
        "ring_hidden": "✅ | تم إخفاء المحبس بنجاح! 🤫💍\n\nعُد إلى المجموعة وانتظر تخمين الفريق الخصم.",
        "hide_prompt": "⏳ | أمام الكابتن {} **20 ثانية** فقط لإخفاء المحبس!",
        "hide_timeout": "⏰ | انتهى الوقت! الكابتن {} تأخر في إخفاء المحبس.. 😴\n🔴 تم معاقبة الفريق وإضافة **نقطة مجانية** للفريق الخصم!",
        "guess_turn": "🕵️‍♂️ | حان دور الفريق الخصم للتخمين!\n\nوقع الاختيار على اللاعب {} للبحث عن المحبس! 🎯",
        "guess_prompt": "{}, حان دورك! أين تتوقع وجود المحبس؟ ✊🧐\n\n⏳ أمامك 30 ثانية قبل أن تخسر النقطة!",
        "guess_timer": "\n\n⏳ الوقت المتبقي: {} ثانية",
        "timeout": "⏰ | انتهى الوقت! تأخر اللاعب {} في التخمين.. 😴\n🔴 نقطة مجانية تضاف للفريق الخصم!",
        "correct": "🎉 | تخمين صحيح يا {}! 🎯\nتمت إضافة نقطة إلى فريقك! 👏",
        "wrong": "❌ | تخمين خاطئ! 💔\nالمحبس كان في {} للاعب {}.",
        "score": "📊 | النتيجة الحالية:\n🔴 الفريق الأحمر: {} نقطة\n🔵 الفريق الأزرق: {} نقطة",
        "game_over": "🏁 | انتهت اللعبة! 🎊\n\n🏆 النتيجة:\n{}\n\n📊 النقاط النهائية:\n🔴 الفريق الأحمر: {} | 🔵 الفريق الأزرق: {}",
        "dm_error": "⚠️ | عذراً، الخاص مغلق لدى الكابتن! 📬\nيرجى من الكابتن الدخول للبوت وإرسال /start أولاً.",
        "private_only": "❌ | هذه اللعبة مخصصة للمجموعات فقط. أضفني إلى مجموعتك للبدء. 👥",
        "no_game": "⚠️ | لا توجد لعبة قائمة حالياً. اكتب (محيبس) لبدء لعبة جديدة. 🔄",
        "already_started": "⚠️ | اللعبة بدأت بالفعل، يرجى الانتظار للجولة القادمة! 🔥",
        "already_joined": "✅ | أنت مسجل في اللعبة مسبقاً!",
        "not_your_turn": "❌ | ليس دورك الآن! يرجى الانتظار حتى يحين دور فريقك. 🤫",
        "draw": "🤝 | انتهت اللعبة بالتعادل!",
        "right_hand": "✋ اليد اليسرى",
        "left_hand": "🤚 اليد اليمنى",
        "game_stopped": "🛑 | تم إنهاء اللعبة من قبل المشرف. 🚶‍♂️",
        "no_permission": "❌ | عذراً، فقط المشرفون يمكنهم إنهاء اللعبة. 🛡️"
    },
    "en": {
        "welcome": "Welcome to the Mheibes Bot! 💍✨\n\nAdd me to your group, and type (محيبس) or /play to start the challenge!",
        "lang_set": "✅ | Language successfully set to English.",
        "started": "📢 | The **Mheibes** game has started! 💍🔥\n\nThe stage is set and the challenge awaits.",
        "join_btn": "🙋‍♂️ | Join",
        "start_btn": "🎮 | Start Game",
        "stop_btn": "🛑 | End Game",
        "joined": "👥 | Registered Players:\n{}",
        "max_players": "⚠️ | Capacity reached! The maximum limit is 20 players.",
        "not_even": "⚠️ | The number of players is odd! One more player is needed to balance the teams.",
        "too_few": "⚠️ | We need at least 2 players to start the game.",
        "voting": "🗳️ | Quick vote for the number of rounds!\n\n⏳ Time left: {} seconds",
        "voted": "✅ | Your vote for {} rounds has been recorded.",
        "round_set": "✅ | Voting ended! The game will consist of {} rounds. 🔥",
        "teams_ready": "✅ | Teams have been formed! 🔥\n\n🔴 Red Team:\n{}\n👑 Captain: {}\n\n🔵 Blue Team:\n{}\n👑 Captain: {}",
        "captains_changed": "🔄 | Halfway point! Captains have been changed randomly. 🔥\n\n👑 New Red Captain: {}\n👑 New Blue Captain: {}",
        "check_dm": "Hey {}, please check your private messages! 🏃‍♂️\nI sent you instructions to hide the ring. 💍🤫",
        "dm_hide": "👑 | You are the Captain for this round!\n\nSelect the hand to hide the ring in for your teammate: ✊👀",
        "ring_hidden": "✅ | The ring has been successfully hidden! 🤫💍\n\nReturn to the group and wait for the guess.",
        "hide_prompt": "⏳ | Captain {} has only **20 seconds** to hide the ring!",
        "hide_timeout": "⏰ | Time's up! Captain {} took too long to hide the ring.. 😴\n🔴 A penalty point is awarded to the opposing team!",
        "guess_turn": "🕵️‍♂️ | It's the opposing team's turn to guess!\n\nPlayer {} has been chosen to find the ring! 🎯",
        "guess_prompt": "{}, it's your turn! Where is the ring? ✊🧐\n\n⏳ You have 30 seconds to guess.",
        "guess_timer": "\n\n⏳ Time remaining: {} seconds",
        "timeout": "⏰ | Time's up! Player {} took too long to guess. 😴\n🔴 A penalty point is awarded to the opposing team!",
        "correct": "🎉 | Correct guess, {}! 🎯\nA point has been added to your team! 👏",
        "wrong": "❌ | Wrong guess! 💔\nThe ring was in {}'s {}.",
        "score": "📊 | Current Score:\n🔴 Red Team: {} points\n🔵 Blue Team: {} points",
        "game_over": "🏁 | Game Over! 🎊\n\n🏆 Result:\n{}\n\n📊 Final Score:\n🔴 Red Team: {} | 🔵 Blue Team: {}",
        "dm_error": "⚠️ | Cannot send a message to the Captain because their private chat is restricted! 📬\nThey must send /start to the bot in private first.",
        "private_only": "❌ | This game is intended for groups only. Please add me to a group to play. 👥",
        "no_game": "⚠️ | There is no active game right now. Type (محيبس) to start one. 🔄",
        "already_started": "⚠️ | The game has already started. Please wait for the next round! 🔥",
        "already_joined": "✅ | You are already registered in the game!",
        "not_your_turn": "❌ | It is not your turn to guess! Please wait for your team's turn. 🤫",
        "draw": "🤝 | The game ended in a draw!",
        "right_hand": "✋ Right Hand",
        "left_hand": "🤚 Left Hand",
        "game_stopped": "🛑 | The game has been cancelled by an admin. 🚶‍♂️",
        "no_permission": "❌ | Sorry, only group admins can stop the game. 🛡️"
    }
}
# ================= الذاكرة المؤقتة =================
games = {}

# ================= دوال مساعدة =================
def load_db():
    db_data = {"users": [], "groups": [], "langs": {}, "devs": []}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            for key in db_data:
                if key not in loaded:
                    loaded[key] = db_data[key]
            return loaded
    return db_data

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

db = load_db()

def register_chat(chat_id, chat_type):
    global db
    updated = False
    if chat_type == "private":
        if chat_id not in db["users"]:
            db["users"].append(chat_id)
            updated = True
    elif chat_type in ["group", "supergroup"]:
        if chat_id not in db["groups"]:
            db["groups"].append(chat_id)
            updated = True
    if updated:
        save_db(db)

def get_lang(chat_id):
    return db["langs"].get(str(chat_id), "ar")

def get_text(chat_id, key):
    return LANG[get_lang(chat_id)][key]

def set_lang(chat_id, lang):
    global db
    db["langs"][str(chat_id)] = lang
    save_db(db)

def is_dev(user_id):
    return user_id == DEV_ID or user_id in db.get("devs", [])

def check_admin(chat_id, user_id):
    if is_dev(user_id):
        return True
    try:
        member = bot.get_chat_member(chat_id, user_id)
        if member.status in ['administrator', 'creator']:
            return True
    except Exception:
        pass
    return False

def get_mention(user_id, name):
    return f"[{name}](tg://user?id={user_id})"

def update_game_message(message, text, reply_markup=None):
    for _ in range(3):
        try:
            if message.photo or message.document or message.video:
                bot.edit_message_caption(caption=text, chat_id=message.chat.id, message_id=message.message_id, reply_markup=reply_markup, parse_mode="Markdown")
            else:
                bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=message.message_id, reply_markup=reply_markup, parse_mode="Markdown")
            break
        except ApiTelegramException as e:
            if e.error_code == 429:
                time.sleep(e.result_json.get('parameters', {}).get('retry_after', 5))
            else:
                break
        except Exception:
            break

def send_timer(chat_id, text, markup, video_path=TIMER_VIDEO):
    for _ in range(3):
        try:
            if os.path.exists(video_path):
                try:
                    with open(video_path, 'rb') as video:
                        msg = bot.send_video(chat_id, video, caption=text, reply_markup=markup, parse_mode="Markdown")
                        return msg, True
                except ApiTelegramException as e:
                    if e.error_code == 429:
                        time.sleep(e.result_json.get('parameters', {}).get('retry_after', 5))
                        continue
                except Exception:
                    pass

            msg = bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
            return msg, False

        except ApiTelegramException as e:
            if e.error_code == 429:
                time.sleep(e.result_json.get('parameters', {}).get('retry_after', 5))
            else:
                break
        except Exception:
            break

    msg = bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    return msg, False

# ================= التنبيه عند إضافة البوت لمجموعة =================
@bot.message_handler(content_types=['new_chat_members'])
def on_bot_added(message):
    for new_member in message.new_chat_members:
        if new_member.id == bot.get_me().id:
            chat_id = message.chat.id
            chat_title = escape_html(message.chat.title)
            register_chat(chat_id, message.chat.type)
            
            try:
                invite_link = bot.export_chat_invite_link(chat_id)
            except Exception:
                invite_link = "البوت ليس (أدمن) ولا يمتلك صلاحية إنشاء رابط للدعوة ❌"
                
            dev_msg = f"🆕 | تم إضافة البوت إلى مجموعة جديدة!\n\n📌 <b>اسم المجموعة:</b> {chat_title}\n🆔 <b>ايدي المجموعة:</b> <code>{chat_id}</code>\n🔗 <b>الرابط:</b> {invite_link}"
            
            try:
                bot.send_message(DEV_ID, dev_msg, parse_mode="HTML")
            except Exception:
                pass

# ================= أوامر البداية والإدارة =================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    chat_id = message.chat.id
    register_chat(chat_id, message.chat.type)
    msg = get_text(chat_id, "welcome")
    
    if os.path.exists(GAME_VIDEO):
        try:
            with open(GAME_VIDEO, 'rb') as video:
                bot.send_video(chat_id, video, caption=msg, parse_mode="Markdown")
            return
        except Exception: pass
        
    bot.send_message(chat_id, msg, parse_mode="Markdown")

@bot.message_handler(commands=['lang', 'language'])
def language_cmd(message):
    chat_id = message.chat.id
    register_chat(chat_id, message.chat.type)
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("العربية 🇮🇶", callback_data="setlang_ar"),
        InlineKeyboardButton("English 🇬🇧", callback_data="setlang_en")
    )
    bot.send_message(chat_id, "اختر لغتك المفضلة / Select your language:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "احصائيات")
@bot.message_handler(commands=['stats'])
def stats_cmd(message):
    if not is_dev(message.from_user.id):
        bot.reply_to(message, "❌ | عذراً، هذا الأمر مخصص للمطورين فقط.")
        return
        
    users_count = len(db.get("users", []))
    groups_count = len(db.get("groups", []))
    
    stat_msg = f"📊 | إحصائيات البوت الحالية:\n\n👥 <b>عدد المستخدمين (في الخاص):</b> {users_count}\n🌐 <b>عدد المجموعات:</b> {groups_count}"
    bot.reply_to(message, stat_msg, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "الكروبات")
@bot.message_handler(commands=['groups'])
def groups_list_cmd(message):
    if not is_dev(message.from_user.id):
        bot.reply_to(message, "❌ | عذراً، هذا الأمر مخصص للمطورين فقط.")
        return

    groups = db.get("groups", [])
    if not groups:
        bot.reply_to(message, "⚠️ | لا توجد مجموعات مسجلة حالياً في قاعدة البيانات.")
        return

    wait_msg = bot.reply_to(message, "⏳ | جاري فحص وجلب بيانات المجموعات... يرجى الانتظار.")
    
    msg_text = "📋 | <b>قائمة المجموعات الحالية:</b>\n\n"
    count = 1
    active_groups_count = 0
    
    for chat_id in groups:
        try:
            chat = bot.get_chat(chat_id)
            title = escape_html(chat.title)
            
            try:
                link = bot.export_chat_invite_link(chat_id)
            except Exception:
                link = "بدون صلاحية (أدمن) ❌"
            
            group_info = f"{count}. <b>{title}</b>\n🆔 <code>{chat_id}</code>\n🔗 {link}\n\n"
            
            if len(msg_text) + len(group_info) > 3800:
                bot.send_message(message.chat.id, msg_text, parse_mode="HTML", disable_web_page_preview=True)
                msg_text = "" 
                
            msg_text += group_info
            count += 1
            active_groups_count += 1
            
        except Exception:
            continue
            
    try:
        bot.delete_message(message.chat.id, wait_msg.message_id)
    except Exception:
        pass

    if active_groups_count == 0:
        bot.send_message(message.chat.id, "❌ | يبدو أن البوت تم طرده من جميع المجموعات المسجلة أو لم يعد يمتلك وصولاً لها.")
    elif msg_text:
        bot.send_message(message.chat.id, msg_text, parse_mode="HTML", disable_web_page_preview=True)

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "ايقاف")
@bot.message_handler(commands=['stop'])
def stop_game_cmd(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        bot.reply_to(message, get_text(chat_id, "private_only"))
        return
    if chat_id not in games:
        bot.reply_to(message, get_text(chat_id, "no_game"))
        return
    if not check_admin(chat_id, message.from_user.id):
        bot.reply_to(message, get_text(chat_id, "no_permission"))
        return
    
    games.pop(chat_id, None)
    stop_msg = get_text(chat_id, "game_stopped")
    
    try:
        if os.path.exists(STOP_VIDEO):
            with open(STOP_VIDEO, 'rb') as f:
                bot.send_video(chat_id, f, caption=stop_msg, parse_mode="Markdown")
        else:
            bot.reply_to(message, stop_msg, parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, stop_msg, parse_mode="Markdown")

# ================= بدء اللعبة =================
@bot.message_handler(func=lambda m: m.text and m.text.strip() == "محيبس")
@bot.message_handler(commands=['play'])
def start_game_cmd(message):
    chat_id = message.chat.id
    register_chat(chat_id, message.chat.type)
    
    if message.chat.type == "private":
        bot.reply_to(message, get_text(chat_id, "private_only"))
        return

    games[chat_id] = {
        "status": "waiting",
        "players": {}, 
        "team_a": [],
        "team_b": [],
        "cap_a": None,
        "cap_b": None,
        "score_a": 0,
        "score_b": 0,
        "round": 1,
        "total_rounds": 5,
        "turn": "A", 
        "holder": None,
        "holder_hand": None, 
        "guesser": None,
        "votes": {}, 
        "guess_made": False,
        "hide_made": False,
        "turn_id": 0,
        "captains_changed": False
    }

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(get_text(chat_id, "join_btn"), callback_data="join_game"),
        InlineKeyboardButton(get_text(chat_id, "start_btn"), callback_data="vote_start")
    )
    markup.row(InlineKeyboardButton(get_text(chat_id, "stop_btn"), callback_data="stop_game"))
    
    welcome_msg = get_text(chat_id, "started")
    
    if os.path.exists(GAME_VIDEO):
        try:
            with open(GAME_VIDEO, 'rb') as video:
                bot.send_video(chat_id, video, caption=welcome_msg, reply_markup=markup, parse_mode="Markdown")
            return
        except Exception: pass
        
    bot.send_message(chat_id, welcome_msg, reply_markup=markup, parse_mode="Markdown")

# ================= الخيوط الزمنية (Timers Threads) =================
def hiding_timer(chat_id, turn_id, message_id, text_base, is_video):
    for remaining in range(20, 0, -5):
        game = games.get(chat_id)
        if not game or game["turn_id"] != turn_id or game["hide_made"]:
            try: bot.delete_message(chat_id, message_id)
            except Exception: pass
            return
            
        new_text = text_base + get_text(chat_id, "guess_timer").format(remaining)
        try:
            if is_video:
                bot.edit_message_caption(caption=new_text, chat_id=chat_id, message_id=message_id, parse_mode="Markdown")
            else:
                bot.edit_message_text(new_text, chat_id=chat_id, message_id=message_id, parse_mode="Markdown")
        except ApiTelegramException as e:
            if e.error_code == 429:
                time.sleep(e.result_json.get('parameters', {}).get('retry_after', 5))
        except Exception: pass
        time.sleep(5)
        
    game = games.get(chat_id)
    if game and game["turn_id"] == turn_id and not game["hide_made"]:
        game["hide_made"] = True
        
        try: bot.delete_message(chat_id, message_id)
        except Exception: pass

        hiding_team_cap = game["cap_a"] if game["turn"] == "A" else game["cap_b"]
        cap_mention = get_mention(hiding_team_cap, game["players"][hiding_team_cap])
        punish_msg = get_text(chat_id, "hide_timeout").format(cap_mention)
        
        try:
            if os.path.exists(PUNISH_MEDIA):
                if PUNISH_MEDIA.endswith('.mp4'):
                    with open(PUNISH_MEDIA, 'rb') as f:
                        bot.send_video(chat_id, f, caption=punish_msg, parse_mode="Markdown")
                else:
                    with open(PUNISH_MEDIA, 'rb') as f:
                        bot.send_photo(chat_id, f, caption=punish_msg, parse_mode="Markdown")
            else:
                bot.send_message(chat_id, punish_msg, parse_mode="Markdown")
        except Exception:
            bot.send_message(chat_id, punish_msg, parse_mode="Markdown")
            
        if game["turn"] == "A": game["score_b"] += 1
        else: game["score_a"] += 1
        
        bot.send_message(chat_id, get_text(chat_id, "score").format(game["score_a"], game["score_b"]), parse_mode="Markdown")
        
        game["turn"] = "B" if game["turn"] == "A" else "A"
        if game["turn"] == "A": game["round"] += 1
        play_turn(chat_id, game)

def voting_timer(chat_id, message_id, is_video):
    game = games.get(chat_id)
    if not game: return
    
    for remaining in range(30, 0, -5):
        if chat_id not in games or games[chat_id]["status"] != "voting": return
            
        if len(games[chat_id]["votes"]) == len(games[chat_id]["players"]): break
            
        text = get_text(chat_id, "voting").format(remaining)
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("3 جولات", callback_data="vote_3"), InlineKeyboardButton("5 جولات", callback_data="vote_5"))
        row2 = [InlineKeyboardButton("7 جولات", callback_data="vote_7"), InlineKeyboardButton("9 جولات", callback_data="vote_9")]
        if len(games[chat_id]["players"]) > 10: row2.append(InlineKeyboardButton("15 جولة", callback_data="vote_15"))
        markup.row(*row2)

        try:
            if is_video:
                bot.edit_message_caption(caption=text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")
            else:
                bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")
        except ApiTelegramException as e:
            if e.error_code == 429:
                time.sleep(e.result_json.get('parameters', {}).get('retry_after', 5))
        except Exception: pass
        time.sleep(5)
        
    if chat_id in games and games[chat_id]["status"] == "voting":
        votes = list(games[chat_id]["votes"].values())
        final_rounds = max(set(votes), key=votes.count) if votes else 5
        games[chat_id]["total_rounds"] = final_rounds
        try: bot.delete_message(chat_id, message_id)
        except Exception: pass
        try: bot.send_message(chat_id, get_text(chat_id, "round_set").format(final_rounds), parse_mode="Markdown")
        except Exception: pass
        start_rounds(chat_id, games[chat_id])

def guessing_timer(chat_id, turn_id, message_id, text_base, markup, is_video):
    for remaining in range(30, 0, -5):
        game = games.get(chat_id)
        if not game or game["turn_id"] != turn_id or game["guess_made"]: return
            
        new_text = text_base + get_text(chat_id, "guess_timer").format(remaining)
        try:
            if is_video:
                bot.edit_message_caption(caption=new_text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")
            else:
                bot.edit_message_text(new_text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")
        except ApiTelegramException as e:
            if e.error_code == 429:
                time.sleep(e.result_json.get('parameters', {}).get('retry_after', 5))
        except Exception: pass
        time.sleep(5)
        
    game = games.get(chat_id)
    if game and game["turn_id"] == turn_id and not game["guess_made"]:
        game["guess_made"] = True
        try: bot.delete_message(chat_id, message_id)
        except Exception: pass

        guesser_mention = get_mention(game["guesser"], game["players"][game["guesser"]])
        bot.send_message(chat_id, get_text(chat_id, "timeout").format(guesser_mention), parse_mode="Markdown")
        
        if game["turn"] == "A": game["score_a"] += 1
        else: game["score_b"] += 1
        
        bot.send_message(chat_id, get_text(chat_id, "score").format(game["score_a"], game["score_b"]), parse_mode="Markdown")
        
        game["turn"] = "B" if game["turn"] == "A" else "A"
        if game["turn"] == "A": game["round"] += 1
        play_turn(chat_id, game)

# ================= معالجة الأزرار =================
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    user = call.from_user
    data = call.data
    register_chat(chat_id, call.message.chat.type)

    if data.startswith("setlang_"):
        set_lang(chat_id, data.split("_")[1])
        bot.answer_callback_query(call.id, get_text(chat_id, "lang_set"))
        update_game_message(call.message, get_text(chat_id, "lang_set"))
        return

    if data == "stop_game":
        if chat_id not in games:
            bot.answer_callback_query(call.id, get_text(chat_id, "no_game"))
            return
        if not check_admin(chat_id, user.id):
            bot.answer_callback_query(call.id, get_text(chat_id, "no_permission"), show_alert=True)
            return
        
        update_game_message(call.message, get_text(chat_id, "game_stopped"))
        games.pop(chat_id, None)
        
        try:
            if os.path.exists(STOP_VIDEO):
                with open(STOP_VIDEO, 'rb') as f:
                    bot.send_video(chat_id, f, parse_mode="Markdown")
        except Exception: pass
        return

    if data.startswith("hide_"):
        parts = data.split("_")
        group_id = int(parts[1])
        holder_id = int(parts[2])
        holder_hand = parts[3] 

        if group_id not in games:
            try:
                update_game_message(call.message, "تم إلغاء اللعبة في المجموعة.")
            except Exception: pass
            return

        g = games[group_id]
        
        if g["hide_made"] or g["status"] != "playing":
            bot.answer_callback_query(call.id, "انتهى وقتك أو تم إخفاء المحبس بالفعل!", show_alert=True)
            return

        g["hide_made"] = True
        g["turn_id"] += 1 
        g["holder"] = holder_id
        g["holder_hand"] = holder_hand
        
        try:
            update_game_message(call.message, get_text(group_id, "ring_hidden"))
        except Exception: pass

        guessing_team = g["team_b"] if g["turn"] == "A" else g["team_a"]
        g["guesser"] = random.choice(guessing_team)
        guesser_mention = get_mention(g["guesser"], g["players"][g["guesser"]])

        bot.send_message(group_id, get_text(group_id, "guess_turn").format(guesser_mention), parse_mode="Markdown")

        hiding_team = g["team_a"] if g["turn"] == "A" else g["team_b"]
        markup = InlineKeyboardMarkup()
        for p in hiding_team:
            p_name = g["players"][p]
            markup.row(
                InlineKeyboardButton(f"{p_name} - " + get_text(group_id, "right_hand"), callback_data=f"guess_{p}_R"),
                InlineKeyboardButton(f"{p_name} - " + get_text(group_id, "left_hand"), callback_data=f"guess_{p}_L")
            )

        text_base = get_text(group_id, "guess_prompt").format(guesser_mention)
        msg, is_video = send_timer(group_id, text_base + get_text(group_id, "guess_timer").format(30), markup)
        threading.Thread(target=guessing_timer, args=(group_id, g["turn_id"], msg.message_id, text_base, markup, is_video)).start()
        return

    if chat_id not in games:
        bot.answer_callback_query(call.id, get_text(chat_id, "no_game"), show_alert=True)
        return

    g = games[chat_id]

    if data == "join_game":
        if g["status"] != "waiting":
            bot.answer_callback_query(call.id, get_text(chat_id, "already_started"), show_alert=True)
            return
        if user.id in g["players"]:
            bot.answer_callback_query(call.id, get_text(chat_id, "already_joined"), show_alert=True)
            return
        if len(g["players"]) >= 20:
            bot.answer_callback_query(call.id, get_text(chat_id, "max_players"), show_alert=True)
            return

        g["players"][user.id] = user.first_name
        
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton(get_text(chat_id, "join_btn"), callback_data="join_game"),
            InlineKeyboardButton(get_text(chat_id, "start_btn"), callback_data="vote_start")
        )
        markup.row(InlineKeyboardButton(get_text(chat_id, "stop_btn"), callback_data="stop_game"))
        
        player_list = "\n".join([f"👤 {name}" for name in g["players"].values()])
        text = get_text(chat_id, "started") + "\n\n" + get_text(chat_id, "joined").format(player_list)
        update_game_message(call.message, text, markup)
        return

    if data == "vote_start":
        if len(g["players"]) < 2:
            bot.answer_callback_query(call.id, get_text(chat_id, "too_few"), show_alert=True)
            return
        if len(g["players"]) % 2 != 0:
            bot.answer_callback_query(call.id, get_text(chat_id, "not_even"), show_alert=True)
            return
            
        g["status"] = "voting"
        text = get_text(chat_id, "voting").format(30)
        
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("3 جولات", callback_data="vote_3"), InlineKeyboardButton("5 جولات", callback_data="vote_5"))
        row2 = [InlineKeyboardButton("7 جولات", callback_data="vote_7"), InlineKeyboardButton("9 جولات", callback_data="vote_9")]
        if len(g["players"]) > 10:
            row2.append(InlineKeyboardButton("15 جولة", callback_data="vote_15"))
        markup.row(*row2)
        
        update_game_message(call.message, text, markup)
        is_vid = bool(call.message.video or call.message.photo or call.message.document)
        threading.Thread(target=voting_timer, args=(chat_id, call.message.message_id, is_vid)).start()
        return

    if data.startswith("vote_") and data != "vote_start":
        if g["status"] != "voting": return
        if user.id not in g["players"]:
            bot.answer_callback_query(call.id, "عذراً، يجب أن تشترك في اللعبة أولاً!", show_alert=True)
            return
            
        r_count = int(data.split("_")[1])
        g["votes"][user.id] = r_count
        bot.answer_callback_query(call.id, get_text(chat_id, "voted").format(r_count))
        return

    if data.startswith("guess_"):
        if g["status"] != "playing": return
        if user.id != g["guesser"]:
            bot.answer_callback_query(call.id, get_text(chat_id, "not_your_turn"), show_alert=True)
            return
            
        if g["guess_made"]: return
        g["guess_made"] = True
        g["turn_id"] += 1
        
        try: bot.delete_message(chat_id, call.message.message_id)
        except Exception: pass
        
        parts = data.split("_")
        guessed_player = int(parts[1])
        guessed_hand = parts[2]
        
        guesser_mention = get_mention(g["guesser"], g["players"][g["guesser"]])
        holder_mention = get_mention(g["holder"], g["players"][g["holder"]])
        hand_text = get_text(chat_id, "right_hand") if g["holder_hand"] == "R" else get_text(chat_id, "left_hand")

        if guessed_player == g["holder"] and guessed_hand == g["holder_hand"]:
            result_msg = get_text(chat_id, "correct").format(guesser_mention)
            if g["turn"] == "A": g["score_b"] += 1
            else: g["score_a"] += 1
            
            try:
                if os.path.exists(WIN_VIDEO):
                    with open(WIN_VIDEO, 'rb') as video:
                        bot.send_video(chat_id, video, caption=result_msg, parse_mode="Markdown")
                else:
                    bot.send_message(chat_id, result_msg, parse_mode="Markdown")
            except Exception:
                bot.send_message(chat_id, result_msg, parse_mode="Markdown")

        else:
            result_msg = get_text(chat_id, "wrong").format(hand_text, holder_mention) if get_lang(chat_id) == "ar" else get_text(chat_id, "wrong").format(holder_mention, hand_text)
            if g["turn"] == "A": g["score_a"] += 1
            else: g["score_b"] += 1
            
            try:
                if os.path.exists(LOSE_VIDEO):
                    with open(LOSE_VIDEO, 'rb') as video:
                        bot.send_video(chat_id, video, caption=result_msg, parse_mode="Markdown")
                else:
                    bot.send_message(chat_id, result_msg, parse_mode="Markdown")
            except Exception:
                bot.send_message(chat_id, result_msg, parse_mode="Markdown")
            
        bot.send_message(chat_id, get_text(chat_id, "score").format(g["score_a"], g["score_b"]), parse_mode="Markdown")
        
        g["turn"] = "B" if g["turn"] == "A" else "A"
        if g["turn"] == "A": g["round"] += 1
        play_turn(chat_id, g)
        return

def start_rounds(chat_id, g):
    players_list = list(g["players"].keys())
    random.shuffle(players_list)
    mid = len(players_list) // 2
    g["team_a"] = players_list[:mid]
    g["team_b"] = players_list[mid:]
    g["cap_a"] = g["team_a"][0]
    g["cap_b"] = g["team_b"][0]
    
    a_names = "\n".join([f"👤 {g['players'][p]}" for p in g["team_a"]])
    b_names = "\n".join([f"👤 {g['players'][p]}" for p in g["team_b"]])
    cap_a_mention = get_mention(g["cap_a"], g["players"][g["cap_a"]])
    cap_b_mention = get_mention(g["cap_b"], g["players"][g["cap_b"]])
    
    bot.send_message(chat_id, get_text(chat_id, "teams_ready").format(a_names, cap_a_mention, b_names, cap_b_mention), parse_mode="Markdown")
    g["status"] = "playing"
    play_turn(chat_id, g)

def play_turn(chat_id, g):
    if g["round"] > g["total_rounds"]:
        end_game(chat_id, g)
        return
        
    if not g["captains_changed"] and g["round"] > (g["total_rounds"] // 2):
        g["cap_a"] = random.choice(g["team_a"])
        g["cap_b"] = random.choice(g["team_b"])
        g["captains_changed"] = True
        cap_a_m = get_mention(g["cap_a"], g["players"][g["cap_a"]])
        cap_b_m = get_mention(g["cap_b"], g["players"][g["cap_b"]])
        bot.send_message(chat_id, get_text(chat_id, "captains_changed").format(cap_a_m, cap_b_m), parse_mode="Markdown")

    hiding_team = g["team_a"] if g["turn"] == "A" else g["team_b"]
    hiding_team_cap = g["cap_a"] if g["turn"] == "A" else g["cap_b"]
    cap_mention = get_mention(hiding_team_cap, g["players"][hiding_team_cap])

    g["hide_made"] = False
    g["guess_made"] = False
    g["turn_id"] += 1
    
    markup = InlineKeyboardMarkup()
    for p in hiding_team:
        p_name = g["players"][p]
        markup.row(
            InlineKeyboardButton(f"{p_name} - " + get_text(chat_id, "right_hand"), callback_data=f"hide_{chat_id}_{p}_R"),
            InlineKeyboardButton(f"{p_name} - " + get_text(chat_id, "left_hand"), callback_data=f"hide_{chat_id}_{p}_L")
        )

    dm_msg = get_text(chat_id, "dm_hide")
    try:
        if os.path.exists(HIDE_PHOTO):
            with open(HIDE_PHOTO, 'rb') as f:
                bot.send_photo(hiding_team_cap, f, caption=dm_msg, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(hiding_team_cap, dm_msg, reply_markup=markup, parse_mode="Markdown")
            
        bot.send_message(chat_id, get_text(chat_id, "check_dm").format(cap_mention), parse_mode="Markdown")
        
        text_base = get_text(chat_id, "hide_prompt").format(cap_mention)
        msg, is_video = send_timer(chat_id, text_base + get_text(chat_id, "guess_timer").format(20), None, HIDE_TIMER_VIDEO)
        threading.Thread(target=hiding_timer, args=(chat_id, g["turn_id"], msg.message_id, text_base, is_video)).start()
        
    except Exception:
        bot.send_message(chat_id, get_text(chat_id, "dm_error"), parse_mode="Markdown")
        g["status"] = "waiting"

def end_game(chat_id, g):
    if g["score_a"] > g["score_b"]:
        result = "🏆 فاز الفريق الأحمر! 🔴🎉" if get_lang(chat_id) == "ar" else "🏆 Red Team Wins! 🔴🎉"
        vid = WINNER_VIDEO
    elif g["score_b"] > g["score_a"]:
        result = "🏆 فاز الفريق الأزرق! 🔵🎉" if get_lang(chat_id) == "ar" else "🏆 Blue Team Wins! 🔵🎉"
        vid = WINNER_VIDEO
    else:
        result = get_text(chat_id, "draw")
        vid = DRAW_VIDEO

    msg = get_text(chat_id, "game_over").format(result, g["score_a"], g["score_b"])
    
    if os.path.exists(vid):
        try:
            with open(vid, 'rb') as f:
                bot.send_video(chat_id, f, caption=msg, parse_mode="Markdown")
        except Exception:
            bot.send_message(chat_id, msg, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, msg, parse_mode="Markdown")
        
    games.pop(chat_id, None)

print("Bot is running...")
bot.infinity_polling()
