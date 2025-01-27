Rsys = 607.9493
Z = 600

Rj = Rsys - Z
print("Average response time of one job [sec]:", Rj)

X = 0.0789
print("System throughput [job/min]:", X * 60)

U1avg = 0.1426
U2avg = 0.1646
Nfcr = 150.4786

U1tot = U1avg * Nfcr
U2tot = U2avg * Nfcr
print(f"Total Utilization of:\n\t-Node 1: {U1tot}\n\t-Node 2: {U2tot}")

QT = 1.1964
A = 39.5978

W = QT * A
print("Average number of tasks waiting to enter the system:", W)
