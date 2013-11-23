#!/usr/bin/env python

class Appointment(object):
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    def __lt__(self, other):
        return self.start < other.start

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

def isConflict(a, b):
    a, b = min(a,b), max(a,b)
    return a.end >= b.start

def getConflicts(appointments):
    for i,a in enumerate(appointments):
        for b in appointments[i+1:]:
            if isConflict(a, b):
                print("%s and %s overlap." % (a, b))

if __name__ == "__main__":
    """
        A: ------
        B:    ------
        C:  ----
        D:            ---
    """
    appointments = []
    appointments.append(Appointment("A", 0, 10))
    appointments.append(Appointment("B", 5, 15))
    appointments.append(Appointment("C", 2, 8))
    appointments.append(Appointment("D", 18, 20))
    appointments = sorted(appointments) # Now you can apply some sweep line algorithm
    print appointments
    getConflicts(appointments)

