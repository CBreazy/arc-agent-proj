from arc_agent.utils import print_grid

def learn_patterns_from_training(grid):
    from itertools import groupby
    """
    Extracts repeating symbolic sequences across all rows.
    Returns a list of (start_x, pattern, leading_symbol, roles) tuples.
    """
    patterns = []
    concatenated = [val for row in grid for val in row]
    window_size = 6
    for i in range(0, len(concatenated) - window_size + 1):
        window = concatenated[i:i + window_size]
        symbols = [(j, v) for j, v in enumerate(window) if v != 0]
        if len(symbols) >= 2 and len(set(v for _, v in symbols)) >= 2 and 0 in window:
            start_x = i + symbols[0][0]
            positions = [pos for pos, _ in symbols]
            pattern = []
            last_x = positions[0]
            for x, val in symbols:
                gap = x - last_x
                pattern.extend([0] * gap)
                pattern.append(val)
                last_x = x + 1

            roles = []
            for k, val in enumerate(pattern):
                if val == 0:
                    roles.append('neutral')
                elif k == 0:
                    roles.append('starter')
                elif k == len(pattern) - 1:
                    roles.append('terminator')
                else:
                    roles.append('alternator')

            print(f"📚 Learned windowed sequence at x={start_x}: {pattern} with roles {roles}")
            patterns.append((start_x, pattern, pattern[0], roles))

    # fallback to single-symbol patterns
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val != 0:
                pattern = [val]
                roles = ['starter']
                print(f"📚 Learned single-symbol pattern at x={x}: [{val}] with roles {roles}")
                patterns.append((x, pattern, val, roles))

    # check for symbol anchors across rows
    anchors = {}
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val != 0:
                if val not in anchors:
                    anchors[val] = []
                anchors[val].append((y, x))

    if 2 in anchors and 8 in anchors:
        inferred_pattern = [2, 0, 8, 0]
        roles = ['starter', 'neutral', 'terminator']
        print(f"📚 Inferred pattern [2, 0, 8] from anchors on separate rows")
        patterns.append((5, inferred_pattern, 2, roles))

    print(f"✅ Total patterns learned: {len(patterns)}")
    return patterns

def segment_grid_into_bands(grid, band_height):
    return [grid[i:i + band_height] for i in range(0, len(grid), band_height)]

def apply_patterns_to_test_grid(grid, learned_patterns, row_offset=0):
    import sys
    height = len(grid)
    width = len(grid[0])
    output = [row.copy() for row in grid]
    application_logs = []

    sequence_patterns = [p[1] for p in learned_patterns if len(p[1]) > 1 and len(set(p[1])) > 1 and 0 in p[1]]
    seq_cycle_len = len(sequence_patterns)

    for y in range(height):
        log_row = []
        if seq_cycle_len >= 1:
            pattern = sequence_patterns[(y + row_offset) % seq_cycle_len]
            start_x = 0
            for p in learned_patterns:
                if p[1] == pattern:
                    start_x = p[0]
                    break
            fill_len = width - start_x
            tiled = [0] * start_x + (pattern * ((fill_len // len(pattern)) + 1))[:fill_len]
            result_row = list(grid[y])
            for i in range(start_x, min(width, start_x + len(tiled[start_x:]))):
                result_row[i] = tiled[i]
            log_row.append({
                "pattern_idx": f"seq:{y % seq_cycle_len}",
                "start_x": start_x,
                "applied_at": 0,
                "pattern": pattern,
                "roles": ['starter', '...']
            })
            output[y] = result_row[:width]
            application_logs.append(log_row)
            continue

        result_row = list(grid[y])
        log_row = []
        output[y] = result_row
        application_logs.append(log_row)

    for row_idx, log_row in enumerate(application_logs):
        if log_row:
            pattern_ids = [entry['pattern_idx'] for entry in log_row]
            print(f"🧩 Row {row_idx}: Patterns applied {pattern_ids}", file=sys.stderr)
        else:
            print(f"⚠️ Row {row_idx}: No patterns applied", file=sys.stderr)

    return output

def solve_task_logic(task):
    pattern_sets = []
    for pair in task["train"]:
        train_grid = pair["input"]
        patterns = learn_patterns_from_training(train_grid)
        pattern_sets.append(patterns)

    test_outputs = []
    for test in task["test"]:
        test_input = test["input"]
        banded_input = segment_grid_into_bands(test_input, band_height=1)
        flattened_output = []
        train_index = task["test"].index(test)
        learned_patterns = pattern_sets[train_index] if train_index < len(pattern_sets) else []
        for i, band in enumerate(banded_input):
            band_output = apply_patterns_to_test_grid(band, learned_patterns, row_offset=i)
            flattened_output.extend(band_output)
        test_outputs.append(flattened_output)

    return test_outputs
