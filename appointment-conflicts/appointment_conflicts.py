#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Coding challenge to find all conflicts of a list of appointments."""


class Appointment(object):
    """
    An appointment.

    Parameters
    ----------
    name : str
        Describe what the appointment is about.
    start : int
    end : int
    """
    def __init__(self, name, start, end):
        assert start <= end
        self.name = name
        self.start = start
        self.end = end

    def __lt__(self, other):
        """Compare by start of the appointment."""
        return self.start < other.start

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def is_conflict(a, b):
    """
    Check if appointments a and b overlap.

    Parameters
    ----------
    a : Appointment
    b : Appointment

    Returns
    -------
    bool
        True if they overlap, otherwise False.
    """
    a, b = min(a, b), max(a, b)
    return a.end >= b.start


def get_conflicts(appointments):
    """
    Print all conflicts.

    Parameters
    ----------
    appointments : list
        List of Appointments
    """
    for i, a in enumerate(appointments):
        for b in appointments[i+1:]:
            if is_conflict(a, b):
                print("%s and %s overlap." % (a, b))

if __name__ == "__main__":
    """
    The following appointments get generated:
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

    # Now you can apply some sweep line algorithm
    appointments = sorted(appointments)
    print(appointments)
    get_conflicts(appointments)
