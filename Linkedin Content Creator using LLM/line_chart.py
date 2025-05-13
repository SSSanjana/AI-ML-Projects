#line_chart.py
import matplotlib.pyplot as plt

def create_comparison_line_chart(brandboost_scores, other_scores):
    factors = list(brandboost_scores.keys())
    brandboost_values = list(brandboost_scores.values())
    other_values = list(other_scores.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(factors, brandboost_values, marker='o', label="BrandBoost", color='skyblue', linewidth=2)
    ax.plot(factors, other_values, marker='o', label="Other AI Tool", color='orange', linewidth=2)

    ax.set_title("Comparison of Post Effectiveness Factors")
    ax.set_xlabel("Factors")
    ax.set_ylabel("Effectiveness Score (out of 10)")
    ax.set_ylim(0, 10)
    ax.grid(True)
    ax.legend()

    return fig
