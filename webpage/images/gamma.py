import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.stats import norm
import matplotlib.gridspec as gridspec

def calculate_gamma(S, K, T, r, sigma):
    """Calculate option gamma using Black-Scholes"""
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    return gamma

def create_gamma_animation(output_filename='gamma_animation.gif'):
    # Parameters
    T = 0.25  # Time to expiration (3 months)
    r = 0.05  # Risk-free rate
    sigma = 0.2  # Volatility
    
    # Single strike price
    strike = 100
    
    # Create stock price range for the animation
    S_range = np.linspace(80, 120, 200)
    
    # Set up the figure with subplots
    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    
    ax1 = plt.subplot(gs[0])  # Gamma plot
    ax2 = plt.subplot(gs[1])  # Stock price indicator
    
    # Style settings
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#1f1f1f')
    ax1.set_facecolor('#2d2d2d')
    ax2.set_facecolor('#2d2d2d')
    
    # Calculate gamma
    gamma_values = calculate_gamma(S_range, strike, T, r, sigma)
    
    # Set up gamma plot
    ax1.grid(True, alpha=0.2)
    ax1.set_xlim(80, 120)
    ax1.set_ylim(0, max(gamma_values) * 1.1)
    ax1.set_title(f'Option Gamma vs Stock Price (K=${strike})', color='white', pad=20)
    ax1.set_xlabel('Stock Price ($)')
    ax1.set_ylabel('Gamma')
    
    # Set up stock price indicator
    ax2.set_xlim(80, 120)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('Stock Price ($)')
    ax2.set_xticks(np.arange(80, 121, 10))
    ax2.set_yticks([])
    
    # Plot gamma line
    gamma_line, = ax1.plot(S_range, gamma_values, '-', color='#00ff88', 
                          alpha=0.7, linewidth=2, label='Gamma')
    
    # Add strike price marker
    ax1.axvline(x=strike, color='yellow', alpha=0.3, linestyle=':')
    strike_text = ax1.text(strike, -0.001, f'Strike = ${strike}', color='yellow', ha='center')
    
    # Add legend
    ax1.legend()
    
    # Initialize stock price indicator
    price_indicator = ax2.axvline(x=80, color='yellow', linewidth=2)
    price_text = ax2.text(80, 0.5, '$80', color='yellow', ha='right', va='center')
    
    # Add marker for current gamma value
    gamma_dot, = ax1.plot([], [], 'o', color='#00ff88', markersize=10)
    
    # Create text object for gamma value
    gamma_text = ax1.text(85, max(gamma_values) * 0.9, '', color='#00ff88')
    
    # Add explanatory text
    hedging_text = ax1.text(105, max(gamma_values) * 0.8, '', color='white', fontsize=9)
    
    def update(frame):
        current_price = S_range[frame]
        current_gamma = gamma_values[frame]
        
        # Update price indicator
        price_indicator.set_xdata([current_price, current_price])
        price_text.set_x(current_price)
        price_text.set_text(f'${current_price:.2f}')
        
        # Update gamma marker
        gamma_dot.set_data([current_price], [current_gamma])
        
        # Update gamma value text
        gamma_text.set_text(f'Γ: {current_gamma:.6f}')
        
        # Update hedging text based on gamma value
        relative_gamma = current_gamma / max(gamma_values)
        if relative_gamma > 0.8:
            hedge_msg = "High gamma region:\nRapid delta changes\nFrequent hedging needed"
        elif relative_gamma > 0.4:
            hedge_msg = "Moderate gamma region:\nModerate delta changes\nRegular hedging needed"
        else:
            hedge_msg = "Low gamma region:\nSlow delta changes\nLess frequent hedging"
        hedging_text.set_text(hedge_msg)
        
        return price_indicator, price_text, gamma_dot, gamma_text, hedging_text
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=len(S_range), 
                        interval=50, repeat=True)
    
    # Save animation
    writer = PillowWriter(fps=30)
    anim.save(output_filename, writer=writer)
    plt.close()

if __name__ == "__main__":
    create_gamma_animation()