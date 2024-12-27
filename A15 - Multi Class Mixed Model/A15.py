print(
    "Utilization:\n\t-Web Server: 0.9999743425915374\n\t-Check Out: 0.8332499999999999\n\t-Ware House: 0.8574087470610732\n\t-Packing: 0.16449478455190158"
)
print(
    "Average number of customers in the system:\n\t-Employees: 20\n\t-Maintainers: 3\n\t-Customers: 83.50817535034157"
)
print("Average number of jobs in the Web Server: 97.14878219208322")
print(
    "Average system response time [min]:\n\t-Employees: 83.79365823422947\n\t-Maintainers: 225.55340782942446\n\t-Customers: 250.54958100912563"
)
print("Throughput of Warehouse [job/min]: 0.0313488641823262")
print("Class-independent average number of jobs in the system (N): 106.50817535034157")

XA = 0.036554396567089247
XB = 0.005760786585363729
XC = 0.3333

X = XA + XB + XC

RA = 83.79365823422947
RB = 225.55340782942446
RC = 250.54958100912563

R = XA / X * RA + XB / X * RB + XC / X * RC
print("Class independent average system response time (R [min]):", R)
