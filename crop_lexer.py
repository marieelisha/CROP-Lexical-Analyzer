
import tkinter as tk
from tkinter import ttk


# 1. CROP RESERVED WORDS
keywords = [
    "task", "let", "return", "limit_reached",
    "cleanup", "if", "else", "for", "while",
    "then", "input", "output", "name", "max_steps"
]

data_types = ["int", "float", "bool", "string"]
boolean_values = ["true", "false"]


# 2. OPERATORS AND DELIMITERS
operators = [
    "+", "-", "*", "/", "%", "=",
    "<", ">", "<=", ">=", "==", "!=",
    "&&", "||", "!"
]

two_char_operators = ["==", "!=", "<=", ">=", "&&", "||"]

delimiters = ["(", ")", "{", "}", "[", "]", ";", ",", ":"]


# 3. MAIN LEXICAL ANALYZER
def lexical_analyzer(code):
    tokens = []
    errors = []
    i = 0

    while i < len(code):
        char = code[i]

        # Skip spaces
        if char.isspace():
            i += 1
            continue

        # Check ASCII characters
        if ord(char) > 127:
            errors.append(f"Invalid non-ASCII character: {char}")
            i += 1
            continue

        # Single-line comments
        if code[i:i+2] == "//":
            while i < len(code) and code[i] != "\n":
                i += 1
            continue

        # Multi-line comments
        if code[i:i+2] == "/*":
            end = code.find("*/", i + 2)

            if end == -1:
                errors.append("Unterminated block comment")
                break

            i = end + 2
            continue

        # Identifiers and reserved words
        if char.isalpha() or char == "_":
            start = i

            while i < len(code) and (
                code[i].isalnum() or code[i] == "_"
            ):
                i += 1

            word = code[start:i]

            if word in keywords:
                tokens.append(("KEYWORD", word))

            elif word in data_types:
                tokens.append(("DATA_TYPE", word))

            elif word in boolean_values:
                tokens.append(("BOOLEAN_LITERAL", word))

            elif word == "null":
                tokens.append(("NULL", word))
                errors.append("The keyword 'null' is reserved but not supported.")

            else:
                tokens.append(("IDENTIFIER", word))

            continue

        # Integer and decimal numbers
        if char.isdigit():
            start = i

            while i < len(code) and code[i].isdigit():
                i += 1

            if i < len(code) and code[i] == ".":
                if i + 1 < len(code) and code[i + 1].isdigit():
                    i += 1

                    while i < len(code) and code[i].isdigit():
                        i += 1

                    tokens.append(("FLOAT_LITERAL", code[start:i]))
                else:
                    tokens.append(("INTEGER_LITERAL", code[start:i]))
            else:
                tokens.append(("INTEGER_LITERAL", code[start:i]))

            continue

        # String literals
        if char == '"':
            start = i
            i += 1
            valid = True
            closed = False

            while i < len(code):
                if code[i] == '"':
                    i += 1
                    closed = True
                    break

                elif code[i] == "\\":
                    if i + 1 < len(code):
                        escape = code[i + 1]

                        if escape in ['"', "\\", "n", "t"]:
                            i += 2
                        else:
                            errors.append(
                                f"Invalid string escape: \\{escape}"
                            )
                            valid = False
                            i += 2
                    else:
                        errors.append("Invalid string escape at end of input")
                        valid = False
                        i += 1

                elif code[i] == "\n":
                    errors.append("Line break inside string literal")
                    valid = False
                    break

                else:
                    i += 1

            if not closed:
                errors.append("Unterminated string literal")
                if i < len(code) and code[i] == "\n":
                    i += 1

            elif valid:
                tokens.append(("STRING_LITERAL", code[start:i]))

            continue

        # Two-character operators
        two_char = code[i:i+2]

        if two_char in two_char_operators:
            tokens.append(("OPERATOR", two_char))
            i += 2
            continue

        # One-character operators
        if char in operators:
            tokens.append(("OPERATOR", char))
            i += 1
            continue

        # Delimiters
        if char in delimiters:
            tokens.append(("DELIMITER", char))
            i += 1
            continue

        # Unknown characters
        errors.append(f"Unknown character: {char}")
        i += 1

    return tokens, errors


# 4. ANALYZE BUTTON FUNCTION
def analyze_code():
    code = source_text.get("1.0", tk.END)

    tokens, errors = lexical_analyzer(code)

    # Clear previous results
    for item in token_table.get_children():
        token_table.delete(item)

    error_text.delete("1.0", tk.END)

    # Display tokens and lexemes
    for token, lexeme in tokens:
        token_table.insert("", tk.END, values=(token, lexeme))

    # Display errors
    if errors:
        for error in errors:
            error_text.insert(tk.END, error + "\n")
    else:
        error_text.insert(tk.END, "No lexical errors found.")

    token_count.config(text=f"Total Tokens: {len(tokens)}")


# 5. CLEAR BUTTON FUNCTION
def clear_all():
    source_text.delete("1.0", tk.END)

    for item in token_table.get_children():
        token_table.delete(item)

    error_text.delete("1.0", tk.END)
    token_count.config(text="Total Tokens: 0")


# 6. MAIN WINDOW
window = tk.Tk()
window.title("CROP Lexical Analyzer")
window.geometry("850x700")
window.configure(bg="#f4f6f9")


# 7. HEADER
header = tk.Frame(window, bg="#263859", pady=15)
header.pack(fill="x")

title = tk.Label(
    header,
    text="CROP LEXICAL ANALYZER",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#263859"
)
title.pack()

subtitle = tk.Label(
    header,
    text="Cycle-Driven Resource-Oriented Programming",
    font=("Arial", 10),
    fg="white",
    bg="#263859"
)
subtitle.pack()


# 8. SOURCE CODE INPUT
input_frame = tk.LabelFrame(
    window,
    text="Enter CROP Source Code",
    font=("Arial", 11, "bold"),
    bg="#f4f6f9",
    padx=10,
    pady=10
)
input_frame.pack(fill="both", padx=20, pady=15)

source_text = tk.Text(
    input_frame,
    height=10,
    font=("Consolas", 11),
    wrap="none"
)
source_text.pack(fill="both", expand=True)


# 9. BUTTONS
button_frame = tk.Frame(window, bg="#f4f6f9")
button_frame.pack(pady=5)

analyze_button = tk.Button(
    button_frame,
    text="Analyze Code",
    command=analyze_code,
    bg="#263859",
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
)
analyze_button.pack(side="left", padx=5)

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_all,
    bg="#d9534f",
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
)
clear_button.pack(side="left", padx=5)


# 10. TOKEN RESULTS TABLE
result_frame = tk.LabelFrame(
    window,
    text="Lexical Analysis Results",
    font=("Arial", 11, "bold"),
    bg="#f4f6f9",
    padx=10,
    pady=10
)
result_frame.pack(fill="both", expand=True, padx=20, pady=10)

token_count = tk.Label(
    result_frame,
    text="Total Tokens: 0",
    font=("Arial", 10, "bold"),
    bg="#f4f6f9"
)
token_count.pack(anchor="e")

token_table = ttk.Treeview(
    result_frame,
    columns=("Token", "Lexeme"),
    show="headings",
    height=10
)

token_table.heading("Token", text="TOKEN")
token_table.heading("Lexeme", text="LEXEME")

token_table.column("Token", width=250)
token_table.column("Lexeme", width=400)

token_table.pack(fill="both", expand=True)


# 11. ERROR DISPLAY
error_frame = tk.LabelFrame(
    window,
    text="Lexical Errors",
    font=("Arial", 11, "bold"),
    bg="#f4f6f9",
    padx=10,
    pady=10
)
error_frame.pack(fill="both", padx=20, pady=10)

error_text = tk.Text(
    error_frame,
    height=4,
    font=("Arial", 10),
    fg="red"
)
error_text.pack(fill="both", expand=True)


# 12. RUN THE APPLICATION
window.mainloop()
