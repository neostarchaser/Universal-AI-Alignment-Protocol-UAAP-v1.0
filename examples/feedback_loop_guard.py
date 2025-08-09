"""
examples/feedback_loop_guard.py
Prevent Wetiko-like spread by tracking a simple reproduction proxy.
"""

def wetiko_Rw(shares: int, adoptions: int, exposures: int) -> float:
    if exposures <= 0:
        return 0.0
    return (shares + adoptions) / exposures

if __name__ == "__main__":
    print("R_w example:", wetiko_Rw(120, 30, 1000))
