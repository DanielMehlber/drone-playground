### Trajectory error

| Scenario | Hold / step | Method | Position RMSE | Position at 2 s | Attitude RMSE | Attitude at 2 s |
|---|---:|---|---:|---:|---:|---:|
| Hover | 0.5 ms | nonlinear | 0 m | 0 m | 0° | 0° |
| Hover | 0.5 ms | linear, Jacobian held | 0 m | 0 m | 0° | 0° |
| Hover | 1.0 ms | nonlinear | 0 m | 0 m | 0° | 0° |
| Hover | 1.0 ms | linear, Jacobian held | 0 m | 0 m | 0° | 0° |
| Hover | 2.0 ms | nonlinear | 0 m | 0 m | 0° | 0° |
| Hover | 2.0 ms | linear, Jacobian held | 0 m | 0 m | 0° | 0° |
| Hover | 5.0 ms | nonlinear | 0 m | 0 m | 0° | 0° |
| Hover | 5.0 ms | linear, Jacobian held | 0 m | 0 m | 0° | 0° |
| Hover | 10.0 ms | nonlinear | 0 m | 0 m | 0° | 0° |
| Hover | 10.0 ms | linear, Jacobian held | 0 m | 0 m | 0° | 0° |
| Pitch pulse | 0.5 ms | nonlinear | 6.713e-04 m | 0.0013 m | 0.00435° | 0° |
| Pitch pulse | 0.5 ms | linear, Jacobian held | 3.570e-08 m | 8.447e-08 m | 2.832e-07° | 0° |
| Pitch pulse | 1.0 ms | nonlinear | 0.00151 m | 0.00292 m | 0.00979° | 0° |
| Pitch pulse | 1.0 ms | linear, Jacobian held | 1.696e-07 m | 4.011e-07 m | 3.102e-07° | 0° |
| Pitch pulse | 2.0 ms | nonlinear | 0.00319 m | 0.00616 m | 0.0207° | 3.818e-06° |
| Pitch pulse | 2.0 ms | linear, Jacobian held | 7.350e-07 m | 1.738e-06 m | 3.702e-07° | 0° |
| Pitch pulse | 5.0 ms | nonlinear | 0.00825 m | 0.0159 m | 0.0533° | 2.673e-05° |
| Pitch pulse | 5.0 ms | linear, Jacobian held | 4.815e-06 m | 1.136e-05 m | 3.912e-07° | 0° |
| Pitch pulse | 10.0 ms | nonlinear | 0.0167 m | 0.0322 m | 0.108° | 1.075e-04° |
| Pitch pulse | 10.0 ms | linear, Jacobian held | 1.958e-05 m | 4.605e-05 m | 4.005e-07° | 0° |
| Roll reversal | 0.5 ms | nonlinear | 7.478e-04 m | 0.00145 m | 0.00485° | 0° |
| Roll reversal | 0.5 ms | linear, Jacobian held | 4.437e-08 m | 1.050e-07 m | 2.870e-07° | 0° |
| Roll reversal | 1.0 ms | nonlinear | 0.00168 m | 0.00325 m | 0.0109° | 0° |
| Roll reversal | 1.0 ms | linear, Jacobian held | 2.108e-07 m | 4.986e-07 m | 3.436e-07° | 0° |
| Roll reversal | 2.0 ms | nonlinear | 0.00356 m | 0.00687 m | 0.0231° | 5.663e-06° |
| Roll reversal | 2.0 ms | linear, Jacobian held | 9.136e-07 m | 2.160e-06 m | 4.077e-07° | 0° |
| Roll reversal | 5.0 ms | nonlinear | 0.00919 m | 0.0177 m | 0.0595° | 3.722e-05° |
| Roll reversal | 5.0 ms | linear, Jacobian held | 5.985e-06 m | 1.412e-05 m | 4.183e-07° | 0° |
| Roll reversal | 10.0 ms | nonlinear | 0.0186 m | 0.0358 m | 0.12° | 1.491e-04° |
| Roll reversal | 10.0 ms | linear, Jacobian held | 2.433e-05 m | 5.724e-05 m | 4.005e-07° | 0° |
| Climb with pitch | 0.5 ms | nonlinear | 2.819e-04 m | 6.524e-04 m | 0.00197° | 0.00341° |
| Climb with pitch | 0.5 ms | linear, Jacobian held | 8.788e-09 m | 2.318e-08 m | 4.453e-07° | 0° |
| Climb with pitch | 1.0 ms | nonlinear | 6.345e-04 m | 0.00147 m | 0.00442° | 0.00766° |
| Climb with pitch | 1.0 ms | linear, Jacobian held | 4.176e-08 m | 1.101e-07 m | 4.420e-07° | 1.708e-06° |
| Climb with pitch | 2.0 ms | nonlinear | 0.00134 m | 0.0031 m | 0.00935° | 0.0162° |
| Climb with pitch | 2.0 ms | linear, Jacobian held | 1.811e-07 m | 4.772e-07 m | 4.890e-07° | 0° |
| Climb with pitch | 5.0 ms | nonlinear | 0.00346 m | 0.00799 m | 0.0241° | 0.0417° |
| Climb with pitch | 5.0 ms | linear, Jacobian held | 1.189e-06 m | 3.124e-06 m | 4.830e-07° | 0° |
| Climb with pitch | 10.0 ms | nonlinear | 0.00703 m | 0.0162 m | 0.0488° | 0.0843° |
| Climb with pitch | 10.0 ms | linear, Jacobian held | 4.847e-06 m | 1.269e-05 m | 7.040e-07° | 0° |

### Speed

| Method | Batch | µs / (step·item) | (step·item) / s |
|---|---:|---:|---:|
| NumPy nonlinear | 1 | 95.5 | 1.0470e+04 |
| NumPy linear map | 1 | 3.76 | 2.6611e+05 |
| Analytic Jacobian | 1 | 36.5 | 2.7383e+04 |
| NumPy Jacobian + map | 1 | 35.6 | 2.8114e+04 |
| Torch CPU nonlinear | 1 | 217 | 4599 |
| Torch CPU linear map | 1 | 6.24 | 1.6022e+05 |
| Autograd Jacobian | 1 | 1.079e+04 | 92.69 |
| CUDA nonlinear, resident | 1 | 1.51e+03 | 661.5 |
| CUDA linear map, resident | 1 | 64.8 | 1.5430e+04 |
| Autograd Jacobian, CUDA | 1 | 5.084e+04 | 19.67 |
| CUDA nonlinear, transfer | 1 | 1.53e+03 | 655.3 |
| CUDA linear map, transfer | 1 | 210 | 4753 |
| Analytic Jacobian + H2D | 1 | 112 | 8956 |
| NumPy nonlinear | 8 | 13.5 | 7.3884e+04 |
| NumPy linear map | 8 | 0.639 | 1.5652e+06 |
| Analytic Jacobian | 8 | 33.4 | 2.9973e+04 |
| NumPy Jacobian + map | 8 | 44.6 | 2.2422e+04 |
| Torch CPU nonlinear | 8 | 28.1 | 3.5544e+04 |
| Torch CPU linear map | 8 | 0.901 | 1.1095e+06 |
| Autograd Jacobian | 8 | 1.132e+04 | 88.32 |
| CUDA nonlinear, resident | 8 | 190 | 5253 |
| CUDA linear map, resident | 8 | 7.07 | 1.4146e+05 |
| Autograd Jacobian, CUDA | 8 | 4.986e+04 | 20.05 |
| CUDA nonlinear, transfer | 8 | 196 | 5096 |
| CUDA linear map, transfer | 8 | 25.1 | 3.9909e+04 |
| Analytic Jacobian + H2D | 8 | 108 | 9299 |
| NumPy nonlinear | 32 | 3.72 | 2.6907e+05 |
| NumPy linear map | 32 | 0.311 | 3.2142e+06 |
| Analytic Jacobian | 32 | 33.9 | 2.9470e+04 |
| NumPy Jacobian + map | 32 | 41.1 | 2.4354e+04 |
| Torch CPU nonlinear | 32 | 8.15 | 1.2270e+05 |
| Torch CPU linear map | 32 | 0.329 | 3.0438e+06 |
| Autograd Jacobian | 32 | 1.040e+04 | 96.11 |
| CUDA nonlinear, resident | 32 | 43.3 | 2.3078e+04 |
| CUDA linear map, resident | 32 | 1.71 | 5.8338e+05 |
| Autograd Jacobian, CUDA | 32 | 5.009e+04 | 19.96 |
| CUDA nonlinear, transfer | 32 | 48.1 | 2.0793e+04 |
| CUDA linear map, transfer | 32 | 5.98 | 1.6721e+05 |
| Analytic Jacobian + H2D | 32 | 107 | 9388 |
| NumPy nonlinear | 128 | 1.23 | 8.1396e+05 |
| NumPy linear map | 128 | 0.216 | 4.6398e+06 |
| Analytic Jacobian | 128 | 33.8 | 2.9563e+04 |
| NumPy Jacobian + map | 128 | 38.9 | 2.5718e+04 |
| Torch CPU nonlinear | 128 | 2.92 | 3.4298e+05 |
| Torch CPU linear map | 128 | 0.291 | 3.4405e+06 |
| Autograd Jacobian | 128 | 1.053e+04 | 94.96 |
| CUDA nonlinear, resident | 128 | 10.8 | 9.2349e+04 |
| CUDA linear map, resident | 128 | 0.491 | 2.0357e+06 |
| Autograd Jacobian, CUDA | 128 | 5.018e+04 | 19.93 |
| CUDA nonlinear, transfer | 128 | 11.7 | 8.5383e+04 |
| CUDA linear map, transfer | 128 | 1.59 | 6.3030e+05 |
| Analytic Jacobian + H2D | 128 | 101 | 9909 |
| NumPy nonlinear | 512 | 0.642 | 1.5583e+06 |
| NumPy linear map | 512 | 0.261 | 3.8275e+06 |
| Analytic Jacobian | 512 | 32.2 | 3.1092e+04 |
| NumPy Jacobian + map | 512 | 38.3 | 2.6123e+04 |
| Torch CPU nonlinear | 512 | 0.733 | 1.3644e+06 |
| Torch CPU linear map | 512 | 0.157 | 6.3622e+06 |
| Autograd Jacobian | 512 | 1.051e+04 | 95.11 |
| CUDA nonlinear, resident | 512 | 3.3 | 3.0320e+05 |
| CUDA linear map, resident | 512 | 0.106 | 9.4094e+06 |
| Autograd Jacobian, CUDA | 512 | 6.531e+04 | 15.31 |
| CUDA nonlinear, transfer | 512 | 3.4 | 2.9439e+05 |
| CUDA linear map, transfer | 512 | 0.575 | 1.7403e+06 |
| Analytic Jacobian + H2D | 512 | 108 | 9232 |
| NumPy nonlinear | 2048 | 0.495 | 2.0219e+06 |
| NumPy linear map | 2048 | 0.189 | 5.2940e+06 |
| Analytic Jacobian | 2048 | 32.5 | 3.0740e+04 |
| NumPy Jacobian + map | 2048 | 38.4 | 2.6019e+04 |
| Torch CPU nonlinear | 2048 | 0.388 | 2.5789e+06 |
| Torch CPU linear map | 2048 | 0.0474 | 2.1098e+07 |
| Autograd Jacobian | 2048 | 1.117e+04 | 89.52 |
| CUDA nonlinear, resident | 2048 | 0.765 | 1.3073e+06 |
| CUDA linear map, resident | 2048 | 0.0279 | 3.5845e+07 |
| Autograd Jacobian, CUDA | 2048 | 5.140e+04 | 19.45 |
| CUDA nonlinear, transfer | 2048 | 0.83 | 1.2047e+06 |
| CUDA linear map, transfer | 2048 | 0.153 | 6.5204e+06 |
| Analytic Jacobian + H2D | 2048 | 115 | 8722 |

### Jacobian agreement on the pitch-pulse reference

- Analytic discrete Jacobian vs autograd, max abs: 4.066e-19
- One-step linear remainder at δ ~ 1e-04: 5.265e-08

