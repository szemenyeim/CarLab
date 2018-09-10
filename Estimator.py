import numpy as np

class Estimator(object):
    def __init__(self):
        super(Estimator,self).__init__()
        self.curvatures = np.array([])
        self.deviations = np.array([])
        self.numEstim = 25
        self.slopeEstimNum = 5
        self.filteredDeviations = np.zeros(self.slopeEstimNum)
        self.X = np.transpose(np.array([np.linspace(0,self.slopeEstimNum-1, num=self.slopeEstimNum),np.ones(self.slopeEstimNum)]))

    def update(self, curv, dev):

        self.curvatures = np.append(self.curvatures,curv)
        self.deviations = np.append(self.deviations,dev)

        if len(self.curvatures) > self.numEstim:
            self.curvatures = np.delete(self.curvatures,0)
        if len(self.deviations) > self.numEstim:
            self.deviations = np.delete(self.deviations,0)

        if len(self.curvatures) != self.numEstim or len(self.deviations) != self.numEstim:
            return 0,0,0

        curvEst = np.mean(self.curvatures)
        devEst = np.mean(self.deviations)

        self.filteredDeviations = np.append(self.filteredDeviations, devEst)
        self.filteredDeviations = np.delete(self.filteredDeviations,0)

        lineEst = np.linalg.lstsq(self.X,self.filteredDeviations, rcond=None)

        lineEst = lineEst[0]

        slopeEst = lineEst[0]

        return curvEst,slopeEst,devEst


