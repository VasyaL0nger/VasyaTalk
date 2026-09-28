import streamlit as st
import json
import os
import time

st.set_page_config(page_title="VasyaTalk Premium", layout="wide", page_icon="🐱")

DB_MESSAGES = "db_talks.json"

# --- ФУНКЦИИ БАЗЫ ДАННЫХ ---
def load_data():
    if os.path.exists(DB_MESSAGES):
        try:
            with open(DB_MESSAGES, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_data(data):
    with open(DB_MESSAGES, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

db_talks = load_data()

# Стартовая инициализация комнат, если база пустая
if not db_talks:
    db_talks = {
        "ЧАТ 1": [{"time": "12:00", "user": "Друг 1", "text": "Дарова бро как дела", "avatar": "v1.png"}],
        "ЧАТ 2": [{"time": "12:05", "user": "Друг 2", "text": "Погнали в кэт страйк, бро", "avatar": "v2.png"}],
        "ЧАТ 3": [{"time": "12:10", "user": "Друг 3", "text": "Бро щас на учебе не могу сорри", "avatar": "v4.png"}],
        "ЧАТ 4": [
            {"time": "13:00", "user": "Чат 4", "text": "Дарова брат", "avatar": "v5.png"},
            {"time": "13:01", "user": "Я", "text": "Дарова чё как", "avatar": "v3.png"},
            {"time": "13:02", "user": "Чат 4", "text": "Всё норм Бро", "avatar": "v5.png"},
            {"time": "13:03", "user": "Чат 4", "text": "Спорим на скин вынесу тебя в кэтстрайке", "avatar": "v5.png"}
        ],
        "ЧАТ 5": [{"time": "13:05", "user": "Друг 5", "text": "Бро этот ВасяТалк вообще имба", "avatar": "m4.png"}]
    }
    save_data(db_talks)

if "chat_user" not in st.session_state: st.session_state.chat_user = None
if "chat_avatar" not in st.session_state: st.session_state.chat_avatar = None

# ================= 🎨 ПРЕМИУМ-ИНТЕРФЕЙС СТРОГО ПО МАКЕТУ ПОЛЬЗОВАТЕЛЯ =================
st.markdown("""<style>
    /* Настройки главного фона — чистый и аккуратный */
    .stApp { background-color: #ffffff !important; color: #000000 !important; font-family: sans-serif !important; }
    
    /* Разделительная линия между левой панелью и чатом */
    div[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 3px solid #000000 !important; }
    
    /* Кнопки неактивных чатов в левой панели */
    .stButton>button { background-color: #ffffff !important; color: #000000 !important; border: 2px solid #000000 !important; border-radius: 0px !important; font-weight: bold !important; text-align: left !important; padding: 15px !important; margin-bottom: -5px !important; }
    
    /* Стилизация сообщений: Вражеские (Слева) и Мои (Справа) */
    .msg-left { text-align: left; margin-bottom: 15px; color: #000000; font-size: 18px; }
    .msg-right { text-align: right; margin-bottom: 15px; color: #000000; font-size: 18px; font-weight: bold; }
    
    /* Убираем лишние отступы Streamlit */
    div[data-testid="stBlock"] { padding: 0px !important; }
    input { border: 2px solid #000000 !important; border-radius: 0px !important; color: #000000 !important; }
</style>""", unsafe_allow_html=True)

# --- ФОРМА ВХОДА И ВЫБОРА ХАРИЗМАТИЧНЫХ АВАТАРОК ---
if st.session_state.chat_user is None:
    st.subheader("🔑 Регистрация в ВасяТалк")
    nickname = st.text_input("Введи свой никнейм для общения:", placeholder="Например: Я").strip()
    
    avatar_options = {
        "🐱 Василий Спецназ": "v1.png", "🟢 Василий Геймер": "v2.png", "🛠️ Василий Инженер": "v3.png",
        "🎒 Василий Студент": "v4.png", "🏴‍☠️ Капитан Василий": "v5.png", "🎀 Мурка Стримерша": "m1.png",
        "🕵️‍♀️ Мурка Агент": "m2.png", "🎓 Мурка Отличница": "m3.png", "👑 Мурка Premium": "m4.png", "⚓ Штурман Мурка": "m5.png"
    }
    avatar_choice = st.selectbox("Выбери боевого кота:", list(avatar_options.keys()))
    
    if st.button("🚀 ВОЙТИ В СЕТЬ"):
        if nickname:
            st.session_state.chat_user = nickname
            st.session_state.chat_avatar = avatar_options[avatar_choice]
            st.rerun()
        else: st.error("⚠️ Введите свой ник!")
    st.stop()

# --- ЛЕВАЯ ПАНЕЛЬ С КНОПКАМИ ЧАТОВ (МЕНЮ) ---
st.sidebar.markdown(f"👤 Ник: **{st.session_state.chat_user}**")
st.sidebar.write("---")

# Считаем последние сообщения для подписей в кнопках левой панели
chat1_last = db_talks["ЧАТ 1"][-1]["text"] if db_talks.get("ЧАТ 1") else ""
chat2_last = db_talks["ЧАТ 2"][-1]["text"] if db_talks.get("ЧАТ 2") else ""
chat3_last = db_talks["ЧАТ 3"][-1]["text"] if db_talks.get("ЧАТ 3") else ""
chat4_last = db_talks["ЧАТ 4"][-1]["text"] if db_talks.get("ЧАТ 4") else ""
chat5_last = db_talks["ЧАТ 5"][-1]["text"] if db_talks.get("ЧАТ 5") else ""
# Инициализируем выбранную комнату в памяти, если её нет
if "current_room" not in st.session_state:
    st.session_state.current_room = "ЧАТ 4"

# --- РЕНДЕР КНОПОК В ЛЕВОЙ ПАНЕЛИ С ЗЕЛЕНЫМ ВЫДЕЛЕНИЕМ (СТРОГО ПО МАКЕТУ) ---
# ЧАТ 1
if st.session_state.current_room == "ЧАТ 1":
    st.sidebar.markdown(f'<div style="background-color:#22c55e; border:2px solid #000000; padding:15px; color:#ffffff; font-weight:bold; margin-bottom:5px;"><h3>ЧАТ 1</h3><p style="margin:0;font-size:14px;color:#f0fdf4;">{chat1_last[:25]}...</p></div>', unsafe_allow_html=True)
else:
    if st.sidebar.button(f"ЧАТ 1\n\n{chat1_last[:20]}...", key="btn_c1", use_container_width=True):
        st.session_state.current_room = "ЧАТ 1"
        st.rerun()

# ЧАТ 2
if st.session_state.current_room == "ЧАТ 2":
    st.sidebar.markdown(f'<div style="background-color:#22c55e; border:2px solid #000000; padding:15px; color:#ffffff; font-weight:bold; margin-bottom:5px;"><h3>ЧАТ 2</h3><p style="margin:0;font-size:14px;color:#f0fdf4;">{chat2_last[:25]}...</p></div>', unsafe_allow_html=True)
else:
    if st.sidebar.button(f"ЧАТ 2\n\n{chat2_last[:20]}...", key="btn_c2", use_container_width=True):
        st.session_state.current_room = "ЧАТ 2"
        st.rerun()

# ЧАТ 3
if st.session_state.current_room == "ЧАТ 3":
    st.sidebar.markdown(f'<div style="background-color:#22c55e; border:2px solid #000000; padding:15px; color:#ffffff; font-weight:bold; margin-bottom:5px;"><h3>ЧАТ 3</h3><p style="margin:0;font-size:14px;color:#f0fdf4;">{chat3_last[:25]}...</p></div>', unsafe_allow_html=True)
else:
    if st.sidebar.button(f"ЧАТ 3\n\n{chat3_last[:20]}...", key="btn_c3", use_container_width=True):
        st.session_state.current_room = "ЧАТ 3"
        st.rerun()

# ЧАТ 4 (В стартовом макете он подсвечен зеленым)
if st.session_state.current_room == "ЧАТ 4":
    st.sidebar.markdown(f'<div style="background-color:#22c55e; border:2px solid #000000; padding:15px; color:#ffffff; font-weight:bold; margin-bottom:5px;"><h3>ЧАТ 4</h3><p style="margin:0;font-size:14px;color:#f0fdf4;">{chat4_last[:25]}...</p></div>', unsafe_allow_html=True)
else:
    if st.sidebar.button(f"ЧАТ 4\n\n{chat4_last[:20]}...", key="btn_c4", use_container_width=True):
        st.session_state.current_room = "ЧАТ 4"
        st.rerun()

# ЧАТ 5
if st.session_state.current_room == "ЧАТ 5":
    st.sidebar.markdown(f'<div style="background-color:#22c55e; border:2px solid #000000; padding:15px; color:#ffffff; font-weight:bold; margin-bottom:5px;"><h3>ЧАТ 5</h3><p style="margin:0;font-size:14px;color:#f0fdf4;">{chat5_last[:25]}...</p></div>', unsafe_allow_html=True)
else:
    if st.sidebar.button(f"ЧАТ 5\n\n{chat5_last[:20]}...", key="btn_c5", use_container_width=True):
        st.session_state.current_room = "ЧАТ 5"
        st.rerun()


# ================= 🌐 ПРАВАЯ ЗОНА ПЕРЕПИСКИ (ОКНО ЧАТА) =================
active_room = st.session_state.current_room
room_messages = db_talks.get(active_room, [])

# Блок вывода сообщений
chat_box = st.container()

with chat_box:
    for msg in room_messages:
        # Ссылка на аватарку на GitHub
        avatar_path = msg.get('avatar', 'v1.png')
        avatar_img_url = f"https://githubusercontent.com{avatar_path}"
        
        # Разделяем сообщения по краям (Мои — направо, Друзей — налево)
        if msg['user'] == "Я" or msg['user'] == st.session_state.chat_user:
            st.markdown(f"""
            <div class="msg-right">
                <span style="font-size:12px; color:#64748b; margin-right:8px;">{msg['time']}</span>
                {msg['text']} : <img src="{avatar_img_url}" width="35" style="border-radius:50%; vertical-align:middle; margin-left:5px;" onerror="this.style.display='none'"> <b>{msg['user']}</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-left">
                <img src="{avatar_img_url}" width="35" style="border-radius:50%; vertical-align:middle; margin-right:5px;" onerror="this.style.display='none'"> <b>{msg['user']}</b>: {msg['text']}
                <span style="font-size:12px; color:#64748b; margin-left:8px;">{msg['time']}</span>
            </div>
            """, unsafe_allow_html=True)

# Нижний разделитель перед полем ввода
st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- НИЖНЕЕ ПОЛЕ ВВОДА СООБЩЕНИЯ С АВТО-ОЧИСТКОЙ ---
with st.form("send_msg_form", clear_on_submit=True):
    user_message = st.text_input("", placeholder="Напиши тут сообщение...")
    send_btn = st.form_submit_button("🚀")
    
    if send_btn and user_message:
        # Добавляем новое сообщение в активную комнату
        new_msg_data = {
            "time": time.strftime("%H:%M"),
            "user": st.session_state.chat_user,
            "text": user_message.strip(),
            "avatar": st.session_state.chat_avatar
        }
        db_talks[active_room].append(new_msg_data)
        save_data(db_talks)
        st.rerun()
