import numpy as np

class Kalman():
    def __init__(self, A=1, H=1, Q=0.1, R=4, P=50):
        self.A = A
        self.H = H
        self.Q = Q
        self.R = R
        self.P = P

    def __call__(self, z):
        x = np.zeros(len(z))
        x[0] = z[0]
        for i in range(1, len(z)):
            z_meas = z[i]
            x[i], self.P = self.kalman_filter(z_meas, x[i-1], self.P)

        return x

    def kalman_filter(self, z_meas, x_esti, P):
        # (1) Prediction.
        x_pred = self.A * x_esti
        P_pred = self.A * self.P * self.A + self.Q

        # (2) Kalman Gain.
        self.K = P_pred * self.H / (self.H * P_pred * self.H + self.R)

        # (3) Estimation.
        x_esti = x_pred + self.K * (z_meas - self.H * x_pred)

        # (4) Error Covariance.
        self.P = P_pred - self.K * self.H * P_pred

        return x_esti, self.P

class MA():
    def __init__(self, k):
        self.k = k

    def __call__(self, l, start_index=0):
        ma = []
        for i in range(len(l)):
            if i >= self.k - 1:
                ma.append(np.mean(l[i - self.k + 1:i]))
            else:
                ma.append(np.mean(l[:self.k]))

        return ma[start_index:]
