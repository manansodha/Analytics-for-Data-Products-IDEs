import pandas as pd
from scipy import stats
from collections import deque
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_tool_window_duration(csv_path, close_unmatched_at_end=False):
    """
    Analyze tool window open/close.
    """

    # Load and preprocess
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df = df.sort_values(by=['user_id', 'timestamp']).reset_index(drop=True)

    print(f'Data set\n')
    print(df.head())
    open_stack = {}
    episodes = []
    orphan_closes = 0
    unmatched_opens = 0

    # Creating open/close episodes
    for _, row in df.iterrows():
        user = row['user_id']
        event = row['event'].lower().strip()
        ts = row['timestamp']

        if user not in open_stack:
            open_stack[user] = deque()

        if 'open' in event:
            open_stack[user].append({
                'start_time': ts,
                'open_type': row.get('open_type', None)
            })

        elif 'close' in event:
            if not open_stack[user]:
                orphan_closes += 1
                continue

            open_evt = open_stack[user].pop()
            duration_ms = (ts - open_evt['start_time']).total_seconds()
            episodes.append({
                'user_id': user,
                'open_type': open_evt['open_type'],
                'start_time': open_evt['start_time'],
                'end_time': ts,
                'duration_ms': duration_ms
            })

    # Handle unmatched opens
    for user, stack in open_stack.items():
        while stack:
            unmatched_opens += 1
            open_evt = stack.pop()
            if close_unmatched_at_end:
                end_time = df['timestamp'].max()
                duration_ms = (end_time - open_evt['start_time']).total_seconds() * 1000
                episodes.append({
                    'user_id': user,
                    'open_type': open_evt['open_type'],
                    'start_time': open_evt['start_time'],
                    'end_time': end_time,
                    'duration_ms': duration_ms
                })

    episodes_df = pd.DataFrame(episodes)

    # Early exit if no matched data
    if episodes_df.empty:
        print("\nNo complete open/close episodes found.")
        print(f"• Orphan closes ignored: {orphan_closes}")
        print(f"• Unmatched opens: {unmatched_opens}")
        return episodes_df, None, None

    # Summary statistics
    summary_df = episodes_df.groupby('open_type')['duration_ms'].agg(
        count='count',
        mean_duration_ms='mean',
        median_duration_ms='median',
        std_dev_ms='std'
    ).reset_index()

# Statistical test ---
    manual = episodes_df.query("open_type == 'manual'")['duration_ms']
    auto = episodes_df.query("open_type == 'auto'")['duration_ms']
    t_test = None
    if len(manual) > 1 and len(auto) > 1:
        t_test = stats.ttest_ind(manual, auto, equal_var=False)

# Summary output
    print("\n**Tool Window Duration Summary**")
    print(summary_df.to_string(index=False, formatters={
        'mean_duration_ms': '{:,.2f}'.format,
        'median_duration_ms': '{:,.2f}'.format,
        'std_dev_ms': '{:,.2f}'.format
    }))

    print("\n**Data Quality Report**")
    print(f"Matched episodes: {len(episodes_df)}")
    print(f"Orphan closes ignored: {orphan_closes}")
    print(f"Unmatched opens: {unmatched_opens}")

    if t_test:
        print("\n**Statistical Test (Two-sample t-test)**")
        print(f"t-statistic = {t_test.statistic:.3f}")
        print(f"p-value = {t_test.pvalue:.5f}")
        alpha = 0.05
        if t_test.pvalue < alpha:
            print("Result: Significant difference (Reject H₀)")
        else:
            print("Result: No significant difference (Fail to reject H₀)")
    else:
        print("\nNot enough data for t-test (need ≥2 samples per open_type).")

# Visualization
    plt.figure(figsize=(10, 5))
    sns.boxplot(x='open_type', y='duration_ms', data=episodes_df)
    sns.swarmplot(x='open_type', y='duration_ms', data=episodes_df, color=".25", size=6)
    plt.title("Distribution of Tool Window Durations by Open Type")
    plt.ylabel("Duration (seconds)")
    plt.xlabel("Open Type")
    plt.tight_layout()
    plt.show()

    return episodes_df, summary_df, t_test


episodes_df, summary_df, t_test_result = analyze_tool_window_duration("toolwindow_data.csv")
