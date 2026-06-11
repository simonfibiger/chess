def create_pieces():
    return [1, 3, 2, 1]

pics = 1

def reset():
    return create_pieces()  # Return the new value

pics = reset()  # Update the global variable with the return value
print(pics)  # Outputs [1, 3, 2, 1]
