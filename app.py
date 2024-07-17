from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = "34534randomkey5345"

# Establishing connection to database
def conn_db():
    db_name = "database.db"
    conn = sqlite3.connect(db_name)
    return conn

# Route for home page
@app.route("/")
def index():
    return render_template("home.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    
    if request.method == "POST":
        genders = request.form.getlist("gender")
        locations = request.form.getlist("location")
        user_gender = request.form.get("user-gender")
        hobbies = request.form.get("hobby-list") if request.form.get("hobby-list") else ""
        query_parts = []
        people = []

        hobbies = hobbies.split(" ")
        hobbies = [i for i in hobbies if i]

        try:
            if locations:
                location_queries = []
                for location in locations:
                    for gender in genders:
                        if gender in ["Male", "Female", "Nonbinary"]:
                            if hobbies:
                                hobby_conditions = " OR ".join([f"Interests LIKE '%{hobby}%'" for hobby in hobbies])
                            
                                location_queries.append(
                                    f"SELECT * FROM {gender} WHERE County = '{location}' AND Seeking = '{user_gender}' AND ({hobby_conditions})"
                                )
                            else:
                                    location_queries.append(f"SELECT * FROM {gender} WHERE County = '{location}' AND Seeking = '{user_gender}'"
                                )
                query_parts.extend(location_queries)

            if not query_parts:
                raise Exception()
            else:
                query = " UNION ".join(query_parts)
                print(query)
                with conn_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute(query)
                    people = cursor.fetchall()
        except:
            warning = True


        return render_template("search.html", people=people, warning=True)

    return render_template("search.html")

@app.route("/profile_<gender>_<int:id>")
def profile(gender, id):
    with conn_db() as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM {gender} WHERE id = ?"
        cursor.execute(query, (id,))
        person = cursor.fetchone()
    favourites = session.get('favourites', "").split(",")
    is_favourited = f"{gender}_{id}" in favourites
    return render_template("profile.html", person=person, is_favourited=is_favourited)

@app.route("/favourite_<gender>_<int:id>")
def favourite(gender, id):
    favourites = session.get("favourites", "")
    favourites = favourites.split(",") if favourites else []

    fav_item = f"{gender}_{id}"
    if fav_item in favourites:
        favourites.remove(fav_item)
    else:
        favourites.append(fav_item)

    session["favourites"] = ",".join(favourites)
    return redirect(url_for("account"))

@app.route("/account")
def account():
    favourites = session.get('favourites', "")
    favourites = favourites.split(",") if favourites else []
    people = []

    with conn_db() as conn:
        cursor = conn.cursor()
        for fav in favourites:
            gender, id = fav.split('_')
            cursor.execute(f'SELECT * FROM {gender} WHERE id=?', (id,))
            person = cursor.fetchone()
            if person:
                people.append(person)

    return render_template("account.html", people=people)

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

if __name__ == "__main__":
    app.run(debug=True)