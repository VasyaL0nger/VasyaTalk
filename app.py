import streamlit as st
import json
import os
import time

st.set_page_config(page_title="VasyaTalk Premium", layout="wide", page_icon="🐱")

DB_MESSAGES = "db_talks.json"
DB_ONLINE = "db_online.json"

# --- ФУНКЦИИ БАЗЫ ДАННЫХ ---
def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

db_talks = load_data(DB_MESSAGES)
db_online = load_data(DB_ONLINE)

if "chat_user" not in st.session_state: st.session_state.chat_user = None
if "chat_avatar" not in st.session_state: st.session_state.chat_avatar = None
if "current_room" not in st.session_state: st.session_state.current_room = None

# Фиксация онлайна в сети (Фича №3)
current_time = time.time()
if st.session_state.chat_user:
    db_online[st.session_state.chat_user] = {"time": current_time, "avatar": st.session_state.chat_avatar}
    db_online = {u: t for u, t in db_online.items() if current_time - t["time"] < 300}
    save_data(db_online, DB_ONLINE)

# ================= 🎨 НОЧНОЙ ХАКЕРСКИЙ ИНТЕРФЕЙС =================
st.markdown("""<style>
    .stApp { background-color: #08080c !important; color: #ffffff !important; font-family: sans-serif !important; }
    div[data-testid="stSidebar"] { background-color: #08080c !important; border-right: 3px solid #ffffff !important; color: #ffffff !important; }
    div[data-testid="stSidebar"] .stMarkdown, div[data-testid="stSidebar"] label { color: #ffffff !important; }
    
    .stButton>button { background-color: #08080c !important; color: #ffffff !important; border: 2px solid #ffffff !important; border-radius: 0px !important; font-weight: bold !important; text-align: left !important; padding: 12px !important; margin-bottom: -5px !important; width: 100% !important; }
    .stButton>button:hover { background-color: #1c1c24 !important; border-color: #22c55e !important; }
    
    .msg-left { text-align: left; margin-bottom: 12px; color: #ffffff; font-size: 18px; }
    .msg-right { text-align: right; margin-bottom: 12px; color: #ffffff; font-size: 18px; font-weight: bold; }
    
    input { background-color: #12121a !important; border: 2px solid #ffffff !important; border-radius: 0px !important; color: #ffffff !important; }
    div[data-testid="stForm"] { background-color: #08080c !important; border: none !important; padding: 0px !important; }
    .online-user { display: inline-block; text-align: center; margin-right: 10px; margin-bottom: 10px; }
    
    audio { filter: invert(90%) hue-rotate(180deg); margin-top: 5px; max-width: 100%; }
    
    /* Красивая кнопка звонка в шапке */
    .call-link { display: inline-block; background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%); color: white !important; font-weight: bold; padding: 10px 20px; text-decoration: none; border-radius: 6px; border: 2px solid white; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3); }
    .call-link:hover { background: linear-gradient(135deg, #f87171 0%, #ef4444 100%); transform: scale(1.02); }
</style>""", unsafe_allow_html=True)

# --- ОКНО ВХОДА ---
if st.session_state.chat_user is None:
    st.markdown("<h2 style='color:#ffffff; text-align:center;'>🔑 Вход в сеть VasyaTalk</h2>", unsafe_allow_html=True)
    nickname = st.text_input("Введи свой пацанский никнейм:", placeholder="Например: Снайпер_Рыжий").strip()
    
    avatar_options = {
        "🐱 Василий Спецназ": "🐱", "🟢 Василий Геймер": "🟢", "🛠️ Василий Инженер": "🛠️",
        "🎒 Василий Студент": "🎒", "🏴‍☠️ Капитан Василий": "🏴‍☠️", "🎀 Мурка Стримерша": "🎀",
        "🕵️‍♀️ Мурка Агент": "🕵️‍♀️", "🎓 Мурка Отличница": "🎓", "👑 Мурка Premium": "👑", "⚓ Штурман Мурка": "⚓"
    }
    avatar_choice = st.selectbox("Выбери статус-иконку кота:", list(avatar_options.keys()))
    
    if st.button("🚀 ПОДКЛЮЧИТЬСЯ"):
        if nickname:
            st.session_state.chat_user = nickname
            st.session_state.chat_avatar = avatar_options[avatar_choice]
            db_online[nickname] = {"time": time.time(), "avatar": avatar_options[avatar_choice]}
            save_data(db_online, DB_ONLINE)
            st.rerun()
        else: st.error("⚠️ Никнейм не может быть пустым!")
    st.stop()

# --- ЛЕВАЯ ПАНЕЛЬ С СИСТЕМОЙ КОНТАКТОВ ---
st.sidebar.markdown(f"👤 Кот в сети: **{st.session_state.chat_user}**")
st.sidebar.write("---")

st.sidebar.markdown("### 🔍 Найти кота по нику")
new_friend = st.sidebar.text_input("", placeholder="Введи никнейм пацана...", key="find_friend_input").strip()

if st.sidebar.button("➕ Создать чат", use_container_width=True):
    if new_friend and new_friend != st.session_state.chat_user:
        room_key = "__".join(sorted([st.session_state.chat_user, new_friend]))
        if room_key not in db_talks:
            db_talks[room_key] = [{"time": time.strftime("%H:%M"), "user": "Система", "text": f"🔐 Секретный канал связи с {new_friend} установлен!", "avatar": "🛠️"}]
            save_data(db_talks, DB_MESSAGES)
        st.session_state.current_room = room_key
        st.rerun()
    elif new_friend == st.session_state.chat_user:
        st.sidebar.error("⚠️ Нельзя создать чат с самим собой!")

st.sidebar.write("---")
# --- ВЫВОД СЧЁТЧИКА ОНЛАЙНА (ФИЧА №3) ---
online_count = len(db_online) + 1
st.sidebar.markdown(f"### 👥 Коты в сети: `{online_count}`")

st.sidebar.markdown(f"""
<div class="online-user">
    <span style="font-size:24px; vertical-align:middle;">🐱</span><br>
    <span style="font-size:11px; color:#22c55e;">● Василий</span>
</div>
""", unsafe_allow_html=True)

for user_on, data_on in db_online.items():
    if user_on != "Кот Василий":
        st.sidebar.markdown(f"""
        <div class="online-user">
            <span style="font-size:24px; vertical-align:middle;">{data_on['avatar']}</span><br>
            <span style="font-size:11px; color:#22c55e;">● {user_on[:8]}</span>
        </div>
        """, unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.markdown("### 💬 Твои переписки:")

vasya_room = f"Кот_Василий__{st.session_state.chat_user}"
if vasya_room not in db_talks:
    db_talks[vasya_room] = [{"time": time.strftime("%H:%M"), "user": "Кот Василий", "text": "Дарова брат! Я всегда в сети. Чертежи на месте, пушки заряжены! Пиши, если что.", "avatar": "🐱"}]
    save_data(db_talks, DB_MESSAGES)

if st.session_state.current_room is None:
    st.session_state.current_room = vasya_room

# --- ВЫВОД СПИСКА ТВОИХ ДИАЛОГОВ ---
for room_id in list(db_talks.keys()):
    if st.session_state.chat_user in room_id or room_id.startswith("Кот_Василий__"):
        if room_id.startswith("Кот_Василий__"):
            display_name = "🐱 Кот Василий"
        else:
            names = room_id.split("__")
            display_name = names if names == st.session_state.chat_user else names
            
        last_msg = db_talks[room_id][-1]["text"] if db_talks[room_id] else "Нет сообщений"
        if last_msg.startswith("[AUDIO_"): last_msg = "🎙️ Голосовое сообщение"
        
        if st.session_state.current_room == room_id:
            st.sidebar.markdown(f"""
            <div style="background-color:#22c55e; border:2px solid #ffffff; padding:12px; color:#ffffff; font-weight:bold; margin-bottom:5px;">
                <h4 style="margin:0; font-size:16px;">{display_name}</h4>
                <p style="margin:5px 0 0 0; font-size:13px; color:#f0fdf4; font-weight:normal; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{last_msg}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.sidebar.button(f"{display_name}\n\n{last_msg[:20]}...", key=f"btn_{room_id}", use_container_width=True):
                st.session_state.current_room = room_id
                st.rerun()

st.sidebar.write("---")
if st.sidebar.button("🚪 Выйти из сети", use_container_width=True):
    st.session_state.chat_user = None
    st.session_state.chat_avatar = None
    st.session_state.current_room = None
    st.rerun()


# ================= 🌐 ЗОНА ПЕРЕПИСКИ (ИСПРАВЛЕНО: st.columns(2)) =================
active_room = st.session_state.current_room
raw_messages = db_talks.get(active_room, [])

if active_room.startswith("Кот_Василий__"):
    header_name = "🐱 Кот Василий"
else:
    names = active_room.split("__")
    header_name = names if names == st.session_state.chat_user else names

# ИСПРАВЛЕНО: Передали двойку внутрь st.columns(2), чтобы разбить шапку на две ровные части
col_h, col_call = st.columns(2)
with col_h:
    st.markdown(f"<h2>💬 Чат: {header_name}</h2>", unsafe_allow_html=True)
with col_call:
    clean_room_id = active_room.replace("__", "x").replace(" ", "").replace("@", "").replace("-", "")
    call_url = f"https://jit.si{clean_room_id}"
    st.markdown(f'<div style="text-align:right; margin-top:10px;"><a href="{call_url}" target="_blank" class="call-link">📞 ЗВОНОК</a></div>', unsafe_allow_html=True)

# Поисковый движок (Фича №9)
search_query = st.text_input("🔍 Найти слово в переписке:", placeholder="Введите текст для фильтрации...").strip().lower()
st.write("---")

if search_query:
    room_messages = [m for m in raw_messages if search_query in m['text'].lower() and not m['text'].startswith("[AUDIO_")]
else:
    room_messages = raw_messages

chat_box = st.container()

with chat_box:
    if not room_messages:
        st.info("Здесь пока тихо...")
    else:
        for msg in room_messages:
            av = msg.get('avatar', '🐱')
            
            if msg['text'].startswith("[AUDIO_BASE64_"):
                audio_base64 = msg['text'].replace("[AUDIO_BASE64_", "").replace("]", "")
                display_content = f'🎙️ <audio controls src="data:audio/wav;base64,{audio_base64}"></audio>'
            else:
                display_content = msg['text']
            
            if msg['user'] == st.session_state.chat_user or msg['user'] == "Я":
                st.markdown(f"""
                <div class="msg-right">
                    <span style="font-size:12px; color:#a1a1aa; margin-right:8px;">{msg['time']}</span>
                    {display_content} : <span style="font-size:24px; vertical-align:middle;">{av}</span> <b>{msg['user']}</b>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-left">
                    <span style="font-size:24px; vertical-align:middle;">{av}</span> <b>{msg['user']}</b>: {display_content}
                    <span style="font-size:12px; color:#a1a1aa; margin-left:8px;">{msg['time']}</span>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- ИНТЕГРАЦИЯ РЕКОРДЕРА ГОЛОСОВЫХ СООБЩЕНИЙ ---
st.write("🎙️ Записать аудио-сообщение пацанам:")
audio_value = st.audio_input("Нажми на микрофон для записи:")

if audio_value is not None:
    import base64
    audio_bytes = audio_value.read()
    audio_encoded = base64.b64encode(audio_bytes).decode('utf-8')
    
    if st.button("🚀 ОТПРАВИТЬ ГОЛОСОВУХУ", use_container_width=True):
        new_msg_data = {
            "time": time.strftime("%H:%M"),
            "user": st.session_state.chat_user,
            "text": f"[AUDIO_BASE64_{audio_encoded}]",
            "avatar": st.session_state.chat_avatar
        }
        db_talks[active_room].append(new_msg_data)
        save_data(db_talks, DB_MESSAGES)
        st.rerun()

# --- ОБЫЧНОЕ ТЕКСТОВОЕ ПОЛЕ ВВОДА ---
with st.form("send_msg_form", clear_on_submit=True):
    user_message = st.text_input("", placeholder="Напиши тут текстовое сообщение...")
    send_btn = st.form_submit_button("🚀 Отправить текст")
    
    if send_btn and user_message:
        new_msg_data = {
            "time": time.strftime("%H:%M"),
            "user": st.session_state.chat_user,
            "text": user_message.strip(),
            "avatar": st.session_state.chat_avatar
        }
        db_talks[active_room].append(new_msg_data)
        save_data(db_talks, DB_MESSAGES)
        st.rerun()
