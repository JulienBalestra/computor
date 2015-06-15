# Equation Solver [![Build Status](https://travis-ci.org/JulienBalestra/computor.svg?branch=master)](https://travis-ci.org/jbalestra/computor)


This project allow to solve polynomial equation in the following degrees :

* 0
* 1
* 2


## Language

Used Python 2.7 for this project

## How to use


    ./solver.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
    ./solver.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 0"
    ...
    ./solver.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 0" -g True

**See the illustrated example below :**

<img src="computor.png">
    
**In python projects :**


    from solver import Equation
    
**With the Web platform :**

    python web_engine.py
    
## Amazon EB

This project is ready to be push on AWS Elastic Beanstalk.
Just upload a git archive on the EB platform :

    git archive --format=zip HEAD > computor.zip

## Contributors

* Julie Rossi
* Umi Lefebvre
* Julien Balestra
