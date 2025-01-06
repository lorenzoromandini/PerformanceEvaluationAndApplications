Uk = [0.9999236149157111, 0.8333333333325, 0.8817272726861776, 0.13750345701370786]
print(
    f"Utilization:\n\t-Web Server: {Uk[0]}\n\t-Check Out: {Uk[1]}\n\t-Ware House: {Uk[2]}\n\t-Packing: {Uk[3]}"
)

Nc = [20, 3, 81.07236461019829]
print(
    f"Average number of customers in the system:\n\t-Employees: {Nc[0]}\n\t-Maintainers: {Nc[1]}\n\t-Customers: {Nc[2]}"
)

Nws = 94.09045576288045
print("Average number of jobs in the Web Server:", Nws)

# System Response Time per class without the think time (Terminal)
Rc = [535.4408320259408, 540.6370348058857, 243.21709383083808]
print(
    f"Average system response time [min]:\n\t-Employees: {Rc[0]}\n\t-Maintainers: {Rc[1]}\n\t-Customers: {Rc[2]}"
)

Xwh = 0.03302924881326401
print("Throughput of Warehouse [job/min]:", Xwh)

print("Class-independent average number of jobs in the system (N):", sum(Nc))

Xc = [0.03666758853698876, 0.005528557410522435, 0.333333333333]
X = sum(Xc)

R = Xc[0] / X * Rc[0] + Xc[1] / X * Rc[1] + Xc[2] / X * Rc[2]
print("Class independent average system response time (R [min]):", R)
