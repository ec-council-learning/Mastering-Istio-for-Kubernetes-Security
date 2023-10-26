from flask import Flask, render_template

app = Flask(__name__)

@app.route('/blue')
def blue_route():
    return render_template('blue.html')

@app.route('/red')
def red_route():
    return render_template('red.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

#port 5000 may be reserved port for MAC system, feel free to change other ports