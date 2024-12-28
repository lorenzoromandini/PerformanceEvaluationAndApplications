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

Rc = [97.60157356686157, 253.79034765290316, 243.21709383083808]
print(
    f"Average system response time [min]:\n\t-Employees: {Rc[0]}\n\t-Maintainers: {Rc[1]}\n\t-Customers: {Rc[2]}"
)

Xwh = 0.03302924881326401
print("Throughput of Warehouse [job/min]:", Xwh)

print("Class-independent average number of jobs in the system (N):", sum(Nc))

Xc = [0.03666758853698876, 0.005528557410522435, 0.333333333333]

X = sum(Xc)

# Residence Times without the think time (terminal)
RkA = [447.83925845907936, 0, 83.25562574114423, 4.3459478257173405]
RkB = [288.84668715298255, 0, 251.79034765290316, 0]
RkC = [228.2170938309131, 14.999999999925004, 0, 0]

Rk = [
    Xc[0] / X * RkA[0] + Xc[1] / X * RkB[0] + Xc[2] / X * RkC[0],
    Xc[0] / X * RkA[1] + Xc[1] / X * RkB[1] + Xc[2] / X * RkC[1],
    Xc[0] / X * RkA[2] + Xc[1] / X * RkB[2] + Xc[2] / X * RkC[2],
    Xc[0] / X * RkA[3] + Xc[1] / X * RkB[3] + Xc[2] / X * RkC[3],
]

R = sum(Rk)
print("Class independent average system response time (R [min]):", R)
