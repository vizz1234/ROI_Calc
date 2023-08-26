from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    A1 = request.form.get("A1", "")
    n1 = request.form.get("n1", "")
    w = request.form.get("w", "")
    A2 = request.form.get("A2", "")
    n2 = request.form.get("n2", "")
    
    result = None
    if request.method == "POST":
        A1 = float(request.form["A1"])
        n1 = int(request.form["n1"])
        w = int(request.form["w"])
        A2 = float(request.form["A2"])
        n2 = int(request.form["n2"])
        pr = float(n1) * float(A1)

        def calculate_equation(r, A1, n1, w, A2, n2):
            equation_left = (A1 * ((1 + r) ** n1 - 1) / r) * (1 + r) ** w
            equation_right = (A2 * ((1 + r) ** n2 - 1) / (r * (1 + r) ** n2)) + ((n1 * A1) / ((1 + r) ** n2))
            return equation_left - equation_right

        def calculate_interest_rate(A1, n1, w, A2, n2):
            r_guess = 0.05  # Starting guess for the interest rate
            tolerance = 1e-6  # Tolerance for the Newton-Raphson method
            max_iterations = 1000

            for _ in range(max_iterations):
                f = calculate_equation(r_guess, A1, n1, w, A2, n2)
                f_prime = (calculate_equation(r_guess + 1e-6, A1, n1, w, A2, n2) - f) / 1e-6

                r_guess = r_guess - f / f_prime

                if abs(f) < tolerance:
                    return r_guess

            return None  # If no convergence is achieved

        interest_rate = calculate_interest_rate(A1, n1, w, A2, n2)
        result = interest_rate * 100
        result = np.round(result, 2)
        if interest_rate is not None:
            print("Your rate of interest is approximately: {:.2f}%".format(interest_rate * 100))
        else:
            print("Rate of interest calculation did not converge.")

        

        return render_template("index.html", result=result, A1=A1, n1=n1, w=w, A2=A2, n2=n2, pr = pr)
    
    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug)
