from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import re
import ast

app = FastAPI()

FILE_PATH = "/home/ugo/personal_projects/Gym_Data_Project/test_api.py"

# Map form field -> variable name in the destination .py file
SCALE_LIST_NAMES = {
    "value1": "weight_kg",
    "value2": "body_fat",
    "value3": "muscle_mass",
}

CARDIO_LIST_NAME = {
    "value1" : "meters",
    "value2" : "spm_avg",
    "value3" : "500m_avg"
}


def append_to_list_in_file(file_path: str, var_name: str, new_value):
    with open(file_path, "r") as f:
        content = f.read()

    # Match "var_name = [ ... ]" — DOTALL so it works even if the list spans multiple lines
    pattern = re.compile(rf"^{var_name}\s*=\s*(\[.*?\])", re.MULTILINE | re.DOTALL)
    match = pattern.search(content)
    if not match:
        raise ValueError(f"Could not find list '{var_name}' in {file_path}")

    old_list_str = match.group(1)
    current_list = ast.literal_eval(old_list_str)   # safely parse the list literal
    current_list.append(new_value)
    new_list_str = repr(current_list)

    new_content = content[:match.start(1)] + new_list_str + content[match.end(1):]

    with open(file_path, "w") as f:
        f.write(new_content)


def parse_value(raw: str):
    """Convert form string to int/float if possible, else leave as string."""
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    return raw


# --- Landing page ---

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h2>Gym Data Entry</h2>
            <a href="/scale">Enter Scale Data</a><br><br>
            <a href="/cardio">Enter Cardio Data</a>
        </body>
    </html>
    """


# --- Scale page ---

@app.get("/scale", response_class=HTMLResponse)
def show_scale_form():
    return """
    <html>
        <body>
            <h2>Scale Data</h2>
            <form action="/scale/submit" method="post">
                Weight: <input type="text" name="value1"><br><br>
                Body Fat %: <input type="text" name="value2"><br><br>
                Muscle Mass: <input type="text" name="value3"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """


@app.post("/scale/submit")
def submit_values(
    value1: str = Form(...),
    value2: str = Form(...),
    value3: str = Form(...),
):
    form_values = {"value1": value1, "value2": value2, "value3": value3}
    results = {}

    for field, raw in form_values.items():
        var_name = SCALE_LIST_NAMES[field]
        value = parse_value(raw)
        append_to_list_in_file(FILE_PATH, var_name, value)
        results[var_name] = value

    return {"message": "Saved!", "appended": results}

# --- Cardio page ---

@app.get("/cardio", response_class=HTMLResponse)
def show_cardio_form():
    return """
    <html>
        <body>
            <h2>Cardio Data</h2>
            <form action="/cardio/submit" method="post">
                Duration (min): <input type="text" name="value1"><br><br>
                Distance (km): <input type="text" name="value2"><br><br>
                Avg Heart Rate: <input type="text" name="value3"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """


@app.post("/cardio/submit")
def submit_cardio(
    value1: str = Form(...),
    value2: str = Form(...),
    value3: str = Form(...),
):
    form_values = {"value1": value1, "value2": value2, "value3": value3}
    results = {}
    for field, raw in form_values.items():
        var_name = CARDIO_LIST_NAMES[field]
        value = parse_value(raw)
        append_to_list_in_file(CARDIO_FILE, var_name, value)
        results[var_name] = value
    return {"message": "Cardio data saved!", "appended": results}