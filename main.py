import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


#  Setup and Load Data

sns.set(style='whitegrid')

# Create folder for saving all images
output_dir = "player_stats"
os.makedirs(output_dir, exist_ok=True)

# Load dataset
df = pd.read_csv("IPL dataset final.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Display dataset info
print(" First 5 Rows:")
print(df.head(), "\n")

print(" Dataset Info:")
print(df.info(), "\n")

print(" Statistical Summary:")
print(df.describe(), "\n")

print(" Columns Available:")
print(df.columns, "\n")

# Drop missing values
df.dropna(inplace=True)


#  Top 10 Run Scorers

possible_run_cols = ['Runs', 'Total_Runs', 'TRuns']
run_col = next((col for col in possible_run_cols if col in df.columns), None)
if run_col is None:
    raise ValueError(" No valid run column found in the dataset!")

print(f" Using '{run_col}' as the run column.\n")

top_players = df.nlargest(10, run_col)

plt.figure(figsize=(12, 6))
bars = plt.bar(top_players['Player'], top_players[run_col],
               color='orange', edgecolor='black')
plt.xlabel('Player', fontsize=12)
plt.ylabel('Total Runs', fontsize=12)
plt.title(' Top 10 Run Scorers in IPL', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             int(bar.get_height()), ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(f"{output_dir}/top_10_run_scorers.png")
plt.show()


#  Top 10 Wicket Takers

possible_wicket_cols = ['B_Wkts', 'Wkts', 'Wickets', 'B_TWkts']
wicket_col = next((col for col in possible_wicket_cols if col in df.columns), None)
if wicket_col is None:
    raise ValueError(" No valid wickets column found in the dataset!")

print(f" Using '{wicket_col}' as the wickets column.\n")

top_wicket_takers = df.nlargest(10, wicket_col)[['Player', wicket_col]]

plt.figure(figsize=(12, 6))
bars = plt.bar(top_wicket_takers['Player'], top_wicket_takers[wicket_col],
               color='mediumseagreen', edgecolor='black')
plt.xlabel('Player', fontsize=12)
plt.ylabel('Wickets Taken', fontsize=12)
plt.title(' Top 10 Wicket-Takers in IPL', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             int(bar.get_height()), ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(f"{output_dir}/top_10_wicket_takers.png")
plt.show()


#  Pie Chart — Players per Team

team_counts = df['TEAM'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(team_counts, labels=team_counts.index, autopct='%1.1f%%',
        startangle=140, colors=plt.cm.Set3.colors)
plt.title('🏆 Distribution of Players by Team', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{output_dir}/players_per_team.png")
plt.show()


#  Player-Specific Stats (Bar + Pie Chart — Showing Numbers)

print("\n Sample Player Names:", df['Player'].unique()[:10])

player_name = input("\nEnter player name: ").strip()
player_data = df[df['Player'].str.lower() == player_name.lower()]

if not player_data.empty:
    player_row = player_data.iloc[0]

    runs_val = float(player_row.get(run_col, 0))
    wickets_val = float(player_row.get(wicket_col, 0))
    sr_val = float(player_row.get('SR', 0))
    avg_val = float(str(player_row.get('Avg', 0)).replace('*', '').replace('–', '0'))

    # Bar Chart
    plt.figure(figsize=(6, 4))
    plt.bar([player_name.title()], [runs_val], color='dodgerblue', edgecolor='black')
    plt.xlabel('Player', fontsize=12)
    plt.ylabel('Total Runs', fontsize=12)
    plt.title(f' Total Runs Scored by {player_name.title()}: {runs_val}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{player_name.title()}_runs.png")
    plt.show()

    # Pie Chart (Numbers instead of %)
    labels = ['Runs', 'Wickets', 'Strike Rate', 'Average']
    values = [runs_val, wickets_val, sr_val, avg_val]

    total = sum(values)
    if total > 0:
        plt.figure(figsize=(7, 7))
        def absolute_value(val):
            total = sum(values)
            val_num = int(round(val * total / 100))
            return f"{val_num}"
        plt.pie(values, labels=labels, autopct=absolute_value,
                startangle=90, colors=plt.cm.Paired.colors,
                shadow=True, explode=(0.05, 0.05, 0.05, 0.05))
        plt.title(f" Performance Breakdown: {player_row['Player']}",
                  fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{player_row['Player'].title()}_pie_stats.png")
        plt.show()
    else:
        print(f" No valid numeric data for {player_name}")
else:
    print(f" No data found for player: {player_name}")


#  Top 10 Most Expensive (Sold) Players

def convert_price(price):
    if isinstance(price, str):
        price = price.strip().lower().replace('₹', '').replace(',', '')
        if 'cr' in price:
            return float(price.replace('cr', '').strip()) * 100
        elif 'lakh' in price:
            return float(price.replace('lakh', '').strip())
        else:
            try:
                return float(price)
            except:
                return 0
    return float(price)

if 'SOLD_PRICE' in df.columns:
    df['SOLD_PRICE_NUM'] = df['SOLD_PRICE'].apply(convert_price)

    top_sold_players = df.nlargest(10, 'SOLD_PRICE_NUM')[['Player', 'SOLD_PRICE', 'TEAM', 'SOLD_PRICE_NUM']]

    print("\n Top 10 Most Expensive Players:")
    print(top_sold_players[['Player', 'TEAM', 'SOLD_PRICE']], "\n")

    plt.figure(figsize=(12, 6))
    bars = plt.bar(top_sold_players['Player'], top_sold_players['SOLD_PRICE_NUM'],
                   color='plum', edgecolor='black')
    plt.xlabel('Player', fontsize=12)
    plt.ylabel('Sold Price (in Lakhs ₹)', fontsize=12)
    plt.title(' Top 10 Most Expensive Players in IPL Auction', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for bar, price in zip(bars, top_sold_players['SOLD_PRICE']):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                 f"{price}", ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/top_10_sold_players.png")
    plt.show()
else:
    print("⚠️ SOLD_PRICE column not found in the dataset!")

print(f"\n✅ Analysis complete! All charts saved inside the '{output_dir}' folder.")
