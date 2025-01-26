import streamlit as st
import pandas as pd

# We import our calculations and plots modules
from calculations import (
    calculate_rent_scenario,
    calculate_buy_scenario,
    calculate_rent_investment_scenario,
    compare_scenarios
)
from plots import (
    plot_annual_outflow,
    plot_investment_growth,
    plot_net_equity_over_time,
    plot_buy_cost_breakdown,
    plot_rent_cost_breakdown,
    plot_mortgage_vs_value,
    plot_net_worth_difference,
    plot_cumulative_outflow,
)


st.set_page_config(
    page_title="Rent vs Buy Comparison",
    layout="centered",
    initial_sidebar_state="expanded"
)

def main():
    st.title("Should You Rent or Buy? Financial Calculator")
    st.markdown("""
    This calculator helps you make an informed decision between renting and buying a home 
    by comparing the long-term financial implications.  
    **Note**: All figures are estimates and not guaranteed results. 
    Consult your advisor for personalized advice.
    """)

    #--- TABS for input and results
    tab_input, tab_results = st.tabs(["📝 Input Parameters", "📊 Analysis Results"])

    with tab_input:
        st.header("Input Parameters")
        st.info("Adjust the parameters below to match your situation.")

        with st.expander("🌍 General Assumptions", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                analysis_years = st.number_input("Analysis Term (years)", min_value=1, max_value=50, value=30)
                inflation_rate = st.slider("Annual Inflation Rate (%)", 0.0, 10.0, 2.5, 0.1) / 100
                savings_interest_rate = st.slider("Savings/Investment Rate (%)", 0.0, 10.0, 3.5, 0.1) / 100
            with col2:
                house_appreciation_rate = st.slider("House Appreciation Rate (%)", 0.0, 10.0, 2.5, 0.1) / 100
                rent_increase_rate = st.slider("Rent Increase Rate (%)", 0.0, 10.0, 1.5, 0.1) / 100

        with st.expander("🏢 Rent Scenario", expanded=True):
            current_monthly_rent = st.number_input("Current Monthly Rent (DKK)", value=17654, step=1000)
            annual_renters_insurance = st.number_input("Annual Renter's Insurance (DKK)", value=0, step=500)

        with st.expander("🏠 Buy Scenario", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                cash_price = st.number_input("Purchase Price (DKK)", value=6200000, step=100000)
                downpayment = st.number_input("Downpayment (DKK)", value=1200000, step=100000)
                closing_costs = st.number_input("Closing Costs (DKK)", value=200000, step=50000)
            with col2:
                mortgage_rate = st.slider("Mortgage Interest Rate (%)", 0.0, 15.0, 5.03, 0.01) / 100
                mortgage_term_years = st.number_input("Mortgage Term (years)", value=30)
                interest_deduction_rate = st.slider("Mortgage Interest Deduction Rate (%)", 0.0, 50.0, 33.0, 1.0) / 100

        with st.expander("💰 Property Taxes", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                property_value_tax_below_9200k = st.number_input("Property Value Tax Rate (<= 9,200,000) (%)",
                                                                 value=0.51, step=0.01, format="%.2f") / 100
                property_value_tax_above_9200k = st.number_input("Property Value Tax Rate (> 9,200,000) (%)",
                                                                 value=1.40, step=0.01, format="%.2f") / 100
                land_tax_rate = st.number_input("Land Tax Rate (%)", value=0.51, step=0.01, format="%.2f") / 100
            with col2:
                tax_authority_property_value = st.number_input("Tax Authority's Property Valuation (DKK)",
                                                               value=6822000, step=100000)
                tax_authority_land_value = st.number_input("Tax Authority's Land Valuation (DKK)",
                                                           value=3869000, step=100000)
                annual_revaluation_rate = st.slider("Annual Revaluation Rate (Tax Valuation) (%)",
                                                    0.0, 5.0, 1.5, 0.1) / 100

        with st.expander("🔧 Other Ownership Costs", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                base_insurance = st.number_input("Home Insurance (Year 1)", value=30000, step=1000)
                base_maintenance = st.number_input("Maintenance (Year 1)", value=5000, step=1000)
            with col2:
                base_renovations = st.number_input("Renovations (Year 1)", value=10000, step=1000)
                community_ownership_cost = st.number_input("Monthly Community Ownership Fee (Year 1)",
                                                           value=5609, step=500)
                monthly_car_lease = st.number_input("Monthly Car Lease (if any)", value=0, step=500)

        with st.expander("🏷️ Future Selling Costs", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                agent_commission_rate = st.slider("Agent Commission Rate (%)", 0.0, 10.0, 2.0, 0.1) / 100
            with col2:
                capital_gains_tax_rate = st.slider("Capital Gains Tax Rate (%)", 0.0, 50.0, 0.0, 1.0) / 100

    # Build the inputs dictionary
    inputs = {
        "general": {
            "inflation_rate": inflation_rate,
            "savings_interest_rate": savings_interest_rate,
            "analysis_years": int(analysis_years),
            "house_appreciation_rate": house_appreciation_rate,
            "rent_increase_rate": rent_increase_rate
        },
        "rent": {
            "current_monthly_rent": current_monthly_rent,
            "annual_renters_insurance": annual_renters_insurance
        },
        "buy": {
            "cash_price": cash_price,
            "downpayment": downpayment,
            "closing_costs": closing_costs,
            "mortgage_rate": mortgage_rate,
            "mortgage_term_years": int(mortgage_term_years),
            
            "property_value_tax_rate_below_9200000": property_value_tax_below_9200k,
            "property_value_tax_rate_above_9200000": property_value_tax_above_9200k,
            "land_tax_rate": land_tax_rate,
            
            "tax_authority_property_value": tax_authority_property_value,
            "tax_authority_land_value": tax_authority_land_value,
            "annual_revaluation_rate": annual_revaluation_rate,
            
            "base_insurance": base_insurance,
            "base_maintenance": base_maintenance,
            "base_renovations": base_renovations,
            "community_ownership_cost": community_ownership_cost,
            "monthly_car_lease": monthly_car_lease,
            
            "interest_deduction_rate": interest_deduction_rate
        },
        "selling": {
            "agent_commission_rate": agent_commission_rate,
            "capital_gains_tax_rate": capital_gains_tax_rate
        }
    }

    # Perform calculations
    rent_df = calculate_rent_scenario(inputs)
    buy_df = calculate_buy_scenario(inputs)
    rent_invest_df = calculate_rent_investment_scenario(inputs, rent_df, buy_df)
    comparison_result = compare_scenarios(rent_df, buy_df, rent_invest_df, inputs)

    # Show results in tab
    with tab_results:
        st.header("Summary")
        difference = comparison_result["difference_in_net_worth"]
        if difference > 0:
            st.success(
                f"After {analysis_years} years, **buying** leads to "
                f"**{abs(difference):,.0f} DKK more** net worth than renting."
            )
        elif difference < 0:
            st.warning(
                f"After {analysis_years} years, **renting** leads to "
                f"**{abs(difference):,.0f} DKK more** net worth than buying."
            )
        else:
            st.info(
                f"After {analysis_years} years, both scenarios end up with exactly the same net worth!"
            )

        # Key metrics
        st.subheader("Key Financial Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Final Net Worth (Buying)", 
                f"{comparison_result['final_net_equity_buying']:,.0f} DKK",
                f"{comparison_result['difference_in_net_worth']:,.0f} DKK"
            )
            st.metric(
                "Total Buy Outflow", 
                f"{comparison_result['total_buy_outflow']:,.0f} DKK"
            )
        with col2:
            st.metric(
                "Final Net Worth (Rent + Invest)", 
                f"{comparison_result['final_rent_net_worth']:,.0f} DKK"
            )
            st.metric(
                "Total Rent Outflow", 
                f"{comparison_result['total_rent_outflow']:,.0f} DKK"
            )

        # Dataframes
        st.subheader("Detailed Data")
        st.write("**Rent Scenario**")
        st.dataframe(rent_df.style.format("{:,.2f}"))
        st.write("**Buy Scenario**")
        st.dataframe(buy_df.style.format("{:,.2f}"))
        st.write("**Rent + Invest Scenario**")
        st.dataframe(rent_invest_df.style.format("{:,.2f}"))

        # Plots
        st.subheader("Visual Comparisons")
        fig1 = plot_annual_outflow(rent_df, buy_df)
        st.pyplot(fig1)

        fig2 = plot_investment_growth(rent_invest_df)
        st.pyplot(fig2)

        fig3 = plot_net_equity_over_time(buy_df)
        st.pyplot(fig3)

        fig4 = plot_buy_cost_breakdown(buy_df)
        st.pyplot(fig4)

        fig5 = plot_rent_cost_breakdown(rent_df)
        st.pyplot(fig5)

        fig6 = plot_mortgage_vs_value(buy_df)
        st.pyplot(fig6)

        fig7 = plot_net_worth_difference(buy_df, rent_invest_df)
        st.pyplot(fig7)

        fig8 = plot_cumulative_outflow(rent_df, buy_df)
        st.pyplot(fig8)

    st.write("Adjust the sliders in the input tab to explore different assumptions.")

if __name__ == "__main__":
    main()
