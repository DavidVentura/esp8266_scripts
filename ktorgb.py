def ktorgb(k):
    k /= 100
    if k > 66:
        return (0, 0, 255)
    import math

    if k < 66:
        r = 255
    else:
        r = k - 60
        r = 329.698727466 * pow(r, -0.1332047592)

    g = k
    g = 99.4708025861 * math.log(g) - 161.1195681661

    if k < 19:
        b = 0
    else:
        b = k - 10
        b = 138.5177312231 * math.log(b) - 305.0447927307

    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    return (r, g, b)
