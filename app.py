import pandas as pd

def get_recent_searches():
    try:
        df = pd.read_csv('weather_log.csv')
        return df.tail(5).iloc[::-1].to_dict('records')
    except:
        return []

def update_search_history(history_frame):
    # Clear existing history
    for widget in history_frame.winfo_children():
        widget.destroy()
    
    # Add title
    tk.Label(history_frame, text="Recent Searches", class_="history-title").pack(anchor="w")
    
    # Add recent searches
    searches = get_recent_searches()
    for search in searches:
        history_text = f"{search['location']} - {search['timestamp']}"
        tk.Label(history_frame, text=history_text, class_="history-item").pack(anchor="w")

# In your main GUI setup, add:
history_frame = tk.Frame(root, class_="search-history")
history_frame.pack(padx=20, pady=10, fill="x")
update_search_history(history_frame)

# Add this line after successful weather search:
update_search_history(history_frame)
