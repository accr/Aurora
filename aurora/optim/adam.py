import numpy as np
from .base import Base


class Adam(Base):
    def __init__(self, cost, optim_dict, lr=0.1, beta1=0.9, beta2=0.995, eps=1e-7):
        super().__init__(cost, optim_dict, lr)
        self.beta1 = beta1
        self.beta2 = beta2
        self.vec = {key: np.zeros_like(optim_dict[key]) for key in optim_dict.keys()}
        self.mom = {key: np.zeros_like(optim_dict[key]) for key in optim_dict.keys()}
        self.time_step = 0
        self.eps = eps

    def step(self, feed_dict):
        feed_data = feed_dict.copy()
        for param in list(self.optim_dict.keys()):
            feed_data[param] = self.optim_dict[param]
        exe_output = self.executor.run(feed_data)

        parameters = list(self.optim_dict.keys())
        self.time_step += 1
        vec_hat = {key: np.zeros_like(self.optim_dict[key]) for key in self.optim_dict.keys()}
        mom_hat = {key: np.zeros_like(self.optim_dict[key]) for key in self.optim_dict.keys()}
        for i in range(len(parameters)):
            self.mom[parameters[i]] = self.beta1 * self.mom[parameters[i]] + (1 - self.beta1) * exe_output[i + 1]
            mom_hat[parameters[i]] = self.mom[parameters[i]] / (1 - self.beta1 ** self.time_step)

            self.vec[parameters[i]] = self.beta2 * self.vec[parameters[i]] + (1 - self.beta2) * (exe_output[i + 1] ** 2)
            vec_hat[parameters[i]] = self.vec[parameters[i]] / (1 - self.beta2 ** self.time_step)

        for i in range(len(parameters)):
            self.optim_dict[parameters[i]] += -self.lr * mom_hat[parameters[i]] / (
            np.sqrt(vec_hat[parameters[i]]) + self.eps)

        step_param = self.optim_dict.copy()
        step_param[self.cost] = exe_output[0]
        return step_param
