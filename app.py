import streamlit as st

# --- CORE LOGIC (k-Queens Solver, unchanged) ---
def solve_k_queens(n, k):
    solutions = []
    board = [-1] * n
    def is_safe(row, col):
        for prev_row in range(row):
            if board[prev_row] != -1 and (board[prev_row] == col or abs(row - prev_row) == abs(col - board[prev_row])):
                return False
        return True
    def backtrack(row, queens_placed):
        if queens_placed == k:
            solution_coords = [(r, c) for r, c in enumerate(board) if c != -1]
            solutions.append(solution_coords)
            return
        if row == n:
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                backtrack(row + 1, queens_placed + 1)
                board[row] = -1
        backtrack(row + 1, queens_placed)
    backtrack(0, 0)
    return solutions

# --- DYNAMIC UI STYLING & VISUALIZATION ---

def get_themed_css(theme):
    """ Returns a string of CSS with theme-specific colors. """
    if theme == 'dark':
        # Dark Theme Colors
        bg_color, text_color, primary_color, accent_color, card_bg, border_color = (
            '#0E1117', '#FAFAFA', '#FF4B4B', '#E03C3C', '#262730', '#444'
        )
    else:
        # Light Theme Colors
        bg_color, text_color, primary_color, accent_color, card_bg, border_color = (
            '#FFFFFF', '#333333', '#FF4B4B', '#D03030', '#F0F2F6', '#DDD'
        )
        
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        
        :root {{
            --bg-color: {bg_color};
            --text-color: {text_color};
            --primary-color: {primary_color};
            --accent-color: {accent_color};
            --card-bg: {card_bg};
            --border-color: {border_color};
        }}

        body, .stApp {{
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Poppins', sans-serif;
        }}
        h1 {{
            color: var(--text-color);
            font-weight: 600;
        }}

        /* Main control grid container */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stHorizontalBlock"] {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        /* Input widgets */
        .stNumberInput > div > div > input {{
            background-color: var(--bg-color);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}
        .stNumberInput > div > div > input:focus {{
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px var(--accent-color)40;
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: var(--primary-color);
            color: #FFFFFF;
            border-radius: 8px;
            border: none;
            font-weight: bold;
            padding: 10px 20px;
            width: 100%;
            transition: background-color 0.2s, transform 0.1s;
        }}
        .stButton > button:hover {{
            background-color: var(--accent-color);
            transform: scale(1.02);
        }}
        .stButton > button:active {{
            transform: scale(0.98);
        }}

        /* Status & Navigation */
        .status-text, .nav-text {{
            background-color: var(--card-bg);
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            color: var(--text-color);
            font-weight: bold;
            border: 1px solid var(--border-color);
        }}

        /* Chessboard styling */
        .chessboard {{
            border: 3px solid var(--primary-color);
            border-radius: 8px;
            padding: 5px;
            display: grid;
            box-shadow: 0px 0px 15px var(--primary-color)50;
        }}
        .square {{
            width: 55px;
            height: 55px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 38px;
        }}
        .dark {{ background-color: #769656; }}
        .light {{ background-color: #eeeed2; }}
    </style>
    """

def visualize_board_html(n, solution_coords):
    """Generates an HTML string for the chessboard visualization."""
    board_html = f'<div class="chessboard" style="grid-template-columns: repeat({n}, 1fr);">'
    for row in range(n):
        for col in range(n):
            square_color = "dark" if (row + col) % 2 == 1 else "light"
            queen_symbol = "👑" if (row, col) in solution_coords else ""
            board_html += f'<div class="square {square_color}">{queen_symbol}</div>'
    board_html += "</div>"
    return board_html

# --- STREAMLIT APP LAYOUT ---

st.set_page_config(layout="centered", page_title="N-Queens Visualizer")

# --- Theme Switcher in Sidebar ---
st.sidebar.header("Settings")
theme_mode = st.sidebar.toggle("🌙 Dark Mode", value=True)
theme = 'dark' if theme_mode else 'light'

# Inject the dynamic CSS
st.markdown(get_themed_css(theme), unsafe_allow_html=True)

st.title("N-Queens Visualizer")

# --- Session State Initialization ---
if 'solutions' not in st.session_state:
    st.session_state.solutions = []
if 'current_solution_index' not in st.session_state:
    st.session_state.current_solution_index = 0

# --- Controls Grid ---
# We use st.columns within a container that our CSS targets
# to create the seamless grid effect.
grid = st.columns([2, 2, 3])
with grid[0]:
    st.markdown("**Board size**")
    n = st.number_input("Board (n)", min_value=1, max_value=12, value=4, label_visibility="collapsed")
with grid[1]:
    st.markdown("**Number of Queens (k)**")
    k = st.number_input("Queens (k)", min_value=1, max_value=n, value=4, label_visibility="collapsed")
with grid[2]:
    if st.button("Find Solutions"):
        with st.spinner(f"Searching for solutions..."):
            st.session_state.solutions = solve_k_queens(n, k)
        st.session_state.current_solution_index = 0
        st.rerun()

# --- Display Results ---
if st.session_state.solutions:
    num_solutions = len(st.session_state.solutions)
    st.markdown(f'<p class="status-text">Found {num_solutions} solution(s)</p>', unsafe_allow_html=True)
    
    nav_cols = st.columns([1, 2, 1])
    if nav_cols[0].button("⬅️ Prev"):
        if st.session_state.current_solution_index > 0:
            st.session_state.current_solution_index -= 1
            st.rerun()
    if nav_cols[2].button("Next ➡️"):
        if st.session_state.current_solution_index < num_solutions - 1:
            st.session_state.current_solution_index += 1
            st.rerun()
    
    nav_cols[1].markdown(
        f'<p class="nav-text">Solution {st.session_state.current_solution_index + 1} / {num_solutions}</p>',
        unsafe_allow_html=True
    )
    
    current_solution = st.session_state.solutions[st.session_state.current_solution_index]
    board_html = visualize_board_html(n, current_solution)
    st.markdown(f'<div style="display: flex; justify-content: center; margin-top: 20px;">{board_html}</div>', unsafe_allow_html=True)

else:

    st.info("Set the board size and number of queens, then click 'Find Solutions'.")
