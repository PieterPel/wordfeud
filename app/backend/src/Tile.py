class Tile:
    BASE_COLOR = (186, 212, 193)
    TEXT_COLOR = (0, 0, 0)

    def __init__(self, letter, points):
        self.letter = letter
        self.points = points
        if self.letter == " ":
            self.blank = True
        else:
            self.blank = False

    def __repr__(self):
        if self.blank:
            return self.letter
        else:
            return f"{self.letter}{get_sub(self.points)}"


def get_sub(x):
    """
    Source:
    www.geeksforgeeks.org/how-to-print-superscript-and-subscript-in-python/
    """
    normal = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    )
    sub_s = (
        "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
    )

    x = str(x)
    res = x.maketrans("".join(normal), "".join(sub_s))
    return x.translate(res)
