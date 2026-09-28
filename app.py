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

if "chat_user" not in st.session_state: st.session_state.chat_user = None
if "chat_avatar" not in st.session_state: st.session_state.chat_avatar = None
if "current_room" not in st.session_state: st.session_state.current_room = None

# ================= 🎨 НОЧНОЙ ХАКЕРСКИЙ ИНТЕРФЕЙС (ЧЕРНОЕ БЕЛОЕ + ЗЕЛЕНЫЙ) =================
st.markdown("""<style>
    /* Весь интерфейс становится черным, текст — белым */
    .stApp { background-color: #08080c !important; color: #ffffff !important; font-family: sans-serif !important; }
    
    /* Боковое меню — черное с белой жирной разделительной линией */
    div[data-testid="stSidebar"] { background-color: #08080c !important; border-right: 3px solid #ffffff !important; color: #ffffff !important; }
    div[data-testid="stSidebar"] .stMarkdown, div[data-testid="stSidebar"] label { color: #ffffff !important; }
    
    /* Кнопки неактивных чатов — черные с белой рамкой и белым текстом */
    .stButton>button { background-color: #08080c !important; color: #ffffff !important; border: 2px solid #ffffff !important; border-radius: 0px !important; font-weight: bold !important; text-align: left !important; padding: 12px !important; margin-bottom: -5px !important; }
    .stButton>button:hover { background-color: #1c1c24 !important; border-color: #22c55e !important; }
    
    /* Стилизация сообщений строго по макету */
    .msg-left { text-align: left; margin-bottom: 12px; color: #ffffff; font-size: 18px; }
    .msg-right { text-align: right; margin-bottom: 12px; color: #ffffff; font-size: 18px; font-weight: bold; }
    
    /* Текстовые поля ввода */
    input { background-color: #12121a !important; border: 2px solid #ffffff !important; border-radius: 0px !important; color: #ffffff !important; }
    
    /* Форма отправки внизу */
    div[data-testid="stForm"] { background-color: #08080c !important; border: none !important; padding: 0px !important; }
</style>""", unsafe_allow_html=True)

# --- ОКНО ВХОДА И ВЫБОРА АВАТАРОК ---
if st.session_state.chat_user is None:
    st.markdown("<h2 style='color:#ffffff; text-align:center;'>🔑 Вход в сеть VasyaTalk</h2>", unsafe_allow_html=True)
    nickname = st.text_input("Введи свой пацанский никнейм:", placeholder="Например: Снайпер_Рыжий").strip()
    
    avatar_options = {
        "🐱 Василий Спецназ": "v1.png", "🟢 Василий Геймер": "v2.png", "🛠️ Василий Инженер": "v3.png",
        "🎒 Василий Студент": "v4.png", "🏴‍☠️ Капитан Василий": "v5.png", "🎀 Мурка Стримерша": "m1.png",
        "🕵️‍♀️ Мурка Агент": "m2.png", "🎓 Мурка Отличница": "m3.png", "👑 Мурка Premium": "m4.png", "⚓ Штурман Мурка": "m5.png"
    }
    avatar_choice = st.selectbox("Выбери аватарку кота:", list(avatar_options.keys()))
    
    if st.button("🚀 ПОДКЛЮЧИТЬСЯ"):
        if nickname:
            st.session_state.chat_user = nickname
            st.session_state.chat_avatar = avatar_options[avatar_choice]
            st.rerun()
        else: st.error("⚠️ Никнейм не может быть пустым!")
    st.stop()

# --- ЛЕВАЯ ПАНЕЛЬ С СИСТЕМОЙ ПОИСКА И ДОБАВЛЕНИЯ ПО ЮЗЕРНЕЙМАМ ---
st.sidebar.markdown(f"👤 Кот в сети: **{st.session_state.chat_user}**")
st.sidebar.write("---")

st.sidebar.markdown("### 🔍 Добавить друга по нику")
new_friend = st.sidebar.text_input("", placeholder="Введи никнейм пацана...", key="find_friend_input").strip()

if st.sidebar.button("➕ Создать чат", use_container_width=True):
    if new_friend and new_friend != st.session_state.chat_user:
        if new_friend not in db_talks:
            # Создаем пустой лог чата для нового юзернейма
            db_talks[new_friend] = [{"time": time.strftime("%H:%M"), "user": "Система", "text": f"Секретный чат с {new_friend} успешно создан! 💥", "avatar": "v3.png"}]
            save_data(db_talks)
        st.session_state.current_room = new_friend
        st.rerun()
    elif new_friend == st.session_state.chat_user:
        st.sidebar.error("⚠️ Нельзя создать чат с самим собой!")

st.sidebar.write("---")
st.sidebar.markdown("### 💬 Твои переписки:")

# Если комната не выбрана, автоматически открываем первый доступный чат пацана
if st.session_state.current_room is None and db_talks:
    st.session_state.current_room = list(db_talks.keys())[0]
# --- ДИНАМИЧЕСКИЙ СВИСОК ЧАТОВ ПО ЮЗЕРНЕЙМАМ С ЗЕЛЕНЫМ ВЫДЕЛЕНИЕМ ---
if not db_talks:
    st.sidebar.caption("📭 Список чатов пуст. Добавь друга по нику выше!")
else:
    for friend_name in list(db_talks.keys()):
        last_msg = db_talks[friend_name][-1]["text"] if db_talks[friend_name] else "Нет сообщений"
        
        # Если чат активный — красим плашку в зеленый цвет (строго по макету)
        if st.session_state.current_room == friend_name:
            st.sidebar.markdown(f"""
            <div style="background-color:#22c55e; border:2px solid #ffffff; padding:12px; color:#ffffff; font-weight:bold; margin-bottom:5px;">
                <h4 style="margin:0; font-size:16px;">👤 {friend_name}</h4>
                <p style="margin:5px 0 0 0; font-size:13px; color:#f0fdf4; font-weight:normal; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{last_msg}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Неактивные чаты — обычные черные кнопки с белой рамкой
            if st.sidebar.button(f"👤 {friend_name}\n\n{last_msg[:20]}...", key=f"btn_{friend_name}", use_container_width=True):
                st.session_state.current_room = friend_name
                st.rerun()

# --- ВЫХОД ИЗ СИСТЕМЫ ---
st.sidebar.write("---")
if st.sidebar.button("🚪 Выйти из сети", use_container_width=True):
    st.session_state.chat_user = None
    st.session_state.chat_avatar = None
    st.session_state.current_room = None
    st.rerun()


# ================= 🌐 ЗОНА ПЕРЕПИСКИ ПО ЮЗЕРНЕЙМАМ (СТРОГО ПО МАКЕТУ) =================
if st.session_state.current_room is None:
    st.info("🎈 Создай или выбери чат в левой панели, чтобы начать тереть с пацанами!")
else:
    active_room = st.session_state.current_room
    st.markdown(f"## 💬 Чат: {active_room}")
    st.write("---")
    
    room_messages = db_talks.get(active_room, [])
    chat_box = st.container()
    
    with chat_box:
        for msg in room_messages:
            avatar_path = msg.get('avatar', 'v1.png')
            # Ссылка на аватарки, загруженные тобой в репозиторий GitHub
            avatar_img_url = f"https://githubusercontent.com{avatar_path}"
            
            # Разделяем сообщения по краям (Мои — направо, Друзей — налево)
            if msg['user'] == st.session_state.chat_user or msg['user'] == "Я":
                st.markdown(f"""
                <div class="msg-right">
                    <span style="font-size:12px; color:#a1a1aa; margin-right:8px;">{msg['time']}</span>
                    {msg['text']} : <img src="{avatar_img_url}" width="35" style="border-radius:50%; vertical-align:middle; margin-left:5px;" onerror="this.style.display='none'"> <b>{msg['user']}</b>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-left">
                    <img src="{avatar_img_url}" width="35" style="border-radius:50%; vertical-align:middle; margin-right:5px;" onerror="this.style.display='none'"> <b>{msg['user']}</b>: {msg['text']}
                    <span style="font-size:12px; color:#a1a1aa; margin-left:8px;">{msg['time']}</span>
                </div>
                """, unsafe_allow_html=True)

    # Отступ перед полем ввода внизу страницы
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # --- НИЖНЕЕ ПОЛЕ ВВОДА СООБЩЕНИЯ ---
    with st.form("send_msg_form", clear_on_submit=True):
        user_message = st.text_input("", placeholder="Напиши тут сообщение...")
        send_btn = st.form_submit_button("🚀")
        
        if send_btn and user_message:
            new_msg_data = {
                "time": time.strftime("%H:%M"),
                "user": st.session_state.chat_user,
                "text": user_message.strip(),
                "avatar": st.session_state.chat_avatar
            }
            db_talks[active_room].append(new_msg_data)
            save_data(db_talks)
            st.rerun()
