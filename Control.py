import numpy as np
import skfuzzy.control as ctrl

def createContorller():
    # Fuzzy membership centers [-2 -1 0 1 2]
    universe = np.linspace(-2, 2, 5)

    # Create the three fuzzy variables - two inputs, one output
    error = ctrl.Antecedent(universe, 'error')
    delta = ctrl.Antecedent(universe, 'delta')
    output = ctrl.Consequent(universe, 'output')

    # Name fuzzy variables
    names = ['nb', 'ns', 'ze', 'ps', 'pb']
    error.automf(names=names)
    delta.automf(names=names)
    output.automf(names=names)

    # Rule 0: if the error is big negative and changing in the wrong direction, then output is big positive
    rule0 = ctrl.Rule(antecedent=((error['nb'] & delta['nb']) |
                                  (error['ns'] & delta['nb']) |
                                  (error['nb'] & delta['ns'])),
                      consequent=output['pb'], label='rule pb')

    # Rule 1: For somewhat more favourable combinations the output is small positive
    rule1 = ctrl.Rule(antecedent=((error['nb'] & delta['ze']) |
                                  (error['nb'] & delta['ps']) |
                                  (error['ns'] & delta['ns']) |
                                  (error['ns'] & delta['ze']) |
                                  (error['ze'] & delta['ns']) |
                                  (error['ze'] & delta['nb']) |
                                  (error['ps'] & delta['nb'])),
                      consequent=output['ps'], label='rule ps')

    # Rule 2: For good errors and good changes, the output is zero
    rule2 = ctrl.Rule(antecedent=((error['nb'] & delta['pb']) |
                                  (error['ns'] & delta['ps']) |
                                  (error['ze'] & delta['ze']) |
                                  (error['ps'] & delta['ns']) |
                                  (error['pb'] & delta['nb'])),
                      consequent=output['ze'], label='rule ze')

    # Rule 3: For somewhat less favourable combinations the output is small negative
    rule3 = ctrl.Rule(antecedent=((error['ns'] & delta['pb']) |
                                  (error['ze'] & delta['pb']) |
                                  (error['ze'] & delta['ps']) |
                                  (error['ps'] & delta['ps']) |
                                  (error['ps'] & delta['ze']) |
                                  (error['pb'] & delta['ze']) |
                                  (error['pb'] & delta['ns'])),
                      consequent=output['ns'], label='rule ns')

    # Rule 4: if the error is big positive and changing in the wrong direction, then output is big negative
    rule4 = ctrl.Rule(antecedent=((error['ps'] & delta['pb']) |
                                  (error['pb'] & delta['pb']) |
                                  (error['pb'] & delta['ps'])),
                      consequent=output['nb'], label='rule nb')

    # Create fuzzy controller
    system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4])

    # Return fuzzy simulator
    return ctrl.ControlSystemSimulation(system)