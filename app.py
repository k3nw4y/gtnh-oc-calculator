from cgitb import reset
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("app.html")


@app.route("/calculate", methods=['POST'])
def calculate():
    tier = ["ULV", "LV", "MV", "HV", "EV", "IV", "LuV", "ZPMV", "UV", "MaxV"]
    a = request.form['recipeTier']
    recipeTier = float(a)
    machineTier = request.form['machineTier']
    machineTier = float(machineTier)
    eu = request.form['eu']
    eu=float(eu)
    seconds = request.form['seconds']
    seconds = float(seconds)

    while True:
        try:
            if recipeTier > 9 or recipeTier < 0 or recipeTier % 1 != 0:
                raise TypeError
            if machineTier > 9 or machineTier < 0 or machineTier % 1 != 0:
                raise TypeError
            if recipeTier > machineTier:
                raise Exception
            amps = 0
            if recipeTier != machineTier:
                seconds /= (2 ** (machineTier - recipeTier))
                amps = (eu * (4 ** (machineTier - recipeTier))) / 2 ** ((machineTier * 2) + 3)
            else:
                amps = eu / 2 ** ((machineTier * 2) + 3)
            if recipeTier == 0 and recipeTier != machineTier:
                seconds *= 2
                # amps /= 4 have no idea what it does so
            result=("That " + tier[int(recipeTier)] + " recipe will take " + "{:,.2f}".format(seconds) + " seconds to complete and will use " + str(amps) + " amps with an " + tier[int(machineTier)] + " tier machine!")
            return render_template('app.html', result=result)
        except ValueError as error:
            result= " - Please Only Enter Numbers! -"
            return render_template('app.html', result=result)
        except TypeError as error:
            result= " - Please Enter a Valid Tier! -"
            return render_template('app.html', result=result)
        except Exception as error:
            result=" - Recipe Voltage Cannot Be Greater Than Machine Voltage -"
            return render_template('app.html', result=result)
