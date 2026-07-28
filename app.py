import streamlit as st
import random
import pandas as pd
import json
import os

DATA_FILE = "tournament_data.json"

def save_data():
    data = {
        "players": st.session_state.get("players", []),
        "groups": st.session_state.get("groups", {}),
        "group_scores": st.session_state.get("group_scores", {}),
        "playoff_scores": st.session_state.get("playoff_scores", {})
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.session_state.players = data.get("players", [])
                st.session_state.groups = data.get("groups", {})
                st.session_state.group_scores = data.get("group_scores", {})
                st.session_state.playoff_scores = data.get("playoff_scores", {})
        except Exception as e:
            st.error(f"Ошибка загрузки данных: {e}")

st.set_page_config(
    page_title="Лига уличного футбола", 
    page_icon="⚽",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Подключение современных шрифтов и установка вашей картинки на фон
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@700;900&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        .stApp {
            background-color: #A3D2C2;
            background-image: linear-gradient(to bottom, #A3D2C2 82%, #228B45 82%);
            background-size: 100% 100%;
            background-attachment: fixed;
            color: #0F172A;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        h1 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 900 !important;
            font-size: 2.4rem !important;
            text-transform: uppercase;
            letter-spacing: 2px !important;
            color: #0F172A;
            text-align: center;
            margin-top: 10px !important;
            margin-bottom: 30px !important;
            text-shadow: 0 2px 10px rgba(255, 255, 255, 0.4);
        }
        
        h2, h3, .stHeader {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 1.2px !important;
            color: #0F172A !important;
            font-size: 1.35rem !important;
            border-left: 4px solid #1E293B;
            padding-left: 12px;
            margin-top: 25px !important;
            margin-bottom: 15px !important;
        }

        label, .stCheckbox label span, .stNumberInput label, .stSelectbox label, p {
            color: #1E293B !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        /* Поля ввода */
        div[data-baseweb="textarea"] {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
            backdrop-filter: blur(8px);
        }
        div[data-baseweb="textarea"] textarea {
            color: #0F172A !important;
            -webkit-text-fill-color: #0F172A !important;
            background-color: transparent !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            padding: 14px !important;
        }

        div[data-baseweb="input"] {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
        }
        div[data-baseweb="input"] input {
            color: #0F172A !important;
            font-weight: 600 !important;
        }

        /* Контейнеры-экспандеры */
        div[data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.88) !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
            border-radius: 18px !important;
            margin-bottom: 14px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04) !important;
            backdrop-filter: blur(10px);
        }
        div[data-testid="stExpander"] * {
            color: #0F172A !important;
        }

        /* Кнопки */
        .stButton>button {
            width: 100%;
            border-radius: 14px;
            height: 3.4em;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            background: #0F172A !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.25);
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(15, 23, 42, 0.35);
            background: #1E293B !important;
        }

        /* Датафреймы */
        div[data-testid="stDataFrame"] {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.04);
            backdrop-filter: blur(8px);
        }
        div[data-testid="stDataFrame"] * {
            color: #0F172A !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
        }

        /* Навигационные табы */
        button[data-baseweb="tab"] {
            color: #1E293B !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 12px 16px !important;
        }
        button[aria-selected="true"] {
            color: #0F172A !important;
            border-bottom: 3px solid #0F172A !important;
        }

        .stCaption {
            color: #334155 !important;
            font-weight: 500 !important;
            font-size: 13px !important;
        }

        hr {
            border-color: rgba(255, 255, 255, 0.4) !important;
            margin: 25px 0 !important;
        }

        /* Стилизованные иконки */
        .icon-svg {
            display: inline-block;
            vertical-align: middle;
            width: 18px;
            height: 18px;
            margin-right: 8px;
            fill: #0F172A;
        }
    </style>
""", unsafe_allow_html=True)

# SVG Шаблоны иконок
icon_ball = '<svg class="icon-svg" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 2.07c3.16.33 5.76 2.3 6.74 5.03h-4.35c-.41-1.35-1.2-2.6-2.39-3.53V4.07zM11 4.07v1.5c-1.19.93-1.98 2.18-2.39 3.53H4.26c.98-2.73 3.58-4.7 6.74-5.03zM4.07 11h4.62c.11 1.01.4 1.98.84 2.86l-3.27 3.27c-1.46-1.54-2.35-3.64-2.19-6.13zM12 20c-1.74 0-3.34-.58-4.64-1.57l3.41-3.41c.42.12.86.18 1.23.18s.81-.06 1.23-.18l3.41 3.41C15.34 19.42 13.74 20 12 20zm5.93-3.87l-3.27-3.27c.44-.88.73-1.85.84-2.86h4.62c.16 2.49-.73 4.59-2.19 6.13z"/></svg>'
icon_dice = '<svg class="icon-svg" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM7.5 18c-.83 0-1.5-.67-1.5-1.5S6.67 15 7.5 15s1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM7.5 9C6.67 9 6 8.33 6 7.5S6.67 6 7.5 6 9 6.67 9 7.5 8.33 9 7.5 9zm4.5 4.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4.5 4.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm0-9c-.83 0-1.5-.67-1.5-1.5S15.67 6 16.5 6s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>'
icon_calendar = '<svg class="icon-svg" viewBox="0 0 24 24"><path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/></svg>'
icon_chart = '<svg class="icon-svg" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg>'
icon_trophy = '<svg class="icon-svg" viewBox="0 0 24 24"><path d="M19 5h-2V3H7v2H5c-1.1 0-2 .9-2 2v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V19H7v2h10v-2h-3.001v-3.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v3.82C5.84 10.4 5 9.3 5 8zm14 0c0 1.3-.84 2.4-2 2.82V7h2v1z"/></svg>'
icon_save = '<svg class="icon-svg" viewBox="0 0 24 24"><path d="M17 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-5 16c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm3-10H5V5h10v4z"/></svg>'
icon_folder = '<svg class="icon-svg" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>'

st.markdown(f"<h1>{icon_ball} ЛИГА УЛИЧНОГО ФУТБОЛА</h1>", unsafe_allow_html=True)

if "initialized" not in st.session_state:
    st.session_state.players = []
    st.session_state.groups = {}
    st.session_state.group_scores = {}
    st.session_state.playoff_scores = {}
    load_data()
    st.session_state.initialized = True

with st.sidebar:
    st.markdown(f"<h3>{icon_save} Управление данными</h3>", unsafe_allow_html=True)
    if st.button("💾 Сохранить турнир"):
        save_data()
        st.success("Данные сохранены!")
        
    if st.button("🗑 Сбросить турнир"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.session_state.players = []
        st.session_state.groups = {}
        st.session_state.group_scores = {}
        st.session_state.playoff_scores = {}
        st.success("Турнир сброшен!")
        st.rerun()

tab1, tab2, tab3, tab4 = st.tabs([
    "🎲 Жеребьевка", 
    "📅 Календарь", 
    "📊 Группы", 
    "🏆 Результаты"
])

# ==========================================
# 1. ЖЕРЕБЬЕВКА С ВЫБОРОМ КОЛИЧЕСТВА ГРУПП
# ==========================================
with tab1:
    st.markdown(f"<h2>{icon_dice} Список участников и настройки</h2>", unsafe_allow_html=True)
    
    col_set1, col_set2 = st.columns(2)
    num_groups = col_set1.selectbox("Количество групп:", options=[1, 2, 3, 4], index=3)
    
    default_text = "\n".join(st.session_state.players) if st.session_state.players else "\n".join([f"Игрок {i}" for i in range(1, 13)])
    raw_players = st.text_area(
        "Введите ФИО игроков (по одному на строку):", 
        value=default_text, 
        height=180
    )
    
    if st.button("🎲 ПРОВЕСТИ ЖЕРЕБЬЕВКУ"):
        players_list = [p.strip() for p in raw_players.split("\n") if p.strip()]
        min_players = num_groups * 3
        if len(players_list) < min_players:
            st.error(f"Для {num_groups} групп(ы) нужно минимум {min_players} игроков (по 3 человека в группу)! У вас: {len(players_list)}.")
        else:
            st.session_state.players = players_list.copy()
            random.shuffle(players_list)
            
            all_group_names = ["Группа А", "Группа Б", "Группа В", "Группа Г"]
            group_names = all_group_names[:num_groups]
            st.session_state.groups = {g: [] for g in group_names}
            
            for i, p in enumerate(players_list):
                g_idx = i % num_groups
                st.session_state.groups[group_names[g_idx]].append(p)
                
            st.session_state.group_scores = {}
            st.session_state.playoff_scores = {}
            save_data()
            st.success("Игроки распределены по группам!")

    if st.session_state.groups:
        st.markdown("---")
        st.markdown(f"<h3>{icon_folder} Ручная корректировка групп</h3>", unsafe_allow_html=True)
        st.caption("Выберите новую группу для любого игрока, если нужно изменить распределение:")

        group_names = list(st.session_state.groups.keys())
        
        for player in st.session_state.players:
            current_group = next((g for g, p_list in st.session_state.groups.items() if player in p_list), group_names[0])
            
            new_group = st.selectbox(
                f"Игрок: {player}",
                options=group_names,
                index=group_names.index(current_group),
                key=f"select_{player}"
            )
            
            if new_group != current_group:
                st.session_state.groups[current_group].remove(player)
                st.session_state.groups[new_group].append(player)
                save_data()
                st.rerun()

        st.markdown("---")
        st.markdown(f"<h3>{icon_folder} Состав групп (Итоговый)</h3>", unsafe_allow_html=True)
        for g_name, g_players in st.session_state.groups.items():
            with st.expander(f"{g_name} ({len(g_players)} чел.)", expanded=True):
                for idx, pl in enumerate(g_players, 1):
                    st.write(f"**№{idx}.** <span style='color:#0F172A;'>{pl}</span>", unsafe_allow_html=True)

def get_group_matches(players):
    matches = []
    n = len(players)
    for i in range(n):
        for j in range(i + 1, n):
            matches.append((players[i], players[j]))
    return matches

def calculate_cross_table(g_name, players):
    n = len(players)
    stats = {p: {"И": 0, "В": 0, "Н": 0, "П": 0, "МЗ": 0, "МП": 0, "Очки": 0} for p in players}
    pair_res = {p1: {p2: "—" for p2 in players} for p1 in players}
    
    for p in players:
        pair_res[p][p] = "—"
        
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = players[i], players[j]
            key1 = f"{g_name}_{p1}_vs_{p2}"
            key2 = f"{g_name}_{p2}_vs_{p1}"
            
            key = key1 if key1 in st.session_state.group_scores else key2
            
            if key in st.session_state.group_scores:
                data = st.session_state.group_scores[key]
                s1, s2 = data.get("s1", 0), data.get("s2", 0)
                panna1, panna2 = data.get("panna1", False), data.get("panna2", False)
                
                if key == key2:
                    s1, s2 = s2, s1
                    panna1, panna2 = panna2, panna1
                
                txt1 = f"{s1}:{s2}" + (" [Панна]" if panna1 else "")
                txt2 = f"{s2}:{s1}" + (" [Панна]" if panna2 else "")
                pair_res[p1][p2] = txt1
                pair_res[p2][p1] = txt2
                
                stats[p1]["И"] += 1; stats[p2]["И"] += 1
                stats[p1]["МЗ"] += s1; stats[p1]["МП"] += s2
                stats[p2]["МЗ"] += s2; stats[p2]["МП"] += s1
                
                if panna1:
                    stats[p1]["В"] += 1; stats[p1]["Очки"] += 4; stats[p2]["П"] += 1
                elif panna2:
                    stats[p2]["В"] += 1; stats[p2]["Очки"] += 4; stats[p1]["П"] += 1
                elif s1 > s2:
                    stats[p1]["В"] += 1; stats[p1]["Очки"] += 3; stats[p2]["П"] += 1
                elif s1 < s2:
                    stats[p2]["В"] += 1; stats[p2]["Очки"] += 3; stats[p1]["П"] += 1
                else:
                    stats[p1]["Н"] += 1; stats[p2]["Н"] += 1
                    stats[p1]["Очки"] += 1; stats[p2]["Очки"] += 1

    temp_df = pd.DataFrame.from_dict(stats, orient="index")
    temp_df["Разница"] = temp_df["МЗ"] - temp_df["МП"]
    temp_df = temp_df.sort_values(by=["Очки", "Разница", "МЗ"], ascending=False)
    
    rows = []
    for idx, (p, row_stat) in enumerate(temp_df.iterrows(), 1):
        row_dict = {"Место": idx, "Игрок": p}
        for o_idx, opp in enumerate(players, 1):
            row_dict[f"№{o_idx}"] = pair_res[p][opp]
            
        row_dict.update({
            "И": row_stat["И"],
            "В": row_stat["В"],
            "Н": row_stat["Н"],
            "П": row_stat["П"],
            "Разница": row_stat["Разница"],
            "Очки": row_stat["Очки"]
        })
        rows.append(row_dict)
        
    df_cross = pd.DataFrame(rows)
    df_standings = temp_df.reset_index().rename(columns={"index": "Игрок"})
    return df_cross, df_standings

def get_current_standings():
    standings = {}
    if "groups" in st.session_state and st.session_state.groups:
        for g_name, g_players in st.session_state.groups.items():
            _, df_standing = calculate_cross_table(g_name, g_players)
            standings[g_name] = df_standing
    return standings

# ==========================================
# 2. КАЛЕНДАРЬ ИГР (ГРУППЫ + ПЛЕЙ-ОФФ)
# ==========================================
with tab2:
    if not st.session_state.groups:
        st.info("Проведите жеребьевку на первой вкладке.")
    else:
        st.markdown(f"<h3>{icon_calendar} Легенда посева (номера игроков в группах)</h3>", unsafe_allow_html=True)
        for g_name, g_players in st.session_state.groups.items():
            num_legend = ", ".join([f"**{g_name[7:]}{i+1}**: {p}" for i, p in enumerate(g_players)])
            st.markdown(f"**{g_name}:** {num_legend}")
            
        st.markdown("---")
        st.markdown(f"<h2>{icon_calendar} Матчи группового этапа</h2>", unsafe_allow_html=True)
        
        scores_updated = False
        
        for g_name, g_players in st.session_state.groups.items():
            with st.expander(f"{g_name} (Матчи)", expanded=True):
                matches = get_group_matches(g_players)
                g_code = g_name[7:]
                
                for p1, p2 in matches:
                    i1 = g_players.index(p1) + 1
                    i2 = g_players.index(p2) + 1
                    key = f"{g_name}_{p1}_vs_{p2}"
                    
                    old_data = st.session_state.group_scores.get(key, {})
                    def_s1 = old_data.get("s1", 0)
                    def_s2 = old_data.get("s2", 0)
                    def_p1 = old_data.get("panna1", False)
                    def_p2 = old_data.get("panna2", False)

                    st.markdown(f"{i1}{g_code} **{p1}** vs {i2}{g_code} **{p2}**")
                    c1, c2 = st.columns(2)
                    s1 = c1.number_input(f"Голы {p1}", min_value=0, value=def_s1, key=f"{key}_s1")
                    s2 = c2.number_input(f"Голы {p2}", min_value=0, value=def_s2, key=f"{key}_s2")
                    
                    cp1, cp2 = st.columns(2)
                    panna1 = cp1.checkbox(f"ПАННА от {p1}", value=def_p1, key=f"{key}_panna1")
                    panna2 = cp2.checkbox(f"ПАННА от {p2}", value=def_p2, key=f"{key}_panna2")
                    
                    new_val = {"s1": s1, "s2": s2, "panna1": panna1, "panna2": panna2}
                    if old_data != new_val:
                        st.session_state.group_scores[key] = new_val
                        scores_updated = True
                        
                    st.markdown("<hr style='margin:10px 0 !important;'>", unsafe_allow_html=True)

        if scores_updated:
            save_data()

        st.markdown("---")
        st.markdown(f"<h2>{icon_trophy} Плей-офф</h2>", unsafe_allow_html=True)
        
        standings = get_current_standings()
        num_groups = len(st.session_state.groups)
        
        if len(standings) != num_groups or any(len(df) < 2 for df in standings.values()):
            st.info("Завершите матчи в группах, чтобы сформировалась сетка плей-офф.")
        else:
            try:
                if "playoff_scores" not in st.session_state:
                    st.session_state.playoff_scores = {}
                po_scores = st.session_state.playoff_scores

                def handle_po_match(match_key, title, player1, player2):
                    st.markdown(f"### {title}")
                    st.markdown(f"**<span style='color:#0F172A;'>{player1}</span>** vs **<span style='color:#0F172A;'>{player2}</span>**", unsafe_allow_html=True)
                    
                    old_po = po_scores.get(match_key, {})
                    c1, c2 = st.columns(2)
                    sc1 = c1.number_input("Счет 1", min_value=0, value=old_po.get("sc1", 0), key=f"po_{match_key}_1")
                    sc2 = c2.number_input("Счет 2", min_value=0, value=old_po.get("sc2", 0), key=f"po_{match_key}_2")
                    p1_panna = c1.checkbox("Панна", value=old_po.get("p1_panna", False), key=f"po_panna_{match_key}_1")
                    p2_panna = c2.checkbox("Панна", value=old_po.get("p2_panna", False), key=f"po_panna_{match_key}_2")
                    
                    new_po = {"sc1": sc1, "sc2": sc2, "p1_panna": p1_panna, "p2_panna": p2_panna}
                    if old_po != new_po:
                        po_scores[match_key] = new_po
                        save_data()

                    winner, loser = player1, player2
                    if p1_panna:
                        winner, loser = player1, player2
                    elif p2_panna:
                        winner, loser = player2, player1
                    elif sc1 > sc2:
                        winner, loser = player1, player2
                    elif sc2 > sc1:
                        winner, loser = player2, player1
                    return winner, loser

                group_names_keys = list(standings.keys())
                
                if num_groups == 4:
                    p1A = standings["Группа А"]["Игрок"].iloc[0]
                    p2A = standings["Группа А"]["Игрок"].iloc[1]
                    p1B = standings["Группа Б"]["Игрок"].iloc[0]
                    p2B = standings["Группа Б"]["Игрок"].iloc[1]
                    p1V = standings["Группа В"]["Игрок"].iloc[0]
                    p2V = standings["Группа В"]["Игрок"].iloc[1]
                    p1G = standings["Группа Г"]["Игрок"].iloc[0]
                    p2G = standings["Группа Г"]["Игрок"].iloc[1]

                    qf_pairs = [
                        ("qf_1", "1/4 #1 (1А vs 2Г)", p1A, p2G),
                        ("qf_2", "1/4 #2 (1В vs 2Б)", p1V, p2B),
                        ("qf_3", "1/4 #3 (1Б vs 2В)", p1B, p2V),
                        ("qf_4", "1/4 #4 (1Г vs 2А)", p1G, p2A),
                    ]
                    qf_winners, qf_losers = [], []
                    for m_key, title, pl1, pl2 in qf_pairs:
                        with st.expander(title, expanded=True):
                            w, l = handle_po_match(m_key, title, pl1, pl2)
                            qf_winners.append(w)
                            qf_losers.append(l)

                    st.markdown(f"<h3>{icon_trophy} 1/2 Финала</h3>", unsafe_allow_html=True)
                    sf_pairs = [
                        ("sf_1", "1/2 #1", qf_winners[0], qf_winners[1]),
                        ("sf_2", "1/2 #2", qf_winners[2], qf_winners[3])
                    ]
                    sf_winners, sf_losers = [], []
                    for m_key, title, pl1, pl2 in sf_pairs:
                        with st.expander(title, expanded=True):
                            w, l = handle_po_match(m_key, title, pl1, pl2)
                            sf_winners.append(w)
                            sf_losers.append(l)

                    st.markdown(f"<h3>{icon_trophy} Финальная стадия</h3>", unsafe_allow_html=True)
                    with st.expander("Матч за 3-е место", expanded=True):
                        handle_po_match("m3", "Матч за 3-е место", sf_losers[0], sf_losers[1])
                    with st.expander("ФИНАЛ", expanded=True):
                        handle_po_match("final", "Финальный матч", sf_winners[0], sf_winners[1])

                elif num_groups == 2:
                    p1A = standings["Группа А"]["Игрок"].iloc[0]
                    p2A = standings["Группа А"]["Игрок"].iloc[1]
                    p1B = standings["Группа Б"]["Игрок"].iloc[0]
                    p2B = standings["Группа Б"]["Игрок"].iloc[1]

                    st.markdown(f"<h3>{icon_trophy} 1/2 Финала (Перекрестный плей-офф)</h3>", unsafe_allow_html=True)
                    sf_pairs = [
                        ("sf_1", "1/2 #1 (1А vs 2Б)", p1A, p2B),
                        ("sf_2", "1/2 #2 (1Б vs 2А)", p1B, p2A)
                    ]
                    sf_winners, sf_losers = [], []
                    for m_key, title, pl1, pl2 in sf_pairs:
                        with st.expander(title, expanded=True):
                            w, l = handle_po_match(m_key, title, pl1, pl2)
                            sf_winners.append(w)
                            sf_losers.append(l)

                    st.markdown(f"<h3>{icon_trophy} Финальная стадия</h3>", unsafe_allow_html=True)
                    with st.expander("Матч за 3-е место", expanded=True):
                        handle_po_match("m3", "Матч за 3-е место", sf_losers[0], sf_losers[1])
                    with st.expander("ФИНАЛ", expanded=True):
                        handle_po_match("final", "Финальный матч", sf_winners[0], sf_winners[1])

                elif num_groups == 3:
                    p1A = standings["Группа А"]["Игрок"].iloc[0]
                    p1B = standings["Группа Б"]["Игрок"].iloc[0]
                    p1V = standings["Группа В"]["Игрок"].iloc[0]
                    second_places = []
                    for g in ["Группа А", "Группа Б", "Группа В"]:
                        second_places.append((standings[g]["Игрок"].iloc[1], standings[g]["Очки"].iloc[1], standings[g]["Разница"].iloc[1]))
                    second_places.sort(key=lambda x: (x[1], x[2]), reverse=True)
                    best_2nd = second_places[0][0]

                    st.markdown(f"<h3>{icon_trophy} 1/2 Финала</h3>", unsafe_allow_html=True)
                    sf_pairs = [
                        ("sf_1", "1/2 #1 (1А vs Лучший 2-й)", p1A, best_2nd),
                        ("sf_2", "1/2 #2 (1Б vs 1В)", p1B, p1V)
                    ]
                    sf_winners, sf_losers = [], []
                    for m_key, title, pl1, pl2 in sf_pairs:
                        with st.expander(title, expanded=True):
                            w, l = handle_po_match(m_key, title, pl1, pl2)
                            sf_winners.append(w)
                            sf_losers.append(l)

                    st.markdown(f"<h3>{icon_trophy} Финальная стадия</h3>", unsafe_allow_html=True)
                    with st.expander("Матч за 3-е место", expanded=True):
                        handle_po_match("m3", "Матч за 3-е место", sf_losers[0], sf_losers[1])
                    with st.expander("ФИНАЛ", expanded=True):
                        handle_po_match("final", "Финальный матч", sf_winners[0], sf_winners[1])

                elif num_groups == 1:
                    g_name = group_names_keys[0]
                    p1 = standings[g_name]["Игрок"].iloc[0]
                    p2 = standings[g_name]["Игрок"].iloc[1]
                    p3 = standings[g_name]["Игрок"].iloc[2]
                    p4 = standings[g_name]["Игрок"].iloc[3]

                    st.markdown(f"<h3>{icon_trophy} 1/2 Финала</h3>", unsafe_allow_html=True)
                    sf_pairs = [
                        ("sf_1", "1/2 #1 (1-й vs 4-й)", p1, p4),
                        ("sf_2", "1/2 #2 (2-й vs 3-й)", p2, p3)
                    ]
                    sf_winners, sf_losers = [], []
                    for m_key, title, pl1, pl2 in sf_pairs:
                        with st.expander(title, expanded=True):
                            w, l = handle_po_match(m_key, title, pl1, pl2)
                            sf_winners.append(w)
                            sf_losers.append(l)

                    st.markdown(f"<h3>{icon_trophy} Финальная стадия</h3>", unsafe_allow_html=True)
                    with st.expander("Матч за 3-е место", expanded=True):
                        handle_po_match("m3", "Матч за 3-е место", sf_losers[0], sf_losers[1])
                    with st.expander("ФИНАЛ", expanded=True):
                        handle_po_match("final", "Финальный матч", sf_winners[0], sf_winners[1])

            except Exception as e:
                st.warning("Для формирования сетки плей-офф требуется полностью завершить матчи группового этапа.")

# ==========================================
# 3. ГРУППЫ (ШАХМАТКИ С РЕЗУЛЬТАТАМИ)
# ==========================================
with tab3:
    if not st.session_state.groups:
        st.info("Проведите жеребьевку на первой вкладке.")
    else:
        st.markdown(f"<h2>{icon_chart} Турнирные таблицы групп</h2>", unsafe_allow_html=True)
        for g_name, g_players in st.session_state.groups.items():
            st.markdown(f"<h3>{g_name}</h3>", unsafe_allow_html=True)
            df_cross, _ = calculate_cross_table(g_name, g_players)
            st.dataframe(
                df_cross, 
                use_container_width=True,
                hide_index=True
            )

# ==========================================
# 4. РЕЗУЛЬТАТЫ (ПОБЕДИТЕЛИ, ПРИЗЕРЫ + РЕЙТИНГ)
# ==========================================
with tab4:
    if not st.session_state.groups:
        st.info("Данные турнира отсутствуют.")
    else:
        standings = get_current_standings()
        po_scores = st.session_state.get("playoff_scores", {})
        
        try:
            playoff_points = {p: 0 for p in st.session_state.players}

            st.markdown(f"<h2>{icon_trophy} Пьедестал почета</h2>", unsafe_allow_html=True)
            st.markdown(f"<h3>Итоги турнира</h3>", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(f"<h2>{icon_chart} Итоговый рейтинг всех участников</h2>", unsafe_allow_html=True)
            
            group_points_map = {}
            for g_name, df_g in standings.items():
                for _, row in df_g.iterrows():
                    group_points_map[row["Игрок"]] = row["Очки"]
            
            all_results = []
            for player in st.session_state.players:
                g_pts = group_points_map.get(player, 0)
                po_pts = playoff_points.get(player, 0)
                total_pts = g_pts + po_pts
                all_results.append({
                    "Игрок": player,
                    "Очки (Группа)": g_pts,
                    "Очки (Плей-офф)": po_pts,
                    "Всего очков": total_pts
                })
            
            df_final = pd.DataFrame(all_results)
            df_final = df_final.sort_values(by=["Всего очков", "Очки (Плей-офф)", "Очки (Группа)"], ascending=False)
            df_final.reset_index(drop=True, inplace=True)
            df_final.index += 1
            df_final.reset_index(inplace=True)
            df_final.rename(columns={"index": "Место"}, inplace=True)
            
            st.dataframe(
                df_final[["Место", "Игрок", "Очки (Группа)", "Очки (Плей-офф)", "Всего очков"]], 
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:
            st.info("Заполните результаты группового и финального этапов для формирования итоговой таблицы.")
