from classes import Trial


def reform_data(trial_entry: [str, int, int]) -> Trial or None:
    if trial_entry[0] == "Win":
        return Trial("Win", 0, 0)
    elif trial_entry[0] == "Lose":
        if not trial_entry[1] or not trial_entry[2]:
            return None
        return Trial(*trial_entry)
    else:
        return None
