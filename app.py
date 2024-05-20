from flask import Flask, render_template, request, redirect, url_for, session
import sys
import fileinput

# replace all occurrences of 'sit' with 'SIT' and insert a line after the 5th


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace 'your_secret_key_here' with a strong secret key.

def checkcode(code):
    if code is None:
        return False, []
    with open("./codes.txt", "r") as txt:
        txtarr = txt.read().split("\n")
    if code in txtarr:
        for i, line in enumerate(fileinput.input('./codes.txt', inplace=1)):
            sys.stdout.write(line.replace("".join([code, "\n"]), ''))  # replace 'sit' and write
        return True, txtarr
    elif code == "admin123": #COMANDO ADMIN PARA TESTE
        return True, txtarr
    else:
        return False, txtarr
def checkvote(sala, numero):
    try:
        with open("./numbers.txt", "r") as txt:
            narr = txt.read().split("\n")

        sala = int(sala)
        if 6 <= sala <= 9:
            if numero in narr:
                index = narr.index(numero)
                if str(sala) == narr[index - 1][0]:
                    with open("./votes.txt", "r") as txt:
                        votes = txt.read()
                    votes_dict = {}
                    for vote in votes.split("\n"):
                        if vote:
                            parts = vote.split(" ")
                            if len(parts) == 2:
                                votes_dict[parts[0]] = parts[1]
                            
                    vote_key = narr[index - 1]
                    if vote_key in votes_dict:
                        votes_dict[vote_key] = str(int(votes_dict[vote_key]) + 1)
                    else:
                        votes_dict[vote_key] = "1"
                    
                    with open("./votes.txt", "w") as txt:
                        for key, value in votes_dict.items():
                            txt.write(f"{key} {value}\n")
                    return True
    except Exception as e:
        print(f"An error occurred: {e}")
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        session['has_voted'] = False
        return render_template("code.html")
    elif request.method == 'POST':
        code = request.form.get('codeinput')
        valid_code, _ = checkcode(code)
        if valid_code:
            if session.get('has_voted'):
                data = "Você já votou"
                return render_template("error.html", data=data)
            return render_template("vote.html")
        data = "Código Inválido"
        return render_template("error.html", data=data)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if session.get('has_voted'):
        return redirect(url_for('main_page'))

    if request.method == 'POST':
        sala = request.form.get("votesala")
        numero = request.form.get("votenumero")
        if sala and numero:
           
            if checkvote(sala, numero):
                session['has_voted'] = True
                data = "Você já votou"
                return render_template("vote-confirmed.html", data=data)
            else:
                data = "Voto inválidos"
                return render_template("error.html", data=data)
    print("Details!")
    data = "Detalhes inválidos"
    return render_template("error.html", data=data)


@app.route('/main_page')
def main_page():
    print("BLOODY!")
    data = "Você já votou."
    return render_template("error.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
