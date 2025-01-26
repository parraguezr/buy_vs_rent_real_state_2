import matplotlib.pyplot as plt
import pandas as pd

def plot_annual_outflow(rent_df, buy_df):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(rent_df["year"], rent_df["total_rent_cost"], label="Rent Annual Outflow", marker='o')
    ax.plot(buy_df["year"], buy_df["total_outflow"], label="Buy Annual Outflow", marker='o')
    ax.set_xlabel("Year")
    ax.set_ylabel("Cost (DKK)")
    ax.set_title("Annual Outflow: Renting vs. Buying")
    ax.legend()
    ax.grid(True)
    return fig

def plot_investment_growth(rent_invest_df):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(rent_invest_df["year"], rent_invest_df["investment_end"], 
            label="Rent Investment Balance", marker='o', color='orange')
    ax.set_xlabel("Year")
    ax.set_ylabel("DKK")
    ax.set_title("Investment Growth When Renting")
    ax.legend()
    ax.grid(True)
    return fig

def plot_net_equity_over_time(buy_df):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(buy_df["year"], buy_df["net_equity_end"], label="Home Equity (Buy)", marker='o', color='green')
    ax.set_xlabel("Year")
    ax.set_ylabel("DKK")
    ax.set_title("Net Equity Over Time (Buying)")
    ax.legend()
    ax.grid(True)
    return fig

def plot_buy_cost_breakdown(buy_df):
    """
    Stacked bar chart for various cost components in the buy scenario.
    """
    cost_components_buy = pd.DataFrame({
        'year': buy_df['year'],
        'Principal': buy_df['principal_paid'],
        'Interest': buy_df['interest_paid'],
        'Property Tax': buy_df['property_value_tax'],
        'Land Tax': buy_df['land_tax'],
        'Insurance': buy_df['insurance'],
        'Maintenance': buy_df['maintenance'],
        'Renovations': buy_df['renovations'],
        'Community Ownership Cost': buy_df['community_ownership_cost'],
    })
    cost_components_buy.set_index('year', inplace=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    cost_components_buy.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Buy Scenario: Yearly Cost Breakdown (Stacked)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cost (DKK)")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
    ax.grid(True)
    return fig

def plot_rent_cost_breakdown(rent_df):
    """
    Stacked bar chart for rent scenario costs.
    """
    cost_components_rent = pd.DataFrame({
        'year': rent_df['year'],
        'Rent': rent_df['annual_rent'],
        'Renter Insurance': rent_df['renters_insurance']
    })
    cost_components_rent.set_index('year', inplace=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    cost_components_rent.plot(kind='bar', stacked=True, color=['#1f77b4', '#ff7f0e'], ax=ax)
    ax.set_title("Rent Scenario: Yearly Cost Breakdown (Stacked)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cost (DKK)")
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    ax.grid(True)
    return fig

def plot_mortgage_vs_value(buy_df):
    """
    Mortgage balance vs. house value over time.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(buy_df["year"], buy_df["mortgage_balance_end"], label="Mortgage Balance", marker='o', color='red')
    ax.plot(buy_df["year"], buy_df["house_value_end"], label="House Value", marker='o', color='green')
    ax.set_title("Mortgage Balance vs. House Value Over Time (Buy)")
    ax.set_xlabel("Year")
    ax.set_ylabel("DKK")
    ax.grid(True)
    ax.legend()
    return fig

def plot_net_worth_difference(buy_df, rent_invest_df):
    """
    Difference in net worth each year = buy_net_equity - rent_invest_balance.
    """
    diff_df = pd.DataFrame({
        'year': buy_df['year'],
        'net_equity_buy': buy_df['net_equity_end'],
        'net_worth_rent': rent_invest_df['investment_end']
    })
    diff_df['difference'] = diff_df['net_equity_buy'] - diff_df['net_worth_rent']

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(diff_df["year"], diff_df["difference"], marker='o', color='purple', 
            label="Net Worth Difference (Buy - Rent)")
    ax.set_title("Difference in Net Worth Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("DKK")
    ax.grid(True)
    ax.axhline(y=0, color='black', linestyle='--')
    ax.legend()
    return fig

def plot_cumulative_outflow(rent_df, buy_df):
    """
    Cumulative outflow comparison between rent and buy.
    """
    rent_df['cumulative_rent_outflow'] = rent_df['total_rent_cost'].cumsum()
    buy_df['cumulative_buy_outflow'] = buy_df['total_outflow'].cumsum()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(rent_df["year"], rent_df["cumulative_rent_outflow"], 
            label="Cumulative Rent Outflow", marker='o')
    ax.plot(buy_df["year"], buy_df["cumulative_buy_outflow"], 
            label="Cumulative Buy Outflow", marker='o')
    ax.set_title("Cumulative Outflow: Renting vs. Buying")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Outflow (DKK)")
    ax.grid(True)
    ax.legend()
    return fig
