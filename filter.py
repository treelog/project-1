import numpy as np
from utils import *
from .padding import get_padder
from scipy.stats import norm

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


class BaseSpatialFilter():
    """Base class for time series filtering.
    """

    def __init__(self, win_size=3, padding="same", n_iter=1):
        assert win_size % 2 == 1, "window size must be odd value."
        assert padding in ("zero", "same", "identical"), \
            "padding method has to be `zero`, `same` or `identical`."

        self.win_size = win_size
        self.padder = get_padder(padding, {"padding_size": win_size // 2})
        self.med_idx = win_size // 2
        self.n_iter = n_iter

    def fit(self, seq):
        self.seq_ = seq  # keep original signal internal
        # padding
        self.seq_padded_ = self.padder.transform(seq)

        return self

    def transform(self, seq):
        for i in range(self.n_iter):
            x = self.seq_padded_
            # do filtering for each sub-sequence
            filt = []
            for xs in window(x, n=self.win_size):
                filt.append(self._filt(xs))
            x = np.hstack(filt)
            self.seq_padded_ = self.padder.transform(x)

        return x

    def fit_transform(self, seq):
        self.fit(seq)
        return self.transform(seq)

    @abc.abstractmethod
    def _filt(self, sub_seq):
        """Execute filtering for sub sequence.
        """
        pass

class GaussianFilter(BaseSpatialFilter):
    """Gaussian Filtering Class.
    """
    def __init__(self, win_size, padding="same", n_iter=1, sigma_d=None):
        super(GaussianFilter, self).__init__(win_size, padding, n_iter)
        if sigma_d is None:
            sigma_d = self._suggest_sigma_d()
        self.sigma_d = sigma_d
        self.weight = norm.pdf(np.arange(win_size), loc=self.med_idx, scale=self.sigma_d)
        self.weight /= self.weight.sum()

    def _filt(self, sub_seq):
        prod = self.weight.reshape(1, -1) @ sub_seq.reshape(-1, 1)
        return prod[0, 0]

    def _suggest_sigma_d(self):
        RATIO = 4
        return self.win_size / (RATIO * 2)

class BilateralFilter(GaussianFilter):
    """Bilateral Filtering Class.
    """
    def __init__(self, win_size, padding="same", n_iter=1,\
            sigma_d=None, sigma_i=None):
        super(BilateralFilter, self).__init__(win_size, padding, n_iter, sigma_d)
        self.sigma_i = sigma_i

    def _filt(self, sub_seq):
        if self.sigma_i is None:
            self.sigma_i = self._suggest_sigma_i()

        w = norm.pdf(sub_seq, loc=sub_seq[self.med_idx], scale=self.sigma_i)
        weight = self.weight * w
        weight /= weight.sum()

        prod = weight.reshape(1, -1) @ sub_seq.reshape(-1, 1)
        return prod[0, 0]

    def _suggest_sigma_i(self):
        """Suggest sigma param.
        Estimate noise standard deviation.
        """
        x = self.seq_
        # 1% of total range
        return (x.max() - x.min()) / 100.0
