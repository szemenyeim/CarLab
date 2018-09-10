import numpy as np

class Estimator(object):
    def __init__(self):
        super(Estimator,self).__init__()

        # Arrays for input variables
        self.curvatures = np.array([])
        self.deviations = np.array([])

        # Number of measurementes to use
        self.numEstim = 25

        # Number of estimates to use for slope estimation
        self.slopeEstimNum = 5

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

        # Append new inputs to the arrays
        self.curvatures = np.append(self.curvatures,curv)
        self.deviations = np.append(self.deviations,dev)

        # If the array is too large, remove the last element
        if len(self.curvatures) > self.numEstim:
            self.curvatures = np.delete(self.curvatures,0)
        if len(self.deviations) > self.numEstim:
            self.deviations = np.delete(self.deviations,0)

        # Compute means
        curvEst = np.mean(self.curvatures)
        devEst = np.mean(self.deviations)

        # Append latest deviation estimate and remove oldest
        self.filteredDeviations = np.append(self.filteredDeviations, devEst)
        self.filteredDeviations = np.delete(self.filteredDeviations,0)

        # Perform LS estimation to fit a line on the deviations
        lineEst, = np.linalg.lstsq(self.X,self.filteredDeviations, rcond=None)

        # Get the slope of the line - change of the deviation
        slopeEst = lineEst[0]

        return curvEst,slopeEst,devEst


