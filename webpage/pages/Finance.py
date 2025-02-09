import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

# Set the page title and layout
st.set_page_config(page_title="Finance Page", layout="wide")

# Add sidebar with styling
st.markdown("""
    <style>
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    #MainMenu {
        display: none;
    }
    section[data-testid="stSidebarNav"] {
        display: none;
    }
    .main-title {
        text-align: center;
        color: #1f1f1f;
        font-size: 36px;
        font-weight: 600;
        margin-bottom: 30px;
        padding-top: 20px;
    }
    [data-testid="stDataFrame"] {
        padding: 0px !important;
    }
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stDataFrame"] > div {
        height: fit-content !important;
    }
    </style>
""", unsafe_allow_html=True)

# Add main title
st.markdown('<div class="main-title">Quantitative Trading</div>', unsafe_allow_html=True)

# Read and process data
import os
df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tradingHist.csv'))
df.rename(columns={'hyp': 'Portfolio', 'hyp2': 'SPXTR Index'}, inplace=True)
df['Portfolio'] = df['Portfolio'].str.replace('$', '').astype(float)
df['SPXTR Index'] = df['SPXTR Index'].str.replace('$', '').astype(float)
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df['Portfolio_Return'] = df['Portfolio'].pct_change()
df['SPXTR_Return'] = df['SPXTR Index'].pct_change()

# Calculate monthly returns
df['YearMonth'] = df['Date'].dt.to_period('M')
monthly_returns = df.groupby('YearMonth').agg({
    'Portfolio_Return': lambda x: (1 + x).prod() - 1,
    'SPXTR_Return': lambda x: (1 + x).prod() - 1
}).reset_index()

def get_normalized_data(df, days=None):
    """Normalize data for the last N days, rebasing both series to 100 at start"""
    if days:
        start_date = df['Date'].max() - pd.Timedelta(days=days)
        temp_df = df[df['Date'] >= start_date].copy()
    else:
        temp_df = df.copy()
    
    # Get initial values
    port_start = temp_df['Portfolio'].iloc[0]
    spx_start = temp_df['SPXTR Index'].iloc[0]
    
    # Normalize both series to 100
    temp_df['Portfolio'] = temp_df['Portfolio'] / port_start * 100
    temp_df['SPXTR Index'] = temp_df['SPXTR Index'] / spx_start * 100
    
    return temp_df

def calculate_metrics(filtered_df, monthly_rets):
    """Calculate enhanced portfolio metrics including all major risk-adjusted ratios"""
    days_in_year = 252
    
    # Daily returns calculations
    returns = filtered_df['Portfolio_Return'].dropna()
    benchmark_returns = filtered_df['SPXTR_Return'].dropna()
    
    # Monthly returns calculations
    monthly_port_returns = monthly_rets['Portfolio_Return']
    monthly_bench_returns = monthly_rets['SPXTR_Return']
    
    # Basic return metrics
    total_return = (filtered_df['Portfolio'].iloc[-1] / filtered_df['Portfolio'].iloc[0] - 1)
    annualization_factor = days_in_year / (len(filtered_df) - 1)
    annualized_return = (1 + total_return) ** annualization_factor - 1
    
    # Risk calculations
    daily_std = returns.std()
    monthly_std = monthly_port_returns.std()
    annualized_vol = daily_std * np.sqrt(days_in_year)
    
    # Sharpe Ratio calculations
    daily_sharpe = np.mean(returns) / np.std(returns)
    annualized_sharpe = daily_sharpe * np.sqrt(days_in_year)
    
    monthly_sharpe = np.mean(monthly_port_returns) / np.std(monthly_port_returns)
    monthly_annualized_sharpe = monthly_sharpe * np.sqrt(12)
    
    # Beta calculation
    beta = returns.cov(benchmark_returns) / benchmark_returns.var()
    
    # Treynor Ratio (annualized return / beta)
    treynor_ratio = annualized_return / beta if beta != 0 else np.nan
    
    # Information Ratio calculations
    # Daily tracking error and IR
    daily_active_returns = returns - benchmark_returns
    tracking_error_daily = np.std(daily_active_returns) * np.sqrt(days_in_year)
    information_ratio = np.mean(daily_active_returns) * days_in_year / tracking_error_daily if tracking_error_daily != 0 else np.nan
    
    # Monthly tracking error and IR
    monthly_active_returns = monthly_port_returns - monthly_bench_returns
    tracking_error_monthly = np.std(monthly_active_returns) * np.sqrt(12)
    monthly_information_ratio = np.mean(monthly_active_returns) * 12 / tracking_error_monthly if tracking_error_monthly != 0 else np.nan
    
    # Sortino Ratio calculations
    # Daily Sortino
    downside_returns = returns[returns < 0]
    downside_std = np.sqrt(np.mean(downside_returns**2)) * np.sqrt(days_in_year)
    sortino_ratio = annualized_return / downside_std if len(downside_returns) > 0 else np.nan
    
    # Monthly Sortino
    monthly_downside_returns = monthly_port_returns[monthly_port_returns < 0]
    monthly_downside_std = np.sqrt(np.mean(monthly_downside_returns**2)) * np.sqrt(12)
    monthly_sortino = (np.mean(monthly_port_returns) * 12) / monthly_downside_std if len(monthly_downside_returns) > 0 else np.nan
    
    # Drawdown calculations
    portfolio_values = filtered_df['Portfolio']
    rolling_max = portfolio_values.expanding().max()
    drawdowns = (portfolio_values - rolling_max) / rolling_max
    max_drawdown = drawdowns.min() * 100  # Convert to percentage
    
    # Monthly statistics
    best_month = monthly_port_returns.max() * 100
    worst_month = monthly_port_returns.min() * 100
    avg_month = monthly_port_returns.mean() * 100
    up_months = (monthly_port_returns > 0).mean() * 100
    down_months = (monthly_port_returns < 0).mean() * 100
    avg_loss = monthly_port_returns[monthly_port_returns < 0].mean() * 100 if len(monthly_port_returns[monthly_port_returns < 0]) > 0 else 0
    
    # Distribution statistics
    skewness = stats.skew(monthly_port_returns)
    kurtosis = stats.kurtosis(monthly_port_returns)
    
    metrics_data = {
        'Metric': [
            'Total Return',
            'Annualized Return',
            'Annualized Volatility',
            'Sharpe Ratio (Ann.)',
            'Monthly Sharpe (Ann.)',
            'Sortino Ratio (Ann.)',
            'Monthly Sortino (Ann.)',
            'Information Ratio',
            'Monthly Info Ratio',
            'Treynor Ratio',
            'Tracking Error (Ann.)',
            'Beta',
            'Maximum Drawdown',
            'Best Month',
            'Worst Month',
            'Average Month',
            'Up Months %',
            'Down Months %',
            'Average Loss',
            'Monthly Std Dev (Ann.)',
            'Skewness',
            'Kurtosis'
        ],
        'Value': [
            f"{total_return*100:,.2f}%",
            f"{annualized_return*100:,.2f}%",
            f"{annualized_vol*100:,.2f}%",
            f"{annualized_sharpe:.2f}",
            f"{monthly_annualized_sharpe:.2f}",
            f"{sortino_ratio:.2f}",
            f"{monthly_sortino:.2f}",
            f"{information_ratio:.2f}",
            f"{monthly_information_ratio:.2f}",
            f"{treynor_ratio:.2f}",
            f"{tracking_error_daily*100:.2f}%",
            f"{beta:.2f}",
            f"{max_drawdown:,.2f}%",
            f"{best_month:.2f}%",
            f"{worst_month:.2f}%",
            f"{avg_month:.2f}%",
            f"{up_months:.1f}%",
            f"{down_months:.1f}%",
            f"{avg_loss:.2f}%",
            f"{monthly_std*np.sqrt(12)*100:.2f}%",
            f"{skewness:.2f}",
            f"{kurtosis:.2f}"
        ]
    }
    
    return pd.DataFrame(metrics_data)

# Add sidebar navigation
with st.sidebar:
    st.title("Trading Philosophy")
    philosophy_nav = st.radio(
        "Trading Strategy Selection",
        ["Performance Dashboard"],
        key="philosophy_nav",
        label_visibility="collapsed"
    )

# Handle Trading Philosophy navigation
if philosophy_nav == "Performance Dashboard":
    # Add introductory paragraph with styling
    st.markdown("""
        <div style='max-width: 1200px; margin: 0 auto 40px auto; text-align: justify; line-height: 1.8; font-size: 18px; color: #333; padding: 0 20px;'>
        Below are performance statistics for my Live Traded Portfolio. Assets traded include /ES Futures, Options on these Futures, SPX Options and occasional small options trades on equities. 
        The goal of the portfolio is to provide market return greater than the index level, but without the same downside risks. The portfolio is always hedged to protect from losses
        that may occur beyond the index returns.
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="small")

    with col1:
        # Calculate metrics
        metrics_df = calculate_metrics(df, monthly_returns)
        
        # Display the dataframe with exact height
        st.dataframe(
            data=metrics_df,
            column_config={
                "Metric": st.column_config.TextColumn(
                    "Metric",
                    width=200,
                    help={
                        "Sharpe Ratio (Ann.)": "Risk-adjusted return measure: (Portfolio Return - Risk Free Rate) / Portfolio Standard Deviation. Annualized using daily returns × √252.\n\nInterpretation:\n• < 0: Poor risk-adjusted returns\n• 0-1: Suboptimal\n• 1-2: Good\n• > 2: Excellent\n\nTop hedge funds typically maintain ratios above 1.5.",
                        "Sortino Ratio (Ann.)": "Similar to Sharpe ratio but only penalizes downside volatility: Annualized Return / Annualized Downside Standard Deviation.\n\nInterpretation:\n• < 0: Poor risk-adjusted returns\n• 0-1: Below average\n• 1-2: Good\n• > 2: Excellent\n\nTypically higher than Sharpe ratio as it ignores upside volatility.",
                        "Information Ratio": "Measures portfolio returns above the benchmark per unit of tracking error: (Portfolio Return - Benchmark Return) / Tracking Error.\n\nInterpretation:\n• < 0: Underperforming benchmark\n• 0-0.5: Moderate skill\n• 0.5-1: Good skill\n• > 1: Excellent skill\n\nTop managers typically maintain ratios above 0.5.",
                        "Treynor Ratio": "Risk-adjusted return using beta instead of standard deviation: Annualized Return / Beta.\n\nInterpretation:\n• Should be compared to market return\n• Higher values indicate better risk-adjusted performance\n• Negative values suggest poor risk management",
                        "Tracking Error (Ann.)": "Standard deviation of the difference between portfolio and benchmark returns, annualized.\n\nInterpretation:\n• < 2%: Very close index tracking\n• 2-5%: Moderate active management\n• 5-10%: Active management\n• > 10%: Highly active management",
                        "Beta": "Measure of portfolio's volatility compared to the market: Covariance(Portfolio, Benchmark) / Variance(Benchmark).\n\nInterpretation:\n• < 0: Inverse market movement\n• 0-1: Less volatile than market\n• 1: Same as market\n• > 1: More volatile than market",
                        "Maximum Drawdown": "Largest peak-to-trough decline in portfolio value.\n\nInterpretation:\n• 0-10%: Conservative\n• 10-20%: Moderate\n• 20-30%: Aggressive\n• > 30%: Very aggressive/high risk\n\nS&P 500 typically experiences 10-20% drawdowns every few years.",
                        "Skewness": "Measures asymmetry in returns distribution.\n\nInterpretation:\n• < -1: Strong negative skew (frequent small gains, rare large losses)\n• -1 to 1: Relatively symmetric\n• > 1: Strong positive skew (frequent small losses, rare large gains)\n\nPositive skewness is generally preferred.",
                        "Kurtosis": "Measures 'tailedness' of returns distribution.\n\nInterpretation:\n• < 0: Less extreme outcomes than normal distribution\n• ≈ 0: Normal distribution\n• > 0: More extreme outcomes\n• > 3: Significantly 'fat tails'",
                        "Monthly Info Ratio": "Information ratio using monthly returns.\n\nSimilar interpretation to daily Information Ratio but may better capture longer-term skill.",
                        "Monthly Sortino (Ann.)": "Sortino ratio using monthly returns (× √12).\n\nTypically more stable than daily Sortino but may miss short-term risks.",
                        "Monthly Sharpe (Ann.)": "Sharpe ratio using monthly returns (× √12).\n\nTypically more stable than daily Sharpe but may miss short-term risks."
                    }
                ),
                "Value": st.column_config.TextColumn(
                    "Value",
                    width=150,
                ),
            },
            hide_index=True,
            use_container_width=True,
            height=(len(metrics_df) * 36 + 15)  # Precise height calculation based on number of rows
        )

    with col2:
        # Add time period selector
        timeframe = st.radio(
            "Select Time Period",
            ["1M", "3M", "YTD", "ALL"],
            horizontal=True,
            key="timeframe"
        )
        
        # Get normalized data based on selection
        if timeframe == "1M":
            plot_df = get_normalized_data(df, days=30)
        elif timeframe == "3M":
            plot_df = get_normalized_data(df, days=90)
        elif timeframe == "YTD":
            ytd_start = pd.Timestamp(df['Date'].max().year, 1, 1)
            plot_df = get_normalized_data(df[df['Date'] >= ytd_start])
        else:  # ALL
            plot_df = get_normalized_data(df)

        # Calculate percentage change from start for hover info
        plot_df['Portfolio_pct'] = (plot_df['Portfolio'] - 100).round(2)
        plot_df['SPXTR_pct'] = (plot_df['SPXTR Index'] - 100).round(2)

        # Create performance figure with custom data
        fig = px.line(plot_df, 
                     x='Date', 
                     y=['Portfolio', 'SPXTR Index'],
                     labels={'value': 'Normalized Value', 'variable': 'Series'},
                     title=f'Relative Performance ({timeframe})',
                     custom_data=[plot_df['Portfolio_pct'], plot_df['SPXTR_pct']])

        fig.update_layout(
            height=500,
            margin=dict(l=0, r=0, t=40, b=0),
            title_font_size=24,
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Normalized Value (Base=100)",
            yaxis_type="log",
            legend_title="Series",
            template="plotly_dark",
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        # Update hover template to show value and percentage change
        fig.update_traces(
            hovertemplate="<b>Value: %{y:.2f}</b><br>"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Add distribution period selector
        distribution_period = st.radio(
            "Return Distribution Period",
            ["Monthly", "Daily"],
            horizontal=True,
            key="distribution_period"
        )

        # Create distribution figure
        fig_dist = go.Figure()

        if distribution_period == "Monthly":
            # Calculate overall range for consistent binning
            all_returns = pd.concat([
                monthly_returns['Portfolio_Return'],
                monthly_returns['SPXTR_Return']
            ])
            min_return = all_returns.min() * 100
            max_return = all_returns.max() * 100
            bin_size = (max_return - min_return) / 20  # 20 bins
            bin_edges = np.arange(min_return, max_return + bin_size, bin_size)

            # Monthly returns distribution with consistent bins
            fig_dist.add_trace(go.Histogram(
                x=monthly_returns['Portfolio_Return'] * 100,
                name='Portfolio',
                opacity=0.75,
                xbins=dict(
                    start=min_return,
                    end=max_return,
                    size=bin_size
                ),
                autobinx=False
            ))

            fig_dist.add_trace(go.Histogram(
                x=monthly_returns['SPXTR_Return'] * 100,
                name='SPXTR Index',
                opacity=0.75,
                xbins=dict(
                    start=min_return,
                    end=max_return,
                    size=bin_size
                ),
                autobinx=False
            ))

            x_title = 'Monthly Return (%)'
        else:
            # Same approach for daily returns
            all_returns = pd.concat([
                df['Portfolio_Return'].dropna(),
                df['SPXTR_Return'].dropna()
            ])
            min_return = all_returns.min() * 100
            max_return = all_returns.max() * 100
            bin_size = (max_return - min_return) / 30  # 30 bins
            bin_edges = np.arange(min_return, max_return + bin_size, bin_size)

            fig_dist.add_trace(go.Histogram(
                x=df['Portfolio_Return'].dropna() * 100,
                name='Portfolio',
                opacity=0.75,
                xbins=dict(
                    start=min_return,
                    end=max_return,
                    size=bin_size
                ),
                autobinx=False
            ))

            fig_dist.add_trace(go.Histogram(
                x=df['SPXTR_Return'].dropna() * 100,
                name='SPXTR Index',
                opacity=0.75,
                xbins=dict(
                    start=min_return,
                    end=max_return,
                    size=bin_size
                ),
                autobinx=False
            ))

            x_title = 'Daily Return (%)'

        fig_dist.update_layout(
            title=f'{distribution_period} Returns Distribution',
            title_x=0.5,
            xaxis_title=x_title,
            yaxis_title='Frequency',
            barmode='overlay',
            template="plotly_dark",
            height=300,
            margin=dict(l=0, r=0, t=40, b=0),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        st.plotly_chart(fig_dist, use_container_width=True)
        st.markdown("""
        <div style='text-align: center; color: #666666; font-size: 12px; font-style: italic; padding: 20px 0px;'>
        Disclaimer: Performance values are derived from broker-provided daily account balance calculations and may not precisely reflect actual account values at every point in time.
        </div>
        """, unsafe_allow_html=True)