import pandas as pd

import math

def calculate_monthly_mortgage_payment(principal, annual_interest_rate, years):
    """
    Computes the monthly mortgage payment using the standard annuity formula.
    """
    monthly_rate = annual_interest_rate / 12
    num_payments = years * 12
    if monthly_rate == 0:
        return principal / num_payments
    payment = principal * (monthly_rate / (1 - (1 + monthly_rate) ** (-num_payments)))
    return payment

def apply_rent_increase(initial_rent, rent_increase_rate, year):
    """Returns monthly rent for a given year, applying annual compounding."""
    return initial_rent * ((1 + rent_increase_rate) ** (year - 1))

def apply_house_appreciation(initial_value, appreciation_rate, year):
    """Returns house value for a given year, applying annual compounding."""
    return initial_value * ((1 + appreciation_rate) ** (year - 1))

def apply_inflation(base_cost, inflation_rate, year):
    """Returns inflated cost for a given year, using annual compounding."""
    return base_cost * ((1 + inflation_rate) ** (year - 1))

def calculate_rent_scenario(inputs):
    """
    Builds a year-by-year DataFrame of rent costs (including insurance).
    """
    rent_data = []
    years = inputs["general"]["analysis_years"]
    rent_increase_rate = inputs["general"]["rent_increase_rate"]
    current_monthly_rent = inputs["rent"]["current_monthly_rent"]
    annual_renters_insurance = inputs["rent"]["annual_renters_insurance"]
    
    for year in range(1, years + 1):
        monthly_rent_this_year = apply_rent_increase(
            current_monthly_rent, 
            rent_increase_rate, 
            year
        )
        annual_rent = monthly_rent_this_year * 12
        total_rent_cost = annual_rent + annual_renters_insurance
        
        rent_data.append({
            "year": year,
            "monthly_rent": monthly_rent_this_year,
            "annual_rent": annual_rent,
            "renters_insurance": annual_renters_insurance,
            "total_rent_cost": total_rent_cost
        })
    
    return pd.DataFrame(rent_data)

def calculate_buy_scenario(inputs):
    """
    Builds a year-by-year DataFrame of homeownership costs and equity.
    """
    purchase_price = inputs["buy"]["cash_price"]
    downpayment = inputs["buy"]["downpayment"]
    closing_costs = inputs["buy"]["closing_costs"]  # one-time upfront
    annual_interest_rate = inputs["buy"]["mortgage_rate"]
    mortgage_term = inputs["buy"]["mortgage_term_years"]
    
    base_insurance = inputs["buy"]["base_insurance"]
    base_maintenance = inputs["buy"]["base_maintenance"]
    base_renovations = inputs["buy"]["base_renovations"]
    community_ownership_cost = inputs["buy"]["community_ownership_cost"]
    
    interest_deduction_rate = inputs["buy"]["interest_deduction_rate"]
    monthly_car_lease = inputs["buy"]["monthly_car_lease"]
    
    # General parameters
    analysis_years = inputs["general"]["analysis_years"]
    inflation_rate = inputs["general"]["inflation_rate"]
    appreciation_rate = inputs["general"]["house_appreciation_rate"]
    
    # Property tax rates
    property_value_tax_rate_below_9200000 = inputs["buy"]["property_value_tax_rate_below_9200000"]
    property_value_tax_rate_above_9200000 = inputs["buy"]["property_value_tax_rate_above_9200000"]
    land_tax_rate = inputs["buy"]["land_tax_rate"]
    
    # Tax authority valuations
    tax_authority_property_value = inputs["buy"]["tax_authority_property_value"]
    tax_authority_land_value = inputs["buy"]["tax_authority_land_value"]
    annual_revaluation_rate = inputs["buy"]["annual_revaluation_rate"]
    
    # Mortgage
    loan_amount = purchase_price - downpayment
    monthly_payment = calculate_monthly_mortgage_payment(
        loan_amount, annual_interest_rate, mortgage_term
    )
    
    mortgage_balance = loan_amount
    buy_data = []
    
    # Month-by-month schedule
    monthly_records = []
    total_months = mortgage_term * 12
    
    for m in range(1, total_months + 1):
        monthly_interest = mortgage_balance * (annual_interest_rate / 12)
        monthly_principal = monthly_payment - monthly_interest
        
        mortgage_balance -= monthly_principal
        mortgage_balance = max(mortgage_balance, 0)  # avoid negative
        
        monthly_records.append({
            "month": m,
            "interest_paid": monthly_interest,
            "principal_paid": monthly_principal,
            "mortgage_balance": mortgage_balance
        })
    
    monthly_df = pd.DataFrame(monthly_records)
    monthly_df["year"] = ((monthly_df["month"] - 1) // 12) + 1
    
    house_value_start = purchase_price
    
    for year in range(1, analysis_years + 1):
        year_df = monthly_df[monthly_df["year"] == year]
        
        if len(year_df) == 0:
            # Mortgage paid off before this year
            interest_paid_this_year = 0.0
            principal_paid_this_year = 0.0
            mortgage_balance_end = 0.0
        else:
            interest_paid_this_year = year_df["interest_paid"].sum()
            principal_paid_this_year = year_df["principal_paid"].sum()
            mortgage_balance_end = year_df["mortgage_balance"].iloc[-1]
        
        # House value start and end of year
        if year == 1:
            house_value_start_year = house_value_start
        else:
            house_value_start_year = buy_data[-1]["house_value_end"]
        
        house_value_end_year = house_value_start_year * (1 + appreciation_rate)
        
        # Property value tax calculation
        taxable_value = tax_authority_property_value * 0.8  # example logic
        if taxable_value <= 9200000:
            property_value_tax_this_year = taxable_value * property_value_tax_rate_below_9200000
        else:
            property_value_tax_this_year = (
                9200000 * property_value_tax_rate_below_9200000
                + (taxable_value - 9200000) * property_value_tax_rate_above_9200000
            )
        
        # Land tax calculation
        taxable_land_value = tax_authority_land_value * (1 - 0.20)
        land_tax_this_year = taxable_land_value * land_tax_rate
        
        # Apply inflation to certain costs
        insurance_this_year = apply_inflation(base_insurance, inflation_rate, year)
        maintenance_this_year = apply_inflation(base_maintenance, inflation_rate, year)
        renovations_this_year = apply_inflation(base_renovations, inflation_rate, year)
        community_ownership_cost_this_year = apply_inflation(
            community_ownership_cost * 12, inflation_rate, year
        )
        car_lease_this_year = apply_inflation(monthly_car_lease * 12, inflation_rate, year)
        
        # Interest deduction
        net_interest_paid_this_year = interest_paid_this_year * (1 - interest_deduction_rate)
        
        total_annual_outflow = (
            net_interest_paid_this_year
            + principal_paid_this_year
            + property_value_tax_this_year
            + land_tax_this_year
            + insurance_this_year
            + maintenance_this_year
            + renovations_this_year
            + community_ownership_cost_this_year
            + car_lease_this_year
        )
        
        net_equity_end = house_value_end_year - mortgage_balance_end
        
        buy_data.append({
            "year": year,
            "interest_paid": net_interest_paid_this_year,
            "principal_paid": principal_paid_this_year,
            "property_value_tax": property_value_tax_this_year,
            "land_tax": land_tax_this_year,
            "insurance": insurance_this_year,
            "maintenance": maintenance_this_year,
            "renovations": renovations_this_year,
            "community_ownership_cost": community_ownership_cost_this_year,
            "car_lease": car_lease_this_year,
            "total_outflow": total_annual_outflow,
            "mortgage_balance_end": mortgage_balance_end,
            "house_value_start": house_value_start_year,
            "house_value_end": house_value_end_year,
            "net_equity_end": net_equity_end
        })
        
        # Revalue the property for next year
        tax_authority_property_value *= (1 + annual_revaluation_rate)
        tax_authority_land_value *= (1 + annual_revaluation_rate)
    
    return pd.DataFrame(buy_data)

def calculate_rent_investment_scenario(inputs, rent_df, buy_df):
    """
    Simulates investing the downpayment + closing costs plus 
    any annual cost difference (if renting is cheaper).
    """
    merged = pd.DataFrame({
        "year": rent_df["year"],
        "rent_outflow": rent_df["total_rent_cost"],
        "buy_outflow": buy_df["total_outflow"]
    })
    
    initial_investment = inputs["buy"]["downpayment"] + inputs["buy"]["closing_costs"]
    savings_rate = inputs["general"]["savings_interest_rate"]
    analysis_years = inputs["general"]["analysis_years"]
    
    rent_invest_data = []
    investment_balance = initial_investment
    
    for year in range(1, analysis_years + 1):
        row = merged[merged["year"] == year].iloc[0]
        
        rent_cost = row["rent_outflow"]
        buy_cost = row["buy_outflow"]
        
        # difference = how much cheaper (or more expensive) renting is vs buying
        difference = buy_cost - rent_cost
        
        investment_start = investment_balance
        investment_after_diff = investment_start + difference
        
        # Apply annual interest
        investment_end = investment_after_diff * (1 + savings_rate)
        
        investment_balance = investment_end
        
        rent_invest_data.append({
            "year": year,
            "rent_outflow": rent_cost,
            "buy_outflow": buy_cost,
            "difference": difference,
            "investment_start": investment_start,
            "investment_end": investment_end
        })
    
    df_rent_invest = pd.DataFrame(rent_invest_data)
    df_rent_invest["final_rent_net_worth"] = df_rent_invest["investment_end"].iloc[-1]
    return df_rent_invest

def compare_scenarios(rent_df, buy_df, rent_invest_df, inputs):
    """
    Summarizes total outflow for rent vs. buy,
    and final net worth in each scenario.
    """
    total_rent_outflow = rent_df["total_rent_cost"].sum()
    final_rent_net_worth = rent_invest_df["final_rent_net_worth"].iloc[-1]
    
    total_buy_outflow = buy_df["total_outflow"].sum()
    
    # Final net equity for buying
    last_year = inputs["general"]["analysis_years"]
    final_buy_row = buy_df[buy_df["year"] == last_year].iloc[0]
    final_home_value = final_buy_row["house_value_end"]
    final_mortgage_balance = final_buy_row["mortgage_balance_end"]
    
    raw_equity = final_home_value - final_mortgage_balance
    
    # Selling costs
    commission_rate = inputs["selling"]["agent_commission_rate"]
    capital_gains_rate = inputs["selling"]["capital_gains_tax_rate"]
    
    agent_commission = final_home_value * commission_rate
    purchase_price = inputs["buy"]["cash_price"]
    capital_gains = max(final_home_value - purchase_price, 0)
    cgt = capital_gains * capital_gains_rate
    
    final_net_equity_buying = raw_equity - agent_commission - cgt
    
    difference_in_net_worth = final_net_equity_buying - final_rent_net_worth
    
    return {
        "total_rent_outflow": total_rent_outflow,
        "final_rent_net_worth": final_rent_net_worth,
        "total_buy_outflow": total_buy_outflow,
        "final_net_equity_buying": final_net_equity_buying,
        "difference_in_net_worth": difference_in_net_worth
    }
