import numpy as np

class Estimator(object):
    def __init__(self):
        super(Estimator,self).__init__()

        # Number of measurementes to use
        self.numEstim = 25

        # Number of estimates to use for slope estimation
        self.slopeEstimNum = 5

        # Iteration counter
        self.iter = 0

        # Arrays for input variables
        self.curvatures = np.zeros(self.numEstim)
        self.deviations = np.zeros(self.numEstim)

        # Store filtered deviations for slope estimation
        self.filteredDeviations = np.zeros(self.slopeEstimNum)

        # Create coefficient matrix for LS estimate
        '''
        [ 0 1 ]
        [ 1 1 ]
        [ 2 1 ]
        [ 3 1 ]
        [ 4 1 ]
        '''
        self.X = np.transpose(np.array([np.linspace(0,self.slopeEstimNum-1, num=self.slopeEstimNum),np.ones(self.slopeEstimNum)]))

    def update(self, curv, dev):

        # Shift the arrays


        # Write new elements to replace the last


        # Compute means


        # Append latest deviation estimate and remove oldest


        self.iter += 1

        if self.iter < self.slopeEstimNum:
            slopeEst = 0
        else:
            # Perform LS estimation to fit a line on the deviations
            None


            # Get the slope of the line - change of the deviation


        return curvEst,slopeEst,devEst


