def validate_data(trial_entry: [str, int, int]) -> [str, int, int] or None:
    if trial_entry[0] == "Win":
        return ["Win", 0, 0]
    elif trial_entry[0] == "Lose":
        if not trial_entry[1] or not trial_entry[2]:
            return None
        return trial_entry
    else:
        return None
