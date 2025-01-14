def get_shock_value(lower_threshold, higher_threshold, intensities, shock):
    intensity = intensities[shock - 1]
    if intensity < 0:
        intensity = 0
    if intensity > 100:
        intensity = 100

    m = (higher_threshold - lower_threshold) / 10

    shock_mA = ((m * shock) + lower_threshold) * (intensity / 100)

    return shock_mA
