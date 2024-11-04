import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.stats import norm
import matplotlib.gridspec as gridspec

def calculate_call_delta(S, K, T, r, sigma):
    """Calculate call option delta using Black-Scholes"""
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    return norm.cdf(d1)

def calculate_put_delta(S, K, T, r, sigma):
    """Calculate put option delta using Black-Scholes"""
    return calculate_call_delta(S, K, T, r, sigma) - 1

def create_delta_animation(output_filename='delta_animation.gif'):
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
    
    ax1 = plt.subplot(gs[0])  # Delta plot
    ax2 = plt.subplot(gs[1])  # Stock price indicator
    
    # Style settings
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#1f1f1f')
    ax1.set_facecolor('#2d2d2d')
    ax2.set_facecolor('#2d2d2d')
    
    # Set up delta plot
    ax1.grid(True, alpha=0.2)
    ax1.set_xlim(80, 120)
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_title(f'Option Delta vs Stock Price (K=${strike})', color='white', pad=20)
    ax1.set_xlabel('Stock Price ($)')
    ax1.set_ylabel('Delta')
    
    # Set up stock price indicator
    ax2.set_xlim(80, 120)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('Stock Price ($)')
    ax2.set_xticks(np.arange(80, 121, 10))
    ax2.set_yticks([])
    
    # Calculate deltas
    call_deltas = calculate_call_delta(S_range, strike, T, r, sigma)
    put_deltas = calculate_put_delta(S_range, strike, T, r, sigma)
    
    # Plot lines
    call_line, = ax1.plot(S_range, call_deltas, '--', color='#00ff00', 
                         alpha=0.7, linewidth=2, label='Call Delta')
    put_line, = ax1.plot(S_range, put_deltas, '-', color='#ff3366', 
                        alpha=0.7, linewidth=2, label='Put Delta')
    
    # Add strike price marker
    ax1.axvline(x=strike, color='yellow', alpha=0.3, linestyle=':')
    strike_text = ax1.text(strike, -1.05, f'Strike = ${strike}', color='yellow', ha='center')
    
    # Add zero line
    ax1.axhline(y=0, color='white', alpha=0.2, linestyle='-')
    
    # Add legend
    ax1.legend()
    
    # Initialize stock price indicator
    price_indicator = ax2.axvline(x=80, color='yellow', linewidth=2)
    price_text = ax2.text(80, 0.5, '$80', color='yellow', ha='right', va='center')
    
    # Add markers for current delta values
    call_dot, = ax1.plot([], [], 'o', color='#00ff00', markersize=10)
    put_dot, = ax1.plot([], [], 'o', color='#ff3366', markersize=10)
    
    # Create text objects for delta values
    call_text = ax1.text(85, 0.8, '', color='#00ff00')
    put_text = ax1.text(85, 0.6, '', color='#ff3366')
    
    def update(frame):
        current_price = S_range[frame]
        
        # Update price indicator
        price_indicator.set_xdata([current_price, current_price])
        price_text.set_x(current_price)
        price_text.set_text(f'${current_price:.2f}')
        
        # Update delta markers
        call_dot.set_data([current_price], [call_deltas[frame]])
        put_dot.set_data([current_price], [put_deltas[frame]])
        
        # Update delta value text
        call_text.set_text(f'Call Δ: {call_deltas[frame]:.3f}')
        put_text.set_text(f'Put Δ: {put_deltas[frame]:.3f}')
        
        return price_indicator, price_text, call_dot, put_dot, call_text, put_text
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=len(S_range), 
                        interval=50, repeat=True)
    
    # Save animation
    writer = PillowWriter(fps=30)
    anim.save(output_filename, writer=writer)
    plt.close()

if __name__ == "__main__":
    create_delta_animation()