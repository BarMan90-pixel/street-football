import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
import json

# Настройка страницы
st.set_page_config(
    page_title="Лига уличного футбола", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# СТИЛЬНЫЙ СОВРЕМЕННЫЙ UI (Light Premium Sports)
st.markdown("""
    <style>
        /* ИМПОРТ СОВРЕМЕННЫХ ШРИФТОВ */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,700;0,900;1,900&family=Inter:wght@400;600;700&display=swap');

        /* СВЕТЛАЯ ПРЕМИАЛЬНАЯ ТЕМА */
        .stApp {
            background-color: #F8FAFC;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(255, 51, 51, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(15, 23, 42, 0.03) 0%, transparent 50%);
            color: #0F172A;
            font-family: 'Inter', sans-serif;
        }

        /* ГЛАВНЫЙ ЗАГОЛОВОК */
        h1 {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            font-size: 2.2rem !important;
            font-style: italic;
            text-transform: uppercase;
            letter-spacing: 1.5px !important;
            background: linear-gradient(135deg, #0F172A 0%, #334155 60%, #FF3333 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-top: 10px !important;
            margin-bottom: 25px !important;
        }
        
        /* ПОДЗАГОЛОВКИ */
        h2, h3, .stHeader {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            text-transform: uppercase;
            letter-spacing: 1px !important;
            color: #0F172A !important;
            font-size: 1.5rem !important;
            border-left: 4px solid #FF3333;
            padding-left: 12px;
            margin-top: 20px !important;
            margin-bottom: 15px !important;
        }

        /* ЛЕБЕЛЫ, ТЕКСТ, ЧЕКБОКСЫ */
        label, .stCheckbox label span, .stNumberInput label, .stSelectbox label, p {
            color: #334155 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        /* ПОЛЕ ВВОДА УЧАСТНИКОВ (TEXTAREA) */
        div[data-baseweb="textarea"] {
            background-color: #FFFFFF !important;
            border-radius: 12px !important;
            border: 2px solid #E2E8F0 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }
        div[data-baseweb="textarea"] textarea {
            color: #0F172A !important;
            -webkit-text-fill-color: #0F172A !important;
            background-color: #FFFFFF !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 12px !important;
        }
        div[data-baseweb="textarea"]:focus-within {
            border-color: #FF3333 !important;
            box-shadow: 0 0 0 3px rgba(255, 51, 51, 0.2) !important;
        }

        /* ЧИСЛОВЫЕ ПОЛЯ И ВВОД */
        div[data-baseweb="input"] {
            background-color: #FFFFFF !important;
            border-radius: 10px !important;
            border: 1px solid #CBD5E1 !important;
        }
        div[data-baseweb="input"] input {
            color: #0F172A !important;
            font-weight: 700 !important;
        }

        /* КАРТОЧКИ УЧАСТНИКОВ И МАТЧЕЙ (EXPANDERS) */
        div[data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            margin-bottom: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05) !important;
            overflow: hidden;
        }
        
        div[data-testid="stExpander"] * {
            color: #0F172A !important;
        }

        /* СОВРЕМЕННЫЕ КНОПКИ C ЯРКИМ АКЦЕНТОМ */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            height: 3.4em;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            font-size: 16px !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            background: linear-gradient(135deg, #FF3333 0%, #DC2626 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(255, 51, 51, 0.3);
            transition: all 0.2s ease-in-out;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 51, 51, 0.45);
            background: linear-gradient(135deg, #FF4D4D 0%, #B91C1C 100%) !important;
        }

        /* ТАБЛИЦЫ */
        div[data-testid="stDataFrame"] {
            background-color: #FFFFFF !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        div[data-testid="stDataFrame"] * {
            color: #0F172A !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
        }

        /* ВКЛАДКИ (TABS) */
        button[data-baseweb="tab"] {
            color: #64748B !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 12px 20px !important;
        }
        button[aria-selected="true"] {
            color: #FF3333 !important;
            border-bottom: 3px solid #FF3333 !important;
        }

        /* ПОДСКАЗКИ */
        .stCaption {
            color: #64748B !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }

        /* РАЗДЕЛИТЕЛИ */
        hr {
            border-color: #E2E8F0 !important;
            margin: 25px 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ ЛИГА УЛИЧНОГО ФУТБОЛА")

if "players" not in st.session_state:
    st.session_state.players = []
if "groups" not in st.session_state:
    st.session_state.groups = {}
if "group_scores" not in st.session_state:
    st.session_state.group_scores = {}

tab1, tab2, tab3 = st.tabs(["🎲 Жеребьевка", "📊 Групповой этап", "🏆 Плей-офф"])

# ==========================================
# 1. ЖЕРЕБЬЕВКА И DRAG-AND-DROP ГРУППЫ
# ==========================================
with tab1:
    st.header("Список участников")
    default_text = "\n".join([f"Игрок {i}" for i in range(1, 17)])
    raw_players = st.text_area(
        "Введите ФИО игроков (по одного на строку):", 
        value=default_text, 
        height=180
    )
    
    if st.button("🎲 ПРОВЕСТИ ЖЕРЕБЬЕВКУ"):
        players_list = [p.strip() for p in raw_players.split("\n") if p.strip()]
        if len(players_list) < 4:
            st.error("Нужно минимум 4 игрока!")
        else:
            st.session_state.players = players_list.copy()
            random.shuffle(players_list)
            group_names = ["Группа А", "Группа Б", "Группа В", "Группа Г"]
            st.session_state.groups = {g: [] for g in group_names}
            
            for i, p in enumerate(players_list):
                g_idx = i % 4
                st.session_state.groups[group_names[g_idx]].append(p)
                
            st.session_state.group_scores = {}
            st.success("Игроки распределены по группам!")

    if st.session_state.groups:
        st.markdown("---")
        st.subheader("🖐 Интерактивное распределение")
        st.caption("Зажмите игрока мышью и перетащите в нужную группу:")

        # HTML/JS Drag-and-Drop (Светлый стиль)
        groups_json = json.dumps(st.session_state.groups, ensure_ascii=False)
        
        dnd_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&family=Inter:wght@600;700&display=swap');
                body {{
                    font-family: 'Inter', sans-serif;
                    background-color: transparent;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 14px;
                }}
                .group-box {{
                    background: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 14px;
                    padding: 14px;
                    min-height: 170px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                    transition: border-color 0.2s;
                }}
                .group-title {{
                    font-family: 'Montserrat', sans-serif;
                    font-size: 16px;
                    font-weight: 800;
                    color: #FF3333;
                    margin-bottom: 10px;
                    border-bottom: 2px solid #F1F5F9;
                    padding-bottom: 6px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .player-card {{
                    background-color: #F8FAFC;
                    color: #0F172A !important;
                    font-weight: 700;
                    font-size: 14px;
                    padding: 10px 14px;
                    margin-bottom: 8px;
                    border-radius: 10px;
                    border: 1px solid #E2E8F0;
                    cursor: grab;
                    user-select: none;
                    transition: all 0.2s ease;
                }}
                .player-card:hover {{
                    background-color: #FFF5F5;
                    border-color: #FF3333;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(255, 51, 51, 0.15);
                }}
                .player-card:active {{
                    cursor: grabbing;
                    background-color: #FF3333;
                    color: #FFFFFF !important;
                }}
                .drag-over {{
                    background-color: #FFF0F0 !important;
                    border: 2px dashed #FF3333 !important;
                }}
            </style>
        </head>
        <body>
            <div class="container" id="board"></div>

            <script>
                let groupsData = {groups_json};

                function renderBoard() {{
                    const board = document.getElementById('board');
                    board.innerHTML = '';

                    for (let gName in groupsData) {{
                        let box = document.createElement('div');
                        box.className = 'group-box';
                        box.dataset.group = gName;
                        box.ondragover = allowDrop;
                        box.ondragleave = removeDragOver;
                        box.ondrop = drop;

                        let title = document.createElement('div');
                        title.className = 'group-title';
                        title.innerText = gName + ' (' + groupsData[gName].length + ')';
                        box.appendChild(title);

                        groupsData[gName].forEach((player, idx) => {{
                            let card = document.createElement('div');
                            card.className = 'player-card';
                            card.draggable = true;
                            card.innerText = (idx + 1) + '. ' + player;
                            card.dataset.player = player;
                            card.dataset.fromGroup = gName;
                            card.ondragstart = drag;
                            box.appendChild(card);
                        }});

                        board.appendChild(box);
                    }}
                }}

                function allowDrop(ev) {{
                    ev.preventDefault();
                    ev.currentTarget.classList.add('drag-over');
                }}

                function removeDragOver(ev) {{
                    ev.currentTarget.classList.remove('drag-over');
                }}

                function drag(ev) {{
                    ev.dataTransfer.setData("player", ev.target.dataset.player);
                    ev.dataTransfer.setData("fromGroup", ev.target.dataset.fromGroup);
                }}

                function drop(ev) {{
                    ev.preventDefault();
                    let box = ev.currentTarget;
                    box.classList.remove('drag-over');
                    
                    let targetGroup = box.dataset.group;
                    let player = ev.dataTransfer.getData("player");
                    let fromGroup = ev.dataTransfer.getData("fromGroup");

                    if (fromGroup && targetGroup && fromGroup !== targetGroup) {{
                        let idx = groupsData[fromGroup].indexOf(player);
                        if (idx > -1) {{
                            groupsData[fromGroup].splice(idx, 1);
                            groupsData[targetGroup].push(player);
                            renderBoard();
                            
                            window.parent.postMessage({{
                                type: 'streamlit:setComponentValue',
                                value: JSON.stringify(groupsData)
                            }}, '*');
                        }}
                    }}
                }}

                renderBoard();
            </script>
        </body>
        </html>
        """
        
        updated_groups_str = components.html(dnd_html, height=450)
        
        if updated_groups_str and isinstance(updated_groups_str, str):
            try:
                new_groups = json.loads(updated_groups_str)
                if new_groups != st.session_state.groups:
                    st.session_state.groups = new_groups
                    st.rerun()
            except:
                pass

        st.markdown("---")
        st.subheader("Состав групп (Итоговый)")
        for g_name, g_players in st.session_state.groups.items():
            with st.expander(f"📌 {g_name} ({len(g_players)} чел.)", expanded=True):
                for idx, pl in enumerate(g_players, 1):
                    st.write(f"**№{idx}.** <span style='color:#0F172A;'>{pl}</span>", unsafe_allow_html=True)

# Вспомогательная функция построения ШАХМАТКИ
def calculate_cross_table(g_name, players):
    n = len(players)
    stats = {p: {"И": 0, "В": 0, "Н": 0, "П": 0, "МЗ": 0, "МП": 0, "Очки": 0} for p in players}
    pair_res = {p1: {p2: "—" for p2 in players} for p1 in players}
    
    for p in players:
        pair_res[p][p] = "❌"
        
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = players[i], players[j]
            key = f"{g_name}_{p1}_vs_{p2}"
            if key in st.session_state.group_scores:
                data = st.session_state.group_scores[key]
                s1, s2 = data.get("s1", 0), data.get("s2", 0)
                panna1, panna2 = data.get("panna1", False), data.get("panna2", False)
                
                txt1 = f"{s1}:{s2}" + (" 🔴" if panna1 else "")
                txt2 = f"{s2}:{s1}" + (" 🔴" if panna2 else "")
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

# ==========================================
# 2. ГРУППОВОЙ ЭТАП
# ==========================================
with tab2:
    if not st.session_state.groups:
        st.info("Проведите жеребьевку на первой вкладке.")
    else:
        standings_dict = {}
        for g_name, g_players in st.session_state.groups.items():
            st.subheader(f"📌 {g_name}")
            
            num_legend = ", ".join([f"№{i+1} — {p}" for i, p in enumerate(g_players)])
            st.caption(f"Участники: {num_legend}")
            
            with st.expander("📝 Ввод результатов матчей", expanded=False):
                for i in range(len(g_players)):
                    for j in range(i + 1, len(g_players)):
                        p1, p2 = g_players[i], g_players[j]
                        key = f"{g_name}_{p1}_vs_{p2}"
                        
                        st.markdown(f"**№{i+1} <span style='color:#0F172A;'>{p1}</span>** vs **№{j+1} <span style='color:#0F172A;'>{p2}</span>**", unsafe_allow_html=True)
                        c1, c2 = st.columns(2)
                        s1 = c1.number_input(f"Голы {p1}", min_value=0, value=0, key=f"{key}_s1")
                        s2 = c2.number_input(f"Голы {p2}", min_value=0, value=0, key=f"{key}_s2")
                        
                        cp1, cp2 = st.columns(2)
                        panna1 = cp1.checkbox(f"🔴 ПАННА от {p1}", key=f"{key}_panna1")
                        panna2 = cp2.checkbox(f"🔴 ПАННА от {p2}", key=f"{key}_panna2")
                        
                        st.session_state.group_scores[key] = {
                            "s1": s1, "s2": s2, 
                            "panna1": panna1, "panna2": panna2
                        }
                        st.markdown("---")

            df_cross, df_standing = calculate_cross_table(g_name, g_players)
            st.dataframe(
                df_cross, 
                use_container_width=True,
                hide_index=True
            )
            standings_dict[g_name] = df_standing

        st.session_state.standings = standings_dict

# ==========================================
# 3. ПЛЕЙ-ОФФ И ИТОГОВЫЙ РЕЙТИНГ
# ==========================================
with tab3:
    if "standings" not in st.session_state or len(st.session_state.standings) < 4:
        st.info("Заполните группы для формирования плей-офф.")
    else:
        try:
            playoff_points = {p: 0 for p in st.session_state.players}
            
            p1A = st.session_state.standings["Группа А"]["Игрок"].iloc[0]
            p2A = st.session_state.standings["Группа А"]["Игрок"].iloc[1]
            p1B = st.session_state.standings["Группа Б"]["Игрок"].iloc[0]
            p2B = st.session_state.standings["Группа Б"]["Игрок"].iloc[1]
            p1V = st.session_state.standings["Группа В"]["Игрок"].iloc[0]
            p2V = st.session_state.standings["Группа В"]["Игрок"].iloc[1]
            p1G = st.session_state.standings["Группа Г"]["Игрок"].iloc[0]
            p2G = st.session_state.standings["Группа Г"]["Игрок"].iloc[1]
            
            st.subheader("🥊 1/4 Финала")
            qf_pairs = [
                ("1/4 #1 (1А vs 2Г)", p1A, p2G),
                ("1/4 #2 (1Б vs 2В)", p1B, p2V),
                ("1/4 #3 (1В vs 2Б)", p1V, p2B),
                ("1/4 #4 (1Г vs 2А)", p1G, p2A),
            ]
            
            qf_winners, qf_losers = [], []
            for idx, (title, player1, player2) in enumerate(qf_pairs):
                with st.expander(title, expanded=True):
                    st.markdown(f"**<span style='color:#0F172A;'>{player1}</span>** — **<span style='color:#0F172A;'>{player2}</span>**", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    sc1 = c1.number_input("Счет 1", min_value=0, key=f"qf_{idx}_1")
                    sc2 = c2.number_input("Счет 2", min_value=0, key=f"qf_{idx}_2")
                    p1_panna = c1.checkbox("Панна", key=f"qf_panna_{idx}_1")
                    p2_panna = c2.checkbox("Панна", key=f"qf_panna_{idx}_2")
                    
                    if p1_panna:
                        qf_winners.append(player1)
                        qf_losers.append(player2)
                        playoff_points[player1] += 4
                    elif p2_panna:
                        qf_winners.append(player2)
                        qf_losers.append(player1)
                        playoff_points[player2] += 4
                    elif sc1 > sc2:
                        qf_winners.append(player1)
                        qf_losers.append(player2)
                        playoff_points[player1] += 3
                    else:
                        qf_winners.append(player2)
                        qf_losers.append(player1)
                        playoff_points[player2] += 3

            st.subheader("🔥 1/2 Финала")
            sf_pairs = [
                ("1/2 #1", qf_winners[0], qf_winners[1]),
                ("1/2 #2", qf_winners[2], qf_winners[3])
            ]
            sf_winners, sf_losers = [], []
            for idx, (title, player1, player2) in enumerate(sf_pairs):
                with st.expander(f"{title}: {player1} vs {player2}", expanded=True):
                    c1, c2 = st.columns(2)
                    sc1 = c1.number_input("Счет 1", min_value=0, key=f"sf_{idx}_1")
                    sc2 = c2.number_input("Счет 2", min_value=0, key=f"sf_{idx}_2")
                    p1_panna = c1.checkbox("Панна", key=f"sf_panna_{idx}_1")
                    p2_panna = c2.checkbox("Панна", key=f"sf_panna_{idx}_2")
                    
                    if p1_panna:
                        sf_winners.append(player1)
                        sf_losers.append(player2)
                        playoff_points[player1] += 4
                    elif p2_panna:
                        sf_winners.append(player2)
                        sf_losers.append(player1)
                        playoff_points[player2] += 4
                    elif sc1 > sc2:
                        sf_winners.append(player1)
                        sf_losers.append(player2)
                        playoff_points[player1] += 3
                    else:
                        sf_winners.append(player2)
                        sf_losers.append(player1)
                        playoff_points[player2] += 3

            st.subheader("🏆 Финальная стадия")
            with st.expander("🥉 Матч за 3-е место", expanded=True):
                st.markdown(f"**<span style='color:#0F172A;'>{sf_losers[0]}</span>** vs **<span style='color:#0F172A;'>{sf_losers[1]}</span>**", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                sc_m3_1 = c1.number_input("Счет 1", min_value=0, key="m3_1")
                sc_m3_2 = c2.number_input("Счет 2", min_value=0, key="m3_2")
                p1_panna = c1.checkbox("Панна", key="m3_panna_1")
                p2_panna = c2.checkbox("Панна", key="m3_panna_2")
                
                if p1_panna:
                    third_place, fourth_place = sf_losers[0], sf_losers[1]
                    playoff_points[sf_losers[0]] += 4
                elif p2_panna:
                    third_place, fourth_place = sf_losers[1], sf_losers[0]
                    playoff_points[sf_losers[1]] += 4
                elif sc_m3_1 > sc_m3_2:
                    third_place, fourth_place = sf_losers[0], sf_losers[1]
                    playoff_points[sf_losers[0]] += 3
                else:
                    third_place, fourth_place = sf_losers[1], sf_losers[0]
                    playoff_points[sf_losers[1]] += 3
                
            with st.expander("👑 ФИНАЛ", expanded=True):
                st.markdown(f"**<span style='color:#0F172A;'>{sf_winners[0]}</span>** vs **<span style='color:#0F172A;'>{sf_winners[1]}</span>**", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                sc_f_1 = c1.number_input("Счет 1", min_value=0, key="f_1")
                sc_f_2 = c2.number_input("Счет 2", min_value=0, key="f_2")
                p1_panna = c1.checkbox("Панна", key="f_panna_1")
                p2_panna = c2.checkbox("Панна", key="f_panna_2")
                
                if p1_panna:
                    first_place, second_place = sf_winners[0], sf_winners[1]
                    playoff_points[sf_winners[0]] += 4
                elif p2_panna:
                    first_place, second_place = sf_winners[1], sf_winners[0]
                    playoff_points[sf_winners[1]] += 4
                elif sc_f_1 > sc_f_2:
                    first_place, second_place = sf_winners[0], sf_winners[1]
                    playoff_points[sf_winners[0]] += 3
                else:
                    first_place, second_place = sf_winners[1], sf_winners[0]
                    playoff_points[sf_winners[1]] += 3

            st.markdown("---")
            st.markdown(f"### 🥇 1 МЕСТО: <span style='color:#FF3333;'>{first_place}</span>", unsafe_allow_html=True)
            st.markdown(f"### 🥈 2 МЕСТО: <span style='color:#0F172A;'>{second_place}</span>", unsafe_allow_html=True)
            st.markdown(f"### 🥉 3 МЕСТО: <span style='color:#0F172A;'>{third_place}</span>", unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("📊 Итоговый рейтинг всех участников")
            
            group_points_map = {}
            for g_name, df_g in st.session_state.standings.items():
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

        except Exception:
            st.warning("Сначала введите результаты группового этапа.")